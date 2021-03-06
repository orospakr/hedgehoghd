# HedgehogHD - Vector Graphics Platform Game Engine
# Copyright (C) 2010  Andrew Clunis <andrew@orospakr.ca>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

from xmlwitch import builder

class CollisionTile(object):
    '''16x16 Collision Shape Tile

    They effectively draw a filled in bitmapped shape with a value per
    column (they cannot contain an arbitrary 16x16 bitmap), with bits
    that determine whether the column is filled in above or below the
    specified height.

    The first 3 bits of this byte are on when filling in from the top,
    or off when filling in from the bottom.  The remaining bits are
    the height position (counted from the bottom).  However, in order
    to have an empty position, the height value when filling from the
    bottom counts from 1 rather than 0, so that 0 might be used as the
    column empty value.

    http://forums.sonicretro.org/index.php?showtopic=3095
    '''
    def __init__(self, data_arr):
        self.columns = []
        for column_byte in data_arr:
            bits = (0b11100000 & column_byte)
            fill = None # 0 for from-bottom, 1 for from-top
            height = 0
            if(bits != 0xe0):
                # fill from bottom
                fill = 0
                h_val = (0b00011111 & column_byte)
                if(h_val != 0):
                    height = h_val - 1
                else:
                    height = None
            else:
                # fill from top.
                fill = 1
                height = (0b00011111 & column_byte)

            self.columns.append((fill, height))

    def writeSVG(self, filename):
        collxml = builder(version="1.0", encoding="utf-8")

        with collxml.svg(**{'xmlns:dc':"http://purl.org/dc/elements/1.1/",
                            'xmlns:rdf':"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                            'xmlns:svg':"http://www.w3.org/2000/svg",
                            'xmlns':"http://www.w3.org/2000/svg",
                            'version':"1.1",
                            'width': "16",
                            'height': "16"}):
                         
            self.toSVG(collxml)

        svg_fd = open(filename, "wb")
        svg_fd.write(str(collxml))
        svg_fd.close()

    def toSVG(self, xml):
        column_pos = 0
        first = True

        with xml.rect(x="0", y="0", width="16", height="16", style="fill:none;stroke:#7f7f7f"):
            pass

        last_top = None
        last_bottom = None

        path_entries = []

        def prepend(movetype, coordpair):
            path_entries.insert(0, [movetype, coordpair])

        def append(movetype, coordpair):
            path_entries.append([movetype, coordpair])

        for column in self.columns:
            # when we hit the first column with data,
            # create two cursors that will go separate directions ('top' and 'bottom')
            # the cursor should remember its height level so it can avoid putting extra path entries
            # above cursor will prepend points, below cursor will append them.
            # above cursor is reponsible for prepending the M point on the path, on its last entry.

            fill, height = column

            def current_bottom():
                if(fill == 1):
                    # fill from top.
                    return height
                else:
                    # fill from bottom.
                    return 0

            def current_top():
                if(fill == 1):
                    # fill from top
                    return 15
                else:
                    # fill from bottom.
                    return height

            on_last_column = column_pos == 15

            if(height != None):
                # -15 because the SVG origin is top-left, whereas my data is bottom-left.
                if((current_bottom() != last_bottom) or on_last_column):
                    append('L', '%d, %d' % (column_pos, 15 - current_bottom()))
                    last_bottom = current_bottom()

                if((current_top() != last_top) or on_last_column):
                    prepend('L', '%d, %d' % (column_pos, 15 - current_top()))
                    last_top = current_top()
            
            # last column!
            if(on_last_column):
                if(len(path_entries) < 4):
                    # this log message is surpressed down to debug level because it just gets too spammy.
                    # no one cares about those crappy blocks anyway. :)
                    logging.debug("This collision tile cannot be traced.  Skipping. %d" % len(path_entries))
                    return

                path_entries[0][0] = 'M'
                # we need a lineto for that last segment or the stroke won't happen there
                path_entries.append(['L', path_entries[0][1]])
                path_entries.append(['Q', ''])
                break

            column_pos += 1

        path_string = ""
        for node in path_entries:
            path_string += "%s%s " % (node[0], node[1])

        with xml.path(d=path_string,
                      style="fill:#00ff00;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"):
            pass
