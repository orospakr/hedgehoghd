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

import array
import logging
import os

import collision_tile

class CollisionArray(object):
    '''Collision Geometry Array

    As found in ``collision/Collision array N.bin``.  These arrays
    provide the 16x16 collision geometry used in all levels.

    The first array ('1') is used in the CollisionTiles and mapped
    into the Chunks.

    I am still unclear as to the role of the second array.  It appears
    to be rotated 90 CCW, and flipped horizontally.  I'm unsure of its
    purpose, as it is not used in the layout.  Perhaps it is used by
    YU2's physics, maybe proving less expensive than the unrotated
    version for certain operations?

    Contains many instances of CollisionTile.

    These are referenced through the per-zone collision layer
    CollisionIndex instances for each Chunk.
    '''

    def __init__(self, data):
        '''Create a CollisionArray object from array data in a string.'''
        arr = array.array('B', data)
        self.tiles = []
        if((len(arr) % 16) != 0):
            raise ValueError("Inappropriately sized data for a Sonic collision array: %d" % len(arr))
        number_of_tiles = len(arr) / 16
        for i in range(0, number_of_tiles):
            logging.debug("Collision array block #%x" % i)
            row = arr[i*16:(i*16) + 16]
            logging.debug(repr(row))
            self.tiles.append(collision_tile.CollisionTile(row))

    def writeSVGs(self, path):
        idx = 0
        for tile in self.tiles:
            tile.writeSVG(os.path.join(path, "%02x.svg" % idx))
            idx += 1

    def toSVG(self, xml):
        tilecount = 0
        for tile in self.tiles:
            with xml.g(id="tile_%x" % tilecount, transform="translate(%d, 0)" % ((tilecount * 16) + (tilecount * 4)),
                       style="stroke:#000000"):
                tile.toSVG(xml)
            tilecount += 1
