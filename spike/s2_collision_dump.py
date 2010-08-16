#!/usr/bin/env python

import sys
import struct
import os
import os.path

# specify a file containing some collision blocks (no Kosinski compression, yet), such
# as from collision/ in the S2 split disassembly.

# outputs a simple SVG file containing separate path elements for each
# of these collision block shapes.
print("usage: %s <collision_dump> <svg_output_dir>" % sys.argv[0])

fn = sys.argv[1]
fs = os.stat(fn).st_size

svg_dir = sys.argv[2]

if(not os.path.isdir(svg_dir)):
    print("<svg_output_dir> needs to be a directory.")
    exit(-1)



if((fs % 16) != 0):
    print("Inappropriately sized file for a Sonic collision map: %d" % fs)
    exit()

f = open(fn, "rb")

for i in range(0, fs / 16):
    row = f.read(16)
#    if(i != 0x8b):
#       continue
    print("BLOCK: 0x%x" % i)

    # create SVG file, write out header and path element.
    # we are doing this naively with strings, rather than some DOM or XML
    # based SVG lib.  call me lazy.
    svg_filename = os.path.join(svg_dir, "%x.svg" % i)
    svg = open(svg_filename, "wb")
    svg.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n\
<svg\n\
   xmlns:svg="http://www.w3.org/2000/svg"\n\
   xmlns="http://www.w3.org/2000/svg"\n\
   version="1.1"\n\
   width="16"\n\
   height="16"\n\
   id="svg2">\n\
  <defs\n\
     id="defs4" />\n\
  <g\n\
     id="layer1">\n\
    <path\n\
       d="M 0,0')

    byte_position = 0
    for column_byte in row:
        column_val = struct.unpack('B', column_byte)[0]

        bits = (0b11100000 & column_val)

        # are all the bits on?
        if(bits != 0xe0):
            # counted from bottom.
            # a height value wants to represent a value between 0 and 16 (17
            # different values), which requires a full five bits.
            height = (0b00011111 & column_val) 
            print("*" * height)
            svg.write(" L %d,%d" % (byte_position, height))
        else:
            # counted from top.
            # anti_height = column_val - 0xf1 # alternate approach
            # that fifth bit (ie., 16) we talked about is always on in this case...
            anti_height = (0b00011111 & column_val) - 16
            print((" " * (anti_height)) + "*" * (16 - anti_height))
        byte_position += 1
            

    svg.write('" id="path2816"\n\
       style="fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" />\n\
  </g>\n\
</svg>')
    svg.close()
