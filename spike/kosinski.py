#!/usr/bin/env python
import sys
import array
import struct





def reverse(byte):
    if(byte > 0xff):
        print "That isn't a byte: %d" % byte
        exit(-1)
    result = 0
    for i in range(0, 8):
        bit = (byte & (2 ** i)) / (2 ** i)
        result += bit * (2 ** (7-i))
    return result

class Kosinski(object):
    def __init__(self):
#        self.compressed_offset = 0
#        self.uncompressed = array.array('B')
        pass

    # '''Decompress compressed Kosinski data.

    # data is an array of compressed data (from the array module) of bytes ('B' format string).

    # If no EOS marker is present, the number of Kosinski blocks expected
    # can be specified, or -1 for the usual behaviour.'''
    # def decompress(self, data, count = -1):
    #     self.compressed = data
    #     self.compressed_offset = 0
    #     if(count == -1):
    #         should_continue = True
    #         while(should_continue):
    #             should_continue = self.decompressBlock()
    #     else:
    #         for i in range(0, count):
    #             self.decompressBlock()

    '''Decompress Kosinski compressed data.

    data is an optional array (from the array module) of bytes ('B' format string).

#    Returns True if there should be more blocks to process, or False if
#    the stream has terminated.'''
    def decompress(self, compressed = None):
        
        self.uncompressed = array.array('B')
#        if(compressed is None):
#            compressed = self.compressed
#            compressed_offset = self.compressed_offset

        # descriptor block
#        descriptor_high = reverse(compressed[compressed_offset + 0])
#        descriptor_low = reverse(compressed[compressed_offset + 1])
        # compressed[2] and after are all data block

        # offset to current descriptor block
        self.compressed_offset = 0
        
        # cursor that we're reading from in the data ('B') part of the current block.  it's an offset from the end of the two descriptor bytes
        self.data_position = 0

        # our current position in the descriptor.  descriptor_position is merely the inverse of this
        # so we can deal with the 'reverse' arrangement of the descriptor.
        self.position = 0

        # contains the 16-bit value of the current descriptor.
        self.descriptor = None

        # read a new descriptor back from the current compressed_offset.
        def read_new_descriptor():
            descriptor_high = reverse(compressed[self.compressed_offset + 0])
            descriptor_low = reverse(compressed[self.compressed_offset + 1])
            self.descriptor = struct.unpack('>H', array.array('B', [descriptor_high, descriptor_low]).tostring())[0]
            self.position = 0

            print "READ BACK DESCRIPTOR: %x" % self.descriptor

        # prime ourselves with the first descriptor.
        read_new_descriptor()
        self.used_bytes = 2

        # iterate forever over descriptor bits.  they are reloaded every time all 16 bits are consumed,
        # either if they are used up normally, or when an RLE descriptor is split between two
        while(True):
            if(self.position >= 16):
                print "Cleanly beginning a new descriptor block!  Bytes used on last one: %d" % self.used_bytes
                self.compressed_offset += self.used_bytes
                read_new_descriptor()
                self.data_position = 0
                self.used_bytes = 2

            descriptor_position = 15 - self.position

            # bytes that have been consumed from the compressed_data
            
            print "%d:%d" % (self.position, descriptor_position)
            if(self.descriptor & (2 ** descriptor_position)):
                print "uncompressed"
                print "... appending value: 0x%x" % compressed[self.compressed_offset + 2 + self.data_position]
                self.uncompressed.append(compressed[self.compressed_offset + 2 + self.data_position])
                self.position += 1
                self.data_position += 1
                self.used_bytes += 1
            else:
                print "run-length"
                # Run-length, now to determine which type
                if(self.descriptor & (2 ** (descriptor_position - 1))):
                    # separate RLE
                    print "... separate RLE"
                    self.position += 2 # uses two inline descriptor bits
                    first_offset_byte = compressed[self.compressed_offset + 2 + self.data_position]
                    second_offset_byte = compressed[self.compressed_offset + 2 + self.data_position + 1]
                    print "... first offset byte: %02x, second: %02x" % (first_offset_byte, second_offset_byte)
                    
                    base_offset = first_offset_byte
                    factor256 = (second_offset_byte & 0xF8) / 2 ** 3
                    offset = -8192 + (factor256 * 256) + base_offset

                    copy_count = None
                    if(second_offset_byte & 0x7):
                        print "... with two bytes of parameters"
                        # [LLLL LLLL] [HHHH HCCC]
                        # -8192 + HHHHH * 256 + LLLLLLLL, copy_length = CCC + 2
                        copy_count = (second_offset_byte & 0x07) + 2
                    else:
                        print "... with three bytes of parameters"
                        # [LLLL LLLL] [HHHH H000] [CCCC CCCC]
                        # -8192 + HHHHH * 256 + LLLLLLLL, copy_length = CCCCCCCC + 2

                        third_offset_byte = compressed[self.compressed_offset + 2 + self.data_position + 2]
                        print "... third offset byte: %02x" % third_offset_byte
                        if(third_offset_byte == 0):
                            # end of stream marker!
                            print "End of stream marker found! Goodbye."
                            return self.uncompressed
                        elif(third_offset_byte == 1):
                            print "Description block self-terminator found.  Start again!"
                        copy_count = third_offset_byte + 1
                    
                    print "Okay! Separate RLE block params: offset: %d, copy_count: %d" % (offset, copy_count)

                else:
                    # inline RLE
                    print "... inline RLE"
                    if(descriptor_position == 1):
                        # ugh, I don't know why they bothered with this.
                        print "oh man, the two length bits of the inline RLE descriptor are IN THE NEXT DESCRIPTOR BLOCK, argh"
#                        read_new_descriptor()
#                        self.position
                    flb_mask = (2 ** (descriptor_position - 2))
                    print "FLB MASK: %f, descriptor_position: %d" % (flb_mask, descriptor_position)
                    first_length_bit = (self.descriptor & flb_mask) / 2 ** (descriptor_position - 2)
                    second_length_bit = (self.descriptor & (2 ** (descriptor_position - 3))) / 2 ** (descriptor_position - 3)
                    print "first length bit: %d, second length bit: %d" % (first_length_bit, second_length_bit)
                    length_to_copy = (first_length_bit * 2) + (second_length_bit) + 2 # + 2 because format calls for it.
                    #                length_to_copy = ((descriptor & (2 ** descriptor_position)) * 2) + (descriptor & (2 ** descriptor_position + 3)) + 2
                    offset_to_copy_from = (compressed[self.compressed_offset + 2 + self.data_position]) - 256
                    uncompressed_src_pos = offset_to_copy_from + len(self.uncompressed)

                    print "Okay! Inline RLE block params: length_to_copy: %d, offset_to_copy_from: %d, uncompressed_src_pos: %d" % (length_to_copy, offset_to_copy_from, uncompressed_src_pos)
                
                    for i in range(0, length_to_copy):
                        current_pos_to_copy = (uncompressed_src_pos + i) % abs(offset_to_copy_from) # repeat the pattern for as many bytes as are needed
                        self.uncompressed.append(self.uncompressed[current_pos_to_copy])
                    self.position += 4 # inline RLE bits
                    self.data_position += 1 # the offset byte we read back
                    self.used_bytes += 1

        # if((len(compressed) % 16) != 0):
        #     print "Not a valid Kosinski compressed file.  Length should be a multiple of 16."
        #     exit(-1)
            
    
        # continue
        return uncompressed

#while(True):
    # read back


#descriptor_high, descriptor_low = struct.unpack('B', descriptor)

#print "H: %02x L: %02x" % (descriptor_high, descriptor_low)

# OOZ_1.bin should be 844dcc5e3a58902c16a682ae22c800d7dd3158cb

def decompress_file(path):
    c_fd = open(sys.argv[1], "rb")
    compressed = array.array('B', c_fd.read())
    c_fd.close()
    kos = Kosinski()
    kos.decompress(compressed)
    return kos.uncompressed

if __name__ == '__main__':
    import hashlib
    result = decompress_file(sys.argv[1])
    print hashlib.sha1(result.tostring()).hexdigest()

