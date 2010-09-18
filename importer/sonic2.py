#!/usr/bin/env python

import os.path

import kosinski

'''A Level's 128x16x2 Layout Map.

As found in level/layout/, Kosinski compressed.

It has a foreground and background layer.  They are interlaced at the row level.

There is one for each Zone Act.
'''
class LevelLayout(object):
    pass

'''128x128 Blocks as mapped into LevelLayouts' backgrounds and foregrounds.

As found in mappings/128x128/, Kosinski compressed.

They are arranged as a matrix of 16x16 pixel blocks.

For each position in that matrix, there are:

* horizontal and vertical flip bits
* a reference to an artwork tile
* 'primary' and 'alternate' references to two collision blocks.  I still don't
quite understand the functions of these.  Perhaps something to do with constructs like loops that seem to do a "handoff"?
'''
class Block(object):
    pass

'''16x16 collision shape tile.

As found in collision/.  There appear to be two common collision arrays that are *not* Kosinski compressed, and then supplemental "indexes" that are used by specific levels that are Kosinski compressed.  The supplemental arrays seem to be split into "primary" and "secondary" components, which may be related to the "primary" and "alternate" collision block references in the Blocks.  I am not yet sure what their function is, but decompressed they are always 768 bytes.  Off_Colp in disasm is the label for the table of pointers to these indexes.

They effectively draw a bitmapped line with a value per column (they cannot contain an arbitrary 16x16 bitmap), with bits that determine whether the solid piece is above or below the specified height.
'''
class CollisionTile(object):
    pass
    

class Sonic2(object):
    def __init__(self, split_disassembly_dir):
        if not os.path.isdir(split_disassembly_dir):
            raise Exception("Invalid Sonic 2 split disassembly directory!")
        print "Loading Sonic 2 game data."
        
        # 128x128 block 
