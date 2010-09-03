#!/usr/bin/env python
import sys
import array
import struct



def decompress_file(path):
    c_fd = open(sys.argv[1], "rb")
    compressed = array.array('B', c_fd.read())
    c_fd.close()
    return decompress_block(compressed)

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
        self.compressed_offset = 0
        self.uncompressed = array.array('B')

    '''Decompress compressed Kosinski data.

    data is an array of compressed data (from the array module) of bytes ('B' format string).

    If no EOS marker is present, the number of Kosinski blocks expected
    can be specified, or -1 for the usual behaviour.'''
    def decompress(self, data, count = -1):
        self.compressed = data
        self.compressed_offset = 0
        if(count == -1):
            should_continue = True
            while(should_continue):
                should_continue = self.decompressBlock()
        else:
            for i in range(0, count):
                self.decompressBlock()

    '''Decompress a block of compressed data.

    data is an optional array (from the array module) of bytes ('B' format string).

    Returns True if there should be more blocks to process, or False if
    the stream has terminated.'''
    def decompressBlock(self, compressed = None):
        compressed_offset = 0
        if(compressed is None):
            compressed = self.compressed
            compressed_offset = self.compressed_offset

        # descriptor block
        descriptor_high = reverse(compressed[compressed_offset + 0])
        descriptor_low = reverse(compressed[compressed_offset + 1])
        # compressed[2] and after are all data block

        descriptor = struct.unpack('>H', array.array('B', [descriptor_high, descriptor_low]).tostring())[0]
        print "READ BACK DESCRIPTOR: %x" % descriptor

        data_position = 0
        position = 0
        while(position < 16):
            descriptor_position = 15 - position
            print "%d:%d" % (position, descriptor_position)
            if(descriptor & (2 ** descriptor_position)):
                print "uncompressed"
                print "... appending value: 0x%x" % compressed[compressed_offset + 2 + data_position]
                self.uncompressed.append(compressed[compressed_offset + 2 + data_position])
                position += 1
                data_position += 1
            else:
                print "run-length"
                # Run-length, now to determine which type
                if(descriptor & (2 ** (descriptor_position - 1))):
                    # separate RLE
                    print "... separate RLE"
                    position += 2 # uses two inline descriptor bits
                    first_offset_byte = compressed[compressed_offset + 2 + data_position]
                    second_offset_byte = compressed[compressed_offset + 2 + data_position + 1]
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

                        third_offset_byte = compressed[compressed_offset + 2 + data_position + 2]
                        print "... third offset byte: %02x" % third_offset_byte
                        if(third_offset_byte == 0):
                            # end of stream marker!
                            print "End of stream marker found! Goodbye."
                            return False
                        copy_count = third_offset_byte + 1
                    
                    print "Okay! Separate RLE block params: offset: %d, copy_count: %d" % (offset, copy_count)

                else:
                    # inline RLE
                    print "... inline RLE"
                    first_length_bit = (descriptor & (2 ** (descriptor_position - 2))) / 2 ** (descriptor_position - 2)
                    second_length_bit = (descriptor & (2 ** (descriptor_position - 3))) / 2 ** (descriptor_position - 3)
                    print "first length bit: %d, second length bit: %d" % (first_length_bit, second_length_bit)
                    length_to_copy = (first_length_bit * 2) + (second_length_bit) + 2 # + 2 because format calls for it.
                    #                length_to_copy = ((descriptor & (2 ** descriptor_position)) * 2) + (descriptor & (2 ** descriptor_position + 3)) + 2
                    offset_to_copy_from = (compressed[compressed_offset + 2 + data_position]) - 256
                    uncompressed_src_pos = offset_to_copy_from + len(self.uncompressed)

                    print "Okay! Inline RLE block params: length_to_copy: %d, offset_to_copy_from: %d, uncompressed_src_pos: %d" % (length_to_copy, offset_to_copy_from, uncompressed_src_pos)
                
                    for i in range(0, length_to_copy):
                        current_pos_to_copy = (uncompressed_src_pos + i) % abs(offset_to_copy_from) # repeat the pattern for as many bytes as are needed
                        self.uncompressed.append(self.uncompressed[current_pos_to_copy])
                    position += 4 # inline RLE bits
                    data_position += 1 # the offset byte we read back

        # we've used the two descriptor bytes, plus whatever we've used from the data
        self.compressed_offset = 2 + data_position

        # if((len(compressed) % 16) != 0):
        #     print "Not a valid Kosinski compressed file.  Length should be a multiple of 16."
        #     exit(-1)
    
        # continue
        return True

#while(True):
    # read back


#descriptor_high, descriptor_low = struct.unpack('B', descriptor)

#print "H: %02x L: %02x" % (descriptor_high, descriptor_low)

# OOZ_1.bin should be 844dcc5e3a58902c16a682ae22c800d7dd3158cb
if __name__ == '__main__':
    import hashlib
    result = decompress_file(sys.argv[1])
    print hashlib.sha1(result.tostring()).hexdigest()

