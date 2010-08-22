#!/usr/bin/env python

import sys
import os
import struct

if(len(sys.argv) != 2):
    print("usage: %s <sonic 2 level map>" % sys.argv[0])
    exit(-1)

mfn = sys.argv[1]
mfs = os.stat(mfn).st_size

mfd = open(mfn, "rb")

if((mfs % 128) != 0):
    print("Inappropriately sized level map: %d" % mfs)

if((mfs / 128 / 2) != 16):
    print "Sonic 2 levels always have 16 rows. This has: %d" % (mfs / 128 / 2)
    exit(-1)

# 256 rows for both EHZ and HTZ
# 128 rows per zone
# 64 rows per act, so 32 (0x20) actual rows (foreground/background interlacing
# so, the problem is that I was assuming.

foreground = []
background = []

for y in range(0, mfs / 128):
    row = mfd.read(128)
    if((y % 2) == 0):
        foreground.append(row)
    else:
        background.append(row)

print "Foreground:"
for row in foreground:
    result = ""
    for block in row:
        result += "%02x " % struct.unpack('B', block)[0]
    print(result)

print "Background:"
for row in background:
    result = ""
    for block in row:
        result += "%02x " % struct.unpack('B', block)[0]
    print(result)

mfd.close()
