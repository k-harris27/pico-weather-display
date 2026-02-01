import gc
import math

# Seek modes for file IO. Not implemented by micropython os module.
SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2

def gen_pixels(path):
    """
    Return individual pixel values of a *monochrome* bitmap as a generator, in order from left to right, bottom to top.

    All parsing based on info from https://en.wikipedia.org/wiki/BMP_file_format

    First yield of the generator gives the width and height of the image.
    All following yields give a boolean representing the state of the monochrome pixels.
    
    :param path: str Path to bitmap file
    """

    with open(path, "rb") as bytes:
        pixel_start, width, height, bit_depth = _parse_header(bytes)

        yield width, height

        if bit_depth != 1:
            raise NotImplementedError("Non-monochrome images are not currently supported. Screen only has 7 colours.")

        row_bytes = math.ceil(width / 32) * 4  # Rows are padded up to the nearest multiple of 4 bytes (32 bits).

        bytes.seek(pixel_start, SEEK_SET)

        while True:
            buffer = bytes.read(row_bytes)

            if buffer == b'':
                break

            current_x = 0
            for byte in buffer:
                for i in range(8):
                    if current_x >= width:
                        break
                    yield (byte & 2**(7-i)) != 0  # Return a bool per bit (little-endian).
                    current_x += 1
                if current_x >= width:
                    break  # This is ugly but I can't think how to make it nicer right now.
        
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
        bytes.seek(4, SEEK_CUR)  # Size of DIB header
        pixel_width = int.from_bytes(bytes.read(4), "little")  # Pixel width of bitmap
        pixel_height = int.from_bytes(bytes.read(4), "little")  # Pixel height of bitmap
        assert(bytes.read(2) == b'\x01\x00')  # Number of colour planes (Must be 1)
        bit_depth = int.from_bytes(bytes.read(2), "little")  # Bit depth of pixels
        assert(bit_depth == 1, f"Bit depth is {bit_depth} not 1")
        bytes.seek(4, SEEK_CUR)  # Compression method uint id (currently unused)
        bytes.seek(4, SEEK_CUR)  # Total number of bytes of raw pixel data (currently unused)
        bytes.seek(8, SEEK_CUR)  # Discard horizontal and vertical pixel per metre (4 bytes each)
        assert(bytes.read(4) == b'\x00\x00\x00\x00', "Colour tables not currently implemented.")  # If a colour palette is being used, this can be non-zero.

        return pixel_start, pixel_width, pixel_height, bit_depth
    
    #except AssertionError as e:
    #    raise RuntimeError("Bitmap file header malformed or unknown") from e

    finally:
        pass