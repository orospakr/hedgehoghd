#!/usr/bin/env python

# dump a list of defined 128x128 blocks, including a matrix of the addressed 16x16 tiles.

# are the 16x16 tiles (both the generic ones and the per-zone ones) addressed in a single number-space?  I assume so.


import sys
import os
import struct

import array
import importer.kosinski

if(len(sys.argv) != 2):
    print("usage: %s <sonic 2 128x128 block map>" % sys.argv[0])
    exit(-1)

bmfn = sys.argv[1]

#bmfs = os.stat(bmfn).st_size

bm = importer.kosinski.decompress_file(bmfn).tostring()

if((len(bm) % 128) != 0):
    print("Inappropriately sized level map: %d" % bmfs)
    exit(-1)

blocks = len(bm) / 128

print("There are %d blocks." % blocks)

max_index = 0

for block in range(0, blocks):
    block_data = bm[block*128:(block*128) + 128]
    values = struct.unpack('64H', block_data)
    if(len(values) != 64):
        print "whatsdfaf?"
        exit(-1)
#    print(repr(values))

    for r in range(0, 8):
        result = ""
        row_offset = r * 8

        current_row = values[row_offset:row_offset+8]
        alternate_result = ""
        normal_result  = ""
        index_result = ""
        flip_result = ""

        # SSTT YXII IIII IIII
        for column in current_row:
            # what the heck are primary and alternate collision? is it what makes loops work?  pretty sure it's separate from foreground and
            # background, since these blocks are mapped into foreground and background separately
            alternate_collision = (column & 0xC000) >> 14
            normal_collision = (column & 0x3000) >> 12
            tile_index = column & 0x3FF
            y_flipped = (column & 800)
            x_flipped = (column & 400)

            if(tile_index > max_index):
                max_index = tile_index
            
            if(alternate_collision > 3):
                print "WTF"
                exit(-1)
            if(normal_collision > 3):
                print "WETRDSFDSAF"
                exit(-1)
            
            flip_text = ""
            if(y_flipped):
                flip_text += "Y"
            else:
                flip_text += "_"
            if(x_flipped):
                flip_text += "X"
            else:
                flip_text += "_"
            if(tile_index == 0):
                index_result += "___ "
            else:
                index_result += "%03x " % tile_index
            alternate_result += "%01x " % alternate_collision
            normal_result += "%01x " % normal_collision
            flip_result += "%s " % flip_text

        print index_result + "   " + alternate_result + "   " + normal_result + "   "  + flip_result

        # if(len(current_row) != 16):
        #     print("Huh? Array slice wrong?! %d" % len(current_row))
        #     exit(-1)
        
        # for c in current_row:
        #     result += "%01x " % c
        # print result

    print "..."

print "Done."
print "Greatest tile index seen: 0x%x" % max_index
