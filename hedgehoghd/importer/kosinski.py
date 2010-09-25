#!/usr/bin/env python
import sys
import array
import struct
import logging

def reverse(byte):
    if(byte > 0xff):
        logging.error("That isn't a byte: %d" % byte)
        exit(-1)
    result = 0
    for i in range(0, 8):
        bit = (byte & (2 ** i)) / (2 ** i)
        result += bit * (2 ** (7-i))
    return result

class Kosinski(object):
    '''Kosinski decompressor object.

    Use the convenience functions in this module for actually using it.'''

    def decompress(self, compressed):
        '''Decompress Kosinski compressed data.

        `data` is an optional array (from the array module) of bytes ('B' format string).
        '''
        self.uncompressed = array.array('B')

        # offset to current descriptor block
        self.compressed_offset = 0

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
            self.compressed_offset += 2
            logging.debug("READ BACK DESCRIPTOR: %x" % self.descriptor)

        def read_descriptor_bit():
            logging.debug("%d:" % (self.position))
            bit = (self.descriptor & (2** (15 - self.position))) / 2 ** (15 - self.position)
            self.position += 1
            if(self.position == 16):
                logging.debug("Position is 16, loading new descriptor.")
                read_new_descriptor()
                self.position = 0
            return bit

        read_new_descriptor()

        # iterate forever over descriptor bits.  they are reloaded every time all 16 bits are consumed,
        # either if they are used up normally, or when an RLE descriptor is split between two
        while(True):
            first_bit = read_descriptor_bit()
            if(first_bit):
                logging.debug("uncompressed")
                logging.debug("... appending value: 0x%x" % compressed[self.compressed_offset])
                self.uncompressed.append(compressed[self.compressed_offset])
                self.compressed_offset += 1
            else:
                logging.debug("run-length")
                # Run-length, now to determine which type
                if(read_descriptor_bit()):
                    # separate RLE
                    logging.debug("... separate RLE")
                    first_offset_byte = compressed[self.compressed_offset]
                    second_offset_byte = compressed[self.compressed_offset + 1]
                    logging.debug("... first offset byte: %02x, second: %02x" % (first_offset_byte, second_offset_byte))

                    base_offset = first_offset_byte
                    factor256 = (second_offset_byte & 0xF8) / 2 ** 3
                    offset = -8192 + (factor256 * 256) + base_offset
#                    offset = 0xFFFFE000 | ((0xF8 & second_offset_byte) << 5) | first_offset_byte

                    copy_count = None
                    if(second_offset_byte & 0x7):
                        logging.debug("... with two bytes of parameters")
                        # [LLLL LLLL] [HHHH HCCC]
                        # -8192 + HHHHH * 256 + LLLLLLLL, copy_length = CCC + 2
                        copy_count = (second_offset_byte & 0x07) + 2
                        self.compressed_offset += 2
                    else:
                        logging.debug("... with three bytes of parameters")
                        # [LLLL LLLL] [HHHH H000] [CCCC CCCC]
                        # -8192 + HHHHH * 256 + LLLLLLLL, copy_length = CCCCCCCC + 2

                        third_offset_byte = compressed[self.compressed_offset + 2]
                        logging.debug("... third offset byte: %02x" % third_offset_byte)
                        if(third_offset_byte == 0):
                            # end of stream marker!
                            logging.debug("End of stream marker found! Goodbye.")
                            return self.uncompressed
                        elif(third_offset_byte == 1):
                            logging.warn("Description block self-terminator found.  Not implemented!")
                            exit(-1)
                        copy_count = third_offset_byte + 1
                        self.compressed_offset += 3

                    logging.debug("Okay! Separate RLE block params: offset: %d, copy_count: %d" % (offset, copy_count))

                    if((offset * -1) > len(self.uncompressed)):
                        logging.debug("What?  Separate RLE is asking for an offset past the beginning of the uncompressed data?! offset: %d, available uncompressed length: %d" % (offset, len(self.uncompressed)))
                        exit(-1)

                    uncompressed_src_pos = offset + len(self.uncompressed)

                    for i in range(0, copy_count):
                        current_pos_to_copy = uncompressed_src_pos + i
                        logging.debug("current_pos_to_copy: %d, available_length: %d" % (current_pos_to_copy, len(self.uncompressed)))
                        logging.debug("... appending value (separate): 0x%x" % self.uncompressed[current_pos_to_copy])
                        self.uncompressed.append(self.uncompressed[current_pos_to_copy])

                else:
                    # inline RLE
                    logging.debug("... inline RLE")
                    first_length_bit = read_descriptor_bit()
                    second_length_bit = read_descriptor_bit()
                    logging.debug("first length bit: %d, second length bit: %d" % (first_length_bit, second_length_bit))
                    length_to_copy = (first_length_bit * 2) + (second_length_bit) + 2 # + 2 because format calls for it.
                    offset_to_copy_from = (compressed[self.compressed_offset]) - 256
                    uncompressed_src_pos = offset_to_copy_from + len(self.uncompressed)

                    logging.debug("Okay! Inline RLE block params: length_to_copy: %d, offset_to_copy_from: %d, uncompressed_src_pos: %d" % (length_to_copy, offset_to_copy_from, uncompressed_src_pos))

                    if((offset_to_copy_from * -1) > len(self.uncompressed)):
                           logging.error("What? Inline RLE is asking for an offset past the beginning of the uncompressed data?! offset: %d, available uncompressed data: %d" % (offset_to_copy_from, len(self.uncompressed)))
                           exit(-1)

                    logging.debug("length of uncompressed: %d" % len(self.uncompressed))
                    for i in range(0, length_to_copy):

                        current_pos_to_copy = uncompressed_src_pos + i # repeat the pattern for as many bytes as are needed -- note this ends up reading back bytes appended on prior loops

                        logging.debug("current_pos_to_copy: %d" % current_pos_to_copy)
                        logging.debug("... appending value (inline): 0x%x" % self.uncompressed[current_pos_to_copy])
                        self.uncompressed.append(self.uncompressed[current_pos_to_copy])
                    # self.position += 4 # inline RLE bits
                    self.compressed_offset += 1 # the offset byte we read back
        return uncompressed

def decompress_file(path):
    '''Decompress Kosinski data in a file.
    
    Returns an array.array('B') of the decompressed data.'''
    c_fd = open(sys.argv[1], "rb")
    compressed = array.array('B', c_fd.read())
    c_fd.close()
    kos = Kosinski()
    return kos.decompress(compressed)


def decompress_string(data):
    '''Decompress Kosinski data in a string.

    Returns an array.array('B') of the decompressed data.'''
    kos = Kosinski()
    return kos.decompress(array.array('B', data))

def decompress_array(arr):
    '''Decompress Kosinski data in an array.array('B').

    Returns an array.array('B') of the decompressed data.'''
    kos = Kosinski()
    return kos.decompress(arr)

if __name__ == '__main__':
    import hashlib
    result = decompress_file(sys.argv[1])
    print hashlib.sha1(result.tostring()).hexdigest()
    print "size: %d" % len(result)
    f = open(sys.argv[2], "wb")
    f.write(result)
    f.close()
