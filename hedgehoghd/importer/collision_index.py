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

import kosinski

class CollisionIndex(object):
    '''Per-Zone Layer Collision Index

    As found in ``collision/%s [primary,secondary] 16x16 collision
    index.bin``, Kosinski compressed.

    Per-zone indexes (Kosinski-compressed) are provided for mapping
    the 10-bit block IDs to collision block numbers.  Since there are
    256 collision blocks provided in the array (the second one not
    withstanding), each index element is one byte.  Offset in this
    index is the block number, thus providing the collision tile from
    block ID lookup functionality.

    These are usually paired to provide the "primary" and "secondary"
    collision layers for each Zone.  They are typically grouped in the
    same way as the ChunkArrays (eg., one pair shared between CPZ and
    DEZ).

    The player is moved between the primary and secondary collision layers
    when they pass through a special object, the "Path Swapper".
    '''
    def __init__(self, sonic2, data):
        self.sonic2 = sonic2
        self.ids = kosinski.decompress_string(data)
        if(len(self.ids) != 768):
            logging.error("Sonic 2 collision indexes are always 768 records (bytes) long.")
            exit(-1)
