import array
import logging

import kosinski

class LevelLayout(object):
    '''A Level's 128x16x2 Layout Map

    As found in level/layout/, Kosinski compressed.  There is one for
    each Zone Act.

    There are 128 columns, 16 rows, and 2 layers, foreground and
    background.  They are arranged as a sequence of rows, with
    foreground and background interleaved.  Each 1-byte cell addresses
    a 128x128 block out of the 256 available from the ChunkArray
    assigned to this Zone.
    '''
    def __init__(self, chunk_array, data):
        self.chunk_array = chunk_array
        bytemap = kosinski.decompress_string(data).tostring()

        if((len(bytemap) % 128) != 0):
            logging.error("Inappropriately sized level map: %d" % mfs)
            exit(-1)

        self.foreground = []
        self.background = []

        for y in range(0, len(bytemap) / 128):
            row_data = bytemap[y*128:(y*128)+128]
            if(len(row_data) != 128):
                logging.error("Level layout row with length not 128?!: %d" % len(row_data))
                exit(-1)
            block_ids = array.array('B', row_data)
            row = []
            for block_id in block_ids:
                row.append(self.chunk_array.chunks[block_id])
            if((y % 2) == 0):
                self.foreground.append(row)
            else:
                self.background.append(row)

    def toSVG(self, xml):
        rowpos = 0
        for row in self.foreground:
            chunkpos = 0
            for chunk in row:
                with xml.g(transform="translate(%d, %d)" % (chunkpos * 128, rowpos * 128)):
                    chunk.toSVG(xml)
                # with xml.rect(transform="translate(%d, %d)" % (chunkpos * 128, rowpos * 128),
                #               width="128", height="128", x="0", y="0", id="chunk_%d_%d" % (chunkpos, rowpos)):
                #     pass
                chunkpos += 1
            rowpos += 1
