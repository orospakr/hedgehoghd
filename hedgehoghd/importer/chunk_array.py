import logging

import chunk
import kosinski

class ChunkArray(object):
    '''Array of Chunks, used by either one or two Zones.

    Owns equivalent collision indexes.
    '''
    def __init__(self, sonic2, name, data, primary_collision_index, secondary_collision_index):
        self.name = name
        self.sonic2 = sonic2
        self.primary_collision_index = primary_collision_index
        self.secondary_collision_index = secondary_collision_index

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
            self.chunks.append(chunk.Chunk(self, block_data))
