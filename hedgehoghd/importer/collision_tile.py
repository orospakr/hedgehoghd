class CollisionTile(object):
    '''16x16 Collision Shape Tile

    They effectively draw a bitmapped line with a value per column (they
    cannot contain an arbitrary 16x16 bitmap), with bits that determine
    whether the solid piece is above or below the specified height.

    http://forums.sonicretro.org/index.php?showtopic=3095
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
        column_pos = 0
        first = True
        path_string = ""

        with xml.rect(x="0", y="0", width="16", height="16", style="fill:none;stroke:#7f7f7f"):
            pass

        # TODO: there can be breaks in the path, which are not handled here.  really need to start a new path element.
        for column in self.columns:
            fill, height = column
            if(height == 0):
                column_pos += 1
                continue
            if(first):
                path_string += "M %d,%d " % (column_pos, 16 - height)
                first = False
            else:
                path_string += "L %d,%d " % (column_pos, 16 - height)
            column_pos += 1

        with xml.path(d=path_string,
                      style="fill:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"):
            pass
        
