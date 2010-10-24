# HedgehogHD - Vector Graphics Platform Game Engine
# Copyright (C) 2010  Andrew Clunis <andrew@orospakr.ca>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import struct

import tile
from xmlwitch import builder

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

    def writeSVG(self, filename):
        svg = builder(version="1.0", encoding="utf-8")

        with svg.svg(**{'xmlns:dc':"http://purl.org/dc/elements/1.1/",
                        'xmlns:rdf':"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                        'xmlns:svg':"http://www.w3.org/2000/svg",
                        'xmlns':"http://www.w3.org/2000/svg",
                        'version':"1.1",
                        'width': "128",
                        'height': "128"}):

            self.toSVG(svg)

        svg_fd = open(filename, "wb")
        svg_fd.write(str(svg))
        svg_fd.close()

    def toSVG(self, xml):
        rowpos = 0
        for row in self.rows:
            columnpos = 0
            for column in row:
                with xml.g(transform="translate(%d, %d)" % (columnpos*16, rowpos*16), id="tile_c%x_%x_%x" % (self.position, columnpos, rowpos)):
                    column.toSVG(xml)
                columnpos += 1
            rowpos += 1
