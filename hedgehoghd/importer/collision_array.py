import array
import logging

import collision_tile

class CollisionArray(object):
    '''Collision Geometry Array

    As found in ``collision/Collision array N.bin``.  These arrays provide
    the 16x16 collision geometry used in all levels.  I am still unclear
    as to the role of the second array.  Comments in the annotated
    disassembly suggest that it is rotated.  It does *not* appear to have
    to do with the distinction between "primary" and "secondary" collision
    layers.

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
            logging.debug("Collision array block #%d" % i)
            row = arr[i*16:(i*16) + 16]
            self.tiles.append(collision_tile.CollisionTile(row))

    def toSVG(self, xml):
        tilecount = 0
        for tile in self.tiles:
            with xml.g(id="tile_%x" % tilecount, transform="translate(%d, 0)" % (tilecount * 16),
                       style="stroke:#000000"):
                tile.toSVG(xml)
            tilecount += 1
