import logging
import struct

import tile

class Chunk(object):
    '''128x128 Chunks as mapped into LevelLayouts' backgrounds and foregrounds

    As found in ``mappings/128x128/``, Kosinski compressed.

    They are arranged as a matrix of 16x16 pixel blocks, represented
    by the Tile class.
    '''
    def __init__(self, chunk_array, block_data):
        self.chunk_array = chunk_array
        values = struct.unpack('64H', block_data)
        if(len(values) != 64):
            logging.error("Chunk somehow longer than 64?!")
            exit(-1)
        self.tiles = []

        for r in range(0, 8):
            row_offset = r * 8
            current_row = values[row_offset:row_offset+8]

            # SSTT YXII IIII IIII
            for column in current_row:
                self.tiles.append(tile.Tile(self, column))