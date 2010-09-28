import logging

class Tile(object):
    '''16x16 Tile

    64 of which exist in a Chunk, arranged in 8x8.

    They contain:

    * horizontal and vertical flip bits
    * a reference to an artwork tile and collision block by Block ID
    * collision solidity control bits, for the primary and alternate layers    
    '''
    def __init__(self, chunk, tile_word):
        self.chunk = chunk
        self.alternate_collision_idx = (tile_word & 0xC000) >> 14
        self.normal_collision_idx = (tile_word & 0x3000) >> 12
        self.tile_index = tile_word & 0x3FF
        self.y_flipped = (tile_word & 800)
        self.x_flipped = (tile_word & 400)

        if(self.alternate_collision_idx > 3):
            logging.error("Impossible alternate collision value in chunk?!: %d" % self.aternate_collision)
            exit(-1)
        if(self.normal_collision_idx > 3):
            logging.error("Impossible normal collision value in chunk?!: %d" % self.normal_collision)
            exit(-1)

        # reaching back through all the references is really kinda icky,
        # should really make better encapsulation.
#        if(self.alternate_collision_idx != 0):
#            self.alternate_collision = self.chunk.chunk_array.secondary_collision_index.ids[self.alternate_collision_idx]

        self.primary_collision = self.chunk.chunk_array.sonic2.coll1.tiles[self.chunk.chunk_array.primary_collision_index.ids[self.normal_collision_idx]]
        
        # TODO. do lookup in collision index for associated act and
        # get collisiontile.
