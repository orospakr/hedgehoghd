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


    def toSVG(self, xml):
        path_string = "M 0,0 "
        column_pos = 0
        
        for column in self.columns:
            fill, height = column
            if(fill == 1):
                # from top
                path_string += "L %d,%d " % (column_pos, height - 16)
            else:
                # from bottom
                path_string += "L %d,%d " % (column_pos, height)
                column_pos += 1

        with xml.path(d=path_string,
                      style="fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"):
            pass
        
