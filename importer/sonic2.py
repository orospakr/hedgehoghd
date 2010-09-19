#!/usr/bin/env python

import os.path

import kosinski

'''Collision Geometry Array

As found in ``collision/Collision array N.bin``.  These arrays provide
the 16x16 collision geometry used in all levels.  I am still unclear
as to the role of the second array.  Comments in the annotated
disassembly suggest that it is rotated.  It does *not* appear to have
to do with the distinction between "primary" and "secondary" collision
layers.

Contains many instances of CollisionTile_.

These are referenced through the per-zone collision layer
CollisionIndex_ instances for each Chunk_.
'''
class CollisionArray(object):
    def __init__(self, data):
        if((len(data) % 16) != 0):
            raise ValueError("Inappropriately sized data for a Sonic collision array: %d" % len(data))
        number_of_tiles = len(data) / 16
        for i in range(0, number_of_tiles):
            row = data

'''Per-Zone Layer Collision Index

Per-zone indexes (Kosinski-compressed) are provided for mapping the
10-bit block IDs to collision block numbers.  Since there are 256
collision blocks provided in the array (the second one not
withstanding), each index element is one byte.  Offset in this index
is the block number, thus providing the collision tile from block ID
lookup functionality.

These are usually paired to provide the "primary" and "secondary"
collision layers for each Zone.  Note that some pairs are shared
between several zones.

'''
class CollisionIndex(object):
    pass

'''A Level's 128x16x2 Layout Map

As found in level/layout/, Kosinski compressed.

It has a foreground and background layer.  They are interlaced at the
row level.

There is one for each Zone Act.
'''
class LevelLayout(object):
    pass

'''A Zone!
'''
class Zone(object):
    pass

'''128x128 Chunks as mapped into LevelLayouts' backgrounds and foregrounds

As found in ``mappings/128x128/``, Kosinski compressed.

They are arranged as a matrix of 16x16 pixel blocks.

For each position in that matrix, there are:

* horizontal and vertical flip bits

* a reference to an artwork tile and collision block by Block ID

* collision solidity control bits, for the primary and alternate
  layers
'''
class Chunk(object):
    pass

'''16x16 Collision Shape Tile

They effectively draw a bitmapped line with a value per column (they
cannot contain an arbitrary 16x16 bitmap), with bits that determine
whether the solid piece is above or below the specified height.
'''
class CollisionTile(object):
    def __init__(self, data):
        pass

class Sonic2(object):
    def __init__(self, split_disassembly_dir):
        if not os.path.isdir(split_disassembly_dir):
            raise Exception("Invalid Sonic 2 split disassembly directory!")
        print "Loading Sonic 2 game data."
        
        # 128x128 block 
