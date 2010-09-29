class CollisionTile(object):
    '''16x16 Collision Shape Tile

    They effectively draw a bitmapped line with a value per column (they
    cannot contain an arbitrary 16x16 bitmap), with bits that determine
    whether the solid piece is above or below the specified height.
    '''
    def __init__(self, data_arr):
        self.columns = []
        for column_byte in data_arr:
            bits = (0b11100000 & column_byte)
            fill = None # 0 for from-bottom, 1 for from-top
            height = 0
            if(bits != 0xe0):
                # counted from bottom
                fill = 0
                height = (0b00011111 & column_byte)
            else:
                # counted from top.
                fill = 1
                height = (0b00011111 & column_byte)

            self.columns.append((fill, height))


