#!/usr/bin/env python

import array
import logging
import os.path
import struct

import kosinski


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
        if((len(arr) % 16) != 0):
            raise ValueError("Inappropriately sized data for a Sonic collision array: %d" % len(arr))
        number_of_tiles = len(arr) / 16
        for i in range(0, number_of_tiles):
            row = arr[i*16:(i*16) + 16]
            logging.debug("Collision array block #%d" % i)

            for column_byte in row:
                bits = (0b11100000 & column_byte)
                if(bits != 0xe0):
                    # counted from bottom
                    height = (0b00011111 & column_byte)
                else:
                    # counted from top.
                    anti_height = (0b00011111 & column_byte) - 16

class CollisionIndex(object):
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

class Zone(object):
    '''A Zone!
    '''
    def __init__(self, sonic2):
        # load LevelMaps from level/layout for each act
        logging.info("Loading %s Zone..." % self.title)
        self.act_layouts = []
        if(self.acts == 1):
            # only one act, disasm names them directly.
            fd = open(os.path.join(sonic2.s2_split_disassembly_dir, "level", "layout", "%s.bin" % self.code), "rb")
            self.act_layouts[0] = LevelLayout(sonic2.chunk_arrays[self.chunk_array], fd.read())
            fd.close()
        else:
            for act in range(0, self.acts):
                logging.info("... Act %d" % (act + 1))
                fd = open(os.path.join(sonic2.s2_split_disassembly_dir, "level", "layout", "%s_%d.bin" % (self.code, act + 1)), "rb") # acts are named from 1
                self.act_layouts.append(LevelLayout(sonic2.chunk_arrays[self.chunk_array], fd.read()))
                fd.close()

class EmeraldHillZone(Zone):
    acts = 2
    title = "Emerald Hill"
    code = "EHZ"
    chunk_array = "EHZ_HTZ"

class ChunkArray(object):
    '''Array of Chunks, used by either one or two Zones.
    '''
    def __init__(self, data):
        bm = kosinski.decompress_string(data).tostring()

        if((len(bm) % 128) != 0):
            logging.error("Inappropriately sized level map: %d" % bmfs)
            exit(-1)

        blocks = len(bm) / 128

        logging.debug("There are %d blocks in this ChunkArray." % blocks)

        self.chunks = []
        chunk_no = 0
        for block in range(0, blocks):
            logging.debug("... chunk %d: " % chunk_no)
            chunk_no += 1
            block_data = bm[block*128:(block*128) + 128]
            self.chunks.append(Chunk(block_data))

class Tile(object):
    '''16x16 Tile

    64 of which exist in a Chunk, arranged in 8x8.

    They contain:

    * horizontal and vertical flip bits
    * a reference to an artwork tile and collision block by Block ID
    * collision solidity control bits, for the primary and alternate layers    
    '''
    def __init__(self, tile_word):
        self.alternate_collision = (tile_word & 0xC000) >> 14
        self.normal_collision = (tile_word & 0x3000) >> 12
        self.tile_index = tile_word & 0x3FF
        self.y_flipped = (tile_word & 800)
        self.x_flipped = (tile_word & 400)

        if(self.alternate_collision > 3):
            logging.error("Impossible alternate collision value in chunk?!: %d" % self.aternate_collision)
            exit(-1)
        if(self.normal_collision > 3):
            logging.error("Impossible normal collision value in chunk?!: %d" % self.normal_collision)
            exit(-1)    
        
        # TODO. do lookup in collision index for associated act and
        # get collisiontile.

class Chunk(object):
    '''128x128 Chunks as mapped into LevelLayouts' backgrounds and foregrounds

    As found in ``mappings/128x128/``, Kosinski compressed.

    They are arranged as a matrix of 16x16 pixel blocks, represented
    by the Tile class.
    '''
    def __init__(self, block_data):
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
                self.tiles.append(Tile(column))
            
class CollisionTile(object):
    '''16x16 Collision Shape Tile

    They effectively draw a bitmapped line with a value per column (they
    cannot contain an arbitrary 16x16 bitmap), with bits that determine
    whether the solid piece is above or below the specified height.
    '''
    def __init__(self, data):
        pass

class Sonic2(object):
    def __init__(self, s2_split_disassembly_dir):
        self.s2_split_disassembly_dir = s2_split_disassembly_dir
        if not os.path.isdir(s2_split_disassembly_dir):
            raise Exception("%s: invalid Sonic 2 split disassembly directory!" % s2_split_disassembly_dir)
        print "Loading Sonic 2 game data."

        logging.info("Loading Collision Arrays...")
        logging.info("... 1")
        coll1_fd = open(os.path.join(s2_split_disassembly_dir, "collision", "Collision array 1.bin"), "rb")
        self.coll1 = CollisionArray(coll1_fd.read())
        coll1_fd.close()

        logging.info("... 2")
        coll2_fd = open(os.path.join(s2_split_disassembly_dir, "collision", "Collision array 2.bin"), "rb")
        self.coll2 = CollisionArray(coll2_fd.read())
        coll2_fd.close()

        self.chunk_arrays = {}

        for cname in ["ARZ", "CNZ", "CPZ_DEZ", "EHZ_HTZ", "MCZ", "OOZ", "MTZ", "WFZ_SCZ"]:
            self.loadChunkArray(cname)
        
        self.ehz = EmeraldHillZone(self)

        # TODO instantiate each Zone, which will itself instantiate each act
        # they will look up chunks in the chunkarrays above.

    def loadChunkArray(self, name):
        logging.info("Loading 128x128 chunk array for: %s" % name)
        chunk_fd = open(os.path.join(self.s2_split_disassembly_dir, "mappings", "128x128", "%s.bin" % name), "rb")
        self.chunk_arrays[name] = ChunkArray(chunk_fd.read())
