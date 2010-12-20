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

import os.path
import logging

import sonic2
import level_layout

from xmlwitch import builder

class Zone(object):
    '''A Zone!

    Contains several Acts.

    This class is inherited from in order to create a definition of a
    specific Zone.
    '''
    def __init__(self, sonic2, chunk_array):
        if chunk_array is None:
            logging.error("What? Can't give a zone an undefined chunk array!")
        self.chunk_array = chunk_array
        # load LevelMaps from level/layout for each act
        logging.info("Loading %s Zone..." % self.title)
        self.act_layouts = []
        if(self.acts == 1):
            # only one act, disasm names them directly.
            fd = open(os.path.join(sonic2.s2_split_disassembly_dir, "level", "layout", "%s.bin" % self.code), "rb")
            self.act_layouts.append(level_layout.LevelLayout(self.chunk_array, fd.read()))
            fd.close()
        else:
            for act in range(0, self.acts):
                logging.info("... Act %d" % (act + 1))
                fd = open(os.path.join(sonic2.s2_split_disassembly_dir, "level", "layout", "%s_%d.bin" % (self.code, act + 1)), "rb") # acts are numbered from 1 in the disasm
                self.act_layouts.append(level_layout.LevelLayout(self.chunk_array, fd.read()))
                fd.close()

    def jsonMetadata(self):
        return {"title": self.title,
                "code": self.code,
                "acts": self.acts,
                "chunks_id": self.chunk_array.c_id}

    def writeHHD(self, path):
        # have my levellayouts write out their HHD representations
        zone_path = os.path.join(path, self.code)
        sonic2.mkdirs(zone_path)
        for act in range(0, self.acts):
            act_path = os.path.join(zone_path, str(act))
            sonic2.mkdirs(act_path)
            self.act_layouts[act].writeHHDMaps(act_path)

    # def toSVG(self, filename):
    #     xml = builder(version="1.0", encoding="utf-8")

    #     # just doing Act 1 for now.
    #     with xml.svg(**{'xmlns:dc':"http://purl.org/dc/elements/1.1/",
    #                     'xmlns:rdf':"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    #                     'xmlns:svg':"http://www.w3.org/2000/svg",
    #                     'xmlns':"http://www.w3.org/2000/svg",
    #                     'version':"1.1",
    #                     'width':"%d" % (128*128), 'height':"%d" % (128*16),
    #                     'id':self.code}):
    #         with xml.g(id="act1"):
    #              self.act_layouts[0].toSVG(xml)

    #     fd = open(filename, "wb")
    #     fd.write(str(xml))
    #     fd.close()
