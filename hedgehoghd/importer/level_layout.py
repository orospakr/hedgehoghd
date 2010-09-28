import array
import logging

import kosinski

class LevelLayout(object):
    '''A Level's 128x16x2 Layout Map

    As found in level/layout/, Kosinski compressed.

    It has a foreground and background layer.  They are interlaced at the
    row level.

    There is one for each Zone Act.
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
