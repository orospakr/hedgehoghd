import logging
import struct

import tile

class Chunk(object):
    '''128x128 Chunks as mapped into LevelLayouts' backgrounds and foregrounds

    As found in ``mappings/128x128/``, together in the ChunkArrays, Kosinski compressed.

    They contain a 16x16 array of Tiles.
    '''
    def __init__(self, chunk_array, block_data, position):
        self.chunk_array = chunk_array
        self.position = position
        values = struct.unpack('>64H', block_data)
        if(len(values) != 64):
            logging.error("Chunk somehow longer than 64?!")
            exit(-1)

        # Tiles
        self.rows = []

        for r in range(0, 8):
            row_offset = r * 8
            current_row = values[row_offset:row_offset+8]

            row = []
            columnpos = 0
            for column in current_row:
                row.append(tile.Tile(self, column))
                columnpos += 1
            self.rows.append(row)

    def toSVG(self, xml):
        rowpos = 0
        for row in self.rows:
            columnpos = 0
            for column in row:
                with xml.g(transform="translate(%d, %d)" % (columnpos*16, rowpos*16), id="tile_c%x_%x_%x" % (self.position, columnpos, rowpos)):
                    column.toSVG(xml)
                columnpos += 1
            rowpos += 1
