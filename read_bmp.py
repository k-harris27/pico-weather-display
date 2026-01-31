import gc

# Seek modes for file IO. Not implemented by micropython os module.
SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2

def gen_pixels(path):
    """
    Return individual pixel values of a bitmap as a generator, in order from left to right, bottom to top.

    All parsing based on info from https://en.wikipedia.org/wiki/BMP_file_format

    First yield of the generator gives the width and height of the image.
    All following yields give a pixel data tuple of either 3 or 4 ints depending on
    the presence of an alpha channel.
    
    :param path: str Path to bitmap file
    """

    with open(path, "rb") as bytes:
        pixel_start, width, height, bit_depth = _parse_header(bytes)

        yield width, height

        if bit_depth < 16:
            raise NotImplementedError("Bit depths less than 16 use a colour table, which is not implemented.")
        bytes_per_pixel = bit_depth // 8
        has_alpha_channel = (bit_depth != 24)  # 24 bit per pixel stores RGB only.
        n_channels = 3 + int(has_alpha_channel)
        bits_per_channel = bit_depth//n_channels
        
        # Bitmap colour order: BGRA
        base_mask = 2**bits_per_channel-1  # Int representing as many 1's as there are bits in a channel.
        channel_masks = [base_mask << (n * bits_per_channel) for n in range(n_channels)]

        # Go to the start of the actual pixel data.
        bytes.seek(pixel_start,SEEK_SET)

        while True:
            pixel_bytes = bytes.read(bytes_per_pixel)

            # End of file.
            if pixel_bytes == b'':
                break

            pixel_int = int.from_bytes(pixel_bytes, "little")
            pixel_channels = tuple((pixel_int & mask) >> (n*bits_per_channel) for n, mask in enumerate(channel_masks))
            yield pixel_channels
        
        gc.collect()  # Make sure to clean up after ourselves. NOTE: Not 100% sure this will work, but hoping it cleans up all the yielded arrays that aren't used any more
        return


def _parse_header(bytes):
    try:
        # Generic header
        assert(bytes.read(2) == b'BM')  # Identifier
        bytes.read(4)  # byte size of BMP file 
        assert(bytes.read(4) == b'\x00\x00\x00\x00')  # Reserved and unused
        pixel_start = int.from_bytes(bytes.read(4), "little")  # Start of pixel data in file
         
        # DIB header
        assert(bytes.read(4) == b'\x7c\x00\x00\x00')  # Size of DIB header
        pixel_width = int.from_bytes(bytes.read(4), "little")  # Pixel width of bitmap
        pixel_height = int.from_bytes(bytes.read(4), "little")  # Pixel height of bitmap
        assert(bytes.read(2) == b'\x01\x00')  # Number of colour planes (Must be 1)
        bit_depth = int.from_bytes(bytes.read(2), "little")  # Bit depth of pixels
        assert(bit_depth in (1,4,8,16,24,32))
        bytes.seek(4, SEEK_CUR)  # Compression method uint id (currently unused)
        bytes.seek(4, SEEK_CUR)  # Total number of bytes of raw pixel data (currently unused)
        bytes.seek(8, SEEK_CUR)  # Discard horizontal and vertical pixel per metre (4 bytes each)
        assert(bytes.read(4) == b'\x00\x00\x00\x00', "Colour tables not currently implemented.")  # If a colour palette is being used, this can be non-zero.

        return pixel_start, pixel_width, pixel_height, bit_depth

    except AssertionError as e:
        raise RuntimeError(f"Bitmap file {bytes.name} header malformed or unknown") from e