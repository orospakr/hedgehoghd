import logging

class Tile(object):
    '''16x16 Tile instance in a Chunk

    Contains the parameters describing the Collision, graphics Block,
    and flip properties of a given 16x16 tile in a Chuink.  These are
    not shared by any other Chunks.

    64 of which exist in a Chunk, arranged in 8x8.

    They contain:

    * horizontal and vertical flip bits
    * a reference to an artwork tile and collision block (through the
    index) by Tile ID collision solidity control bits, for the primary
    and alternate layers

    # SSTT YXII IIII IIII
    '''
    def __init__(self, chunk, tile_word):
        self.chunk = chunk
        self.alternate_collision_solidity = (tile_word & 0xC000) >> 14
        self.normal_collision_solidity = (tile_word & 0x3000) >> 12
        self.tile_index = tile_word & 0x3FF
        self.y_flipped = (tile_word & 0x800) >> 11
        self.x_flipped = (tile_word & 0x400) >> 10

        if(self.alternate_collision_solidity > 3):
            logging.error("Impossible alternate collision value in chunk?!: %d" % self.aternate_collision)
            exit(-1)
        if(self.normal_collision_solidity > 3):
            logging.error("Impossible normal collision value in chunk?!: %d" % self.normal_collision)
            exit(-1)

        # reaching back through all the references is really kinda icky,
        # should really make better encapsulation.
        self.primary_collision = None

        if(self.tile_index >= len(self.chunk.chunk_array.primary_collision_index.ids)):            
            logging.warning("Tile index greater than length of collision index asked for.  available: %d, index: %d" % (len(self.chunk.chunk_array.primary_collision_index.ids), self.tile_index))
        else:
            col_id = self.chunk.chunk_array.primary_collision_index.ids[self.tile_index]

            self.primary_collision = self.chunk.chunk_array.sonic2.coll1.tiles[col_id]
        
    def toSVG(self, xml):
        if(self.primary_collision is not None):
            colour = "000000"
            if(self.x_flipped and self.y_flipped):
                colour = "ff00ff"
            elif(self.y_flipped):
                colour = "ff0000"
            elif(self.x_flipped):
                colour = "0000ff"
            # transform="scale(%d, %d)" % (-1 if self.x_flipped else 1, -1 if self.y_flipped else 1),
            with xml.g(transform="translate(%d, %d) scale(%d, %d)" % (16 if self.x_flipped else 0, 16 if self.y_flipped else 0, -1 if self.x_flipped else 1, -1 if self.y_flipped else 1),
                       style="stroke:#%s" % colour):
                # with xml.rect(width="16", height="16", style="fill:none;stroke:#000000"):
                #     pass
                self.primary_collision.toSVG(xml)
