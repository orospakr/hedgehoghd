import kosinski

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
    def __init__(self, sonic2, data):
        self.sonic2 = sonic2
        self.ids = kosinski.decompress_string(data)
