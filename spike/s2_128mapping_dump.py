#!/usr/bin/env python

# dump a list of defined 128x128 blocks, including a matrix of the addressed 16x16 tiles.

# are the 16x16 tiles (both the generic ones and the per-zone ones) addressed in a single number-space?  I assume so.


import sys
import os
import struct

if(len(sys.argv) != 2):
    print("usage: %s <sonic 2 128x128 block map>" % sys.argv[0])
    exit(-1)

bmfn = sys.argv[1]

bmfs = os.stat(bmfn).st_size

if((bmfs % 128) != 0):
    print("Inappropriately sized level map: %d" % bmfs)
    exit(-1)

blocks = bmfs / 128

print("There are %d blocks." % blocks)

bmfd = open(bmfn, "rb")

for block in range(0, blocks):
    block_data = bmfd.read(128)
    values = struct.unpack('64H', block_data)
    if(len(values) != 64):
        print "whatsdfaf?"
        exit(-1)
#    print(repr(values))
    for r in range(0, 8):
        result = ""
        row_offset = r * 8

        current_row = values[row_offset:row_offset+8]
        print(repr(current_row))

        for column in current_row:
            background_colision = column & 0xC00
        # if(len(current_row) != 16):
        #     print("Huh? Array slice wrong?! %d" % len(current_row))
        #     exit(-1)
        
        # for c in current_row:
        #     result += "%01x " % c
        # print result

    print "..."
