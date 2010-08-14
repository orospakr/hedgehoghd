#!/usr/bin/env python

import sys
import struct
import os


# specify a file containing some collision blocks (no Kosinski compression, yet), such
# as from collision/ in the S2 split disassembly.
print("usage: %s <collision_dump>" % sys.argv[0])

fn = sys.argv[1]
fs = os.stat(fn).st_size

if((fs % 16) != 0):
    print("Inappropriately sized file for a Sonic collision map: %d" % fs)
    exit()

f = open(fn, "rb")

for i in range(0, fs / 16):
    row = f.read(16)
#    if(i != 0x8b):
#       continue
    print("BLOCK: 0x%x" % i)

    # each byte of the row describes a position in the column of the edge.
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
        else:
            # counted from top.
            # anti_height = column_val - 0xf1 # alternate approach
            # that fifth bit (ie., 16) we talked about is always on in this case...
            anti_height = (0b00011111 & column_val) - 16
            print((" " * (anti_height)) + "*" * (16 - anti_height))
