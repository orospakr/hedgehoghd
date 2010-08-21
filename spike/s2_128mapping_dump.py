#!/usr/bin/env python

import sys
import os
import struct

if(len(sys.argv) != 2):
    print("usage: %s <sonic 2 128x128 block mapping>" % sys.argv[0])
    exit(-1)

mfn = sys.argv[1]
mfs = os.stat(mfn).st_size

mfd = open(mfn, "rb")

if((mfs % 128) != 0):
    print("Inappropriately sized 128x128 block mapping: %d" % mfs)

print "There are %d rows." % (mfs / 128)

# 256 rows for both EHZ and HTZ
# 128 rows per zone
# 64 rows per act, so 32 (0x20) actual rows (foreground/background interlacing
# so, the problem is that I was assuming.

skip = False

for y in range(0, mfs / 128):
    row = mfd.read(128)
    result = ""
    for block in row:
        result += "%02x " % struct.unpack('B', block)[0]
    print result


mfd.close()
