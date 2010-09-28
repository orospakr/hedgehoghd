import os.path
import logging

import level_layout

class Zone(object):
    '''A Zone!
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
