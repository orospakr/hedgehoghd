import unittest
import array
import spike.kosinski

class KosinskiTest(unittest.TestCase):
    def setUp(self):
        self.kos = spike.kosinski.Kosinski()

    def testByteReverse(self):
        # 11110000 -> 00001111
        self.assertEquals(0x0F, spike.kosinski.reverse(0xF0))
        # 10101010 -> 01010101
        self.assertEquals(0x55, spike.kosinski.reverse(0xAA))

    def testAllUncompressed(self):
        self.kos.decompressBlock(array.array('B',[0xff, 0xff, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]))

        self.assertEquals([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f], self.kos.uncompressed.tolist())

    def testSimpleInlineRLE(self):
        # the original inline RLE example given on Sega Retro (http://www.segaretro.org/Kosinski_compression) appears to have an extra
        # byte, giving 12 uncompressed bytes after the inline RLE run of 0x25.  However, there are only 11 more descriptor bits left, thus only
        # indicating 11 bits.  I have removed the extra byte, since it appears to have been erroneous.

        self.kos.decompressBlock(array.array('B',[0xF1, 0xFF, 0x25, 0xFF, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B]))

        self.assertEquals([0x25, 0x25, 0x25, 0x25, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B], self.kos.uncompressed.tolist())

    # rather than decompressing only a single block, verify that we can process a stream of blocks and notice when it ends
    # 0x02, 0x00 (descriptor with only a 01 separate RLE indicator) followed by three null bytes (null separate RLE indicator which means EOS) is a simple byte-aligned EOS
    def testStream(self):
        self.kos.decompress(array.array('B',[0xF1, 0xFF, 0x25, 0xFF, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x02, 0x00, 0x00, 0x00, 0x00]), -1)
        self.assertEquals([0x25, 0x25, 0x25, 0x25, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B], self.kos.uncompressed.tolist())

    # def testStreamWithSeparateRLE(self):
    #     self.kos.decompress[FF 3F 54 3B C4 44 54 33 33 5B 2D 5C 44 5C C4 C5 FC 15 FE C3 44 78 88 98 44 30 FF FF 00 F8 00]

    #     [54 3B C4 44 54 33 33 5B 2D 5C 44 5C C4 C5 C4 C5 C3 44 78 88 98 44 30 30 30 30 30 30 30 30 30 30]

