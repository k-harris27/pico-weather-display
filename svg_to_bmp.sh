#!/bin/bash

# This script will convert all of the files in ./svg to .bmp files, for use on the pico.
# Should only be useful for development, as the .bmp files that get used will be
# moved into ./bmp.

set -e
mkdir -p bmp_all

for f in svg/*.svg; do 
	outf=$(basename $f)
	outf=${outf/.svg/.bmp}
	inkscape -w 100 -h 100 -o bmp/tmp.png $f && \
	convert bmp/tmp.png bmp_all/$outf
done

rm bmp/tmp.png
