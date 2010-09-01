#!/usr/bin/env python

# attempt at porting libkens' Kosinski decompressor to Python.
# doesn't work at all.

import sys
import struct
import array

import hashlib

c_fd = open(sys.argv[1], "rb")


uncompressed = array.array('B')

#	fseek(Src, Location, SEEK_SET);

	# if (Moduled)
	# {
	# 	fread(&High, 1, 1, Src);
	# 	fread(&Low, 1, 1, Src);
	# 	FullSize = ((long)High << 8) + (long)Low;
	# }

# start:


BITFIELD = 0
def read_word():
    val = c_fd.read(2)
    if(len(val) != 2):
        print "Not enough data left to read a word!"
        exit(-1)
    return struct.unpack('<H', val)[0]

def read_byte():
    val = c_fd.read(1)
    if(len(val) != 1):
        print "Not enough data left to read a byte!"
        exit(-1)
    return struct.unpack('B', val)[0]

BFP = 0
Bit = 0
Byte = 0
Low = 0
High = 0
Pointer = 0
Count = 0
Offset = 0
FullSize = 0
DecBytes = 0


# ------------------------------------------------------------------------------------------------
while(True):
#    print "GO!"
    if(BITFIELD & (1<<BFP)):
        Bit=1
    else:
        Bit=0
    BFP += 1
    if (BFP>=16):
        BITFIELD = read_word()
        BFP=0

# -- Direct Copy ---------------------------------------------------------------------------------
    if (Bit):
        print "Direct Copy!"
        Byte = read_byte()
        uncompressed.fromstring(struct.pack('B', Byte))
        DecBytes+=1

    else:
        if(BITFIELD & (1<<BFP)):
            Bit=1
        else:
            Bit=0
        BFP += 1
        if (BFP>=16):
            BITFIELD = read_word()
            BFP=0
# -- Embedded / Separate RLE ---------------------------------------------------------------------
        if (Bit):
            print "Embedded/Separate"
            Low = read_byte()
            High = read_byte()
#            fread(&Low, 1, 1, Src);
#            fread(&High, 1, 1, Src);

            Count= High & 0x07

            if (Count==0):
                Count = read_byte()
                if (Count==0):
                    # finished
                    print "Huh, empty Kosinksi file? (or next module, or something)"
                    break
                
                if (Count==1):
                    print "Count 1, apparently iterate again..."
                    continue
            else:
                Count+=1
        
            Offset = 0xFFFFE000 | ((0xF8 & High) << 5) | Low
  
# -- Inline RLE -----------------------------------------------------------------------------------
        else:
            print "Inline!"
            if(BITFIELD & (1<<BFP)):
                Low=1
            else:
                Low=0
            BFP += 1
            if (BFP>=16):
                BITFIELD = read_word()
                BFP=0
            if(BITFIELD & (1<<BFP)):
                High=1
            else:
                High=0
            BFP += 1
            if (BFP>=16):
                BITFIELD = read_word()
                BFP=0

                Count = (Low)*2 + (High) + 1
                # EOF seems to get noticed here.  original code seems to do nothing.
                # how the fuck does the original code even realize that its time to terminate...?
                Offset = read_byte()
                Offset |= 0xFFFFFF00
        # read a byte from uncompressed data at Offset from current pos
        # return uncompressed data to current position
        # write that byte to the current uncompressed position. (incremement currentpos)
        for i in range(0, Count):
            source_pos = (len(uncompressed) - 1) + Offset + i
            print "Attempting to get value from %d, current length is %d" % (source_pos, len(uncompressed))
            uncompressed.append(uncompressed[source_pos])

        DecBytes+=Count+1
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------

print "ALL DONE!"

print hashlib.sha1sum(uncompressed.tostring()).hexdigest()
# end:
	# if (Moduled)
	# {
	# 	if (DecBytes < FullSize)
	# 	{
	# 		do { fread(&Byte, 1, 1, Src); } while (Byte==0);
	# 		fseek(Src, -1, SEEK_CUR);
	# 		goto start;
	# 	}
	# }
# fclose(Dst);
c_fd.close()
