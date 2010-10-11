import os.path
import logging
import cairo

import level_layout

from xmlwitch import builder


class Zone(object):
    '''A Zone!

    Contains several Acts.

    This class is inherited from in order to create a definition of a
    specific Zone.
    '''
    def __init__(self, sonic2):
        # load LevelMaps from level/layout for each act
        logging.info("Loading %s Zone..." % self.title)
        self.act_layouts = []
        if(self.acts == 1):
            # only one act, disasm names them directly.
            fd = open(os.path.join(sonic2.s2_split_disassembly_dir, "level", "layout", "%s.bin" % self.code), "rb")
            self.act_layouts.append(level_layout.LevelLayout(sonic2.chunk_arrays[self.chunk_array], fd.read()))
            fd.close()
        else:
            for act in range(0, self.acts):
                logging.info("... Act %d" % (act + 1))
                fd = open(os.path.join(sonic2.s2_split_disassembly_dir, "level", "layout", "%s_%d.bin" % (self.code, act + 1)), "rb") # acts are numbered from 1
                self.act_layouts.append(level_layout.LevelLayout(sonic2.chunk_arrays[self.chunk_array], fd.read()))
                fd.close()

    def toSVG(self, filename):

        xml = builder(version="1.0", encoding="utf-8")

        # just doing Act 1 for now.
        with xml.svg(**{'xmlns:dc':"http://purl.org/dc/elements/1.1/",
                        'xmlns:rdf':"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                        'xmlns:svg':"http://www.w3.org/2000/svg",
                        'xmlns':"http://www.w3.org/2000/svg",
                        'version':"1.1",
                        'width':"%d" % (128*128), 'height':"%d" % (128*16),
                        'id':self.code}):
            with xml.g(id="act1"):
                 self.act_layouts[0].toSVG(xml)


        

        fd = open(filename, "wb")
        fd.write(str(xml))
        fd.close()
#        svg = cairo.SVGSurface(filename, 128*128, 128*16) 
#        cr = cairo.Context(svg)
        # cr.translate(512, 512)
        # cr.set_line_width(1)
        # cr.set_source_rgb(0, 0, 0)
        # cr.rectangle(0, 0, 128, 128)
        # cr.fill()

        # cr.translate(512, 512)
        # cr.set_line_width(1)
        # cr.set_source_rgb(0, 0, 0)
        # cr.rectangle(0, 0, 128, 128)
        # cr.fill()

        # cr.translate(-1024, -1024)
        # cr.set_line_width(1)
        # cr.set_source_rgb(255, 0, 255)
        # cr.rectangle(0, 0, 128, 128)
        # cr.fill()

        # let's just do Act 1 for now
        # self.act_layouts[0].toSVG(cr)
#        cr.stroke()
