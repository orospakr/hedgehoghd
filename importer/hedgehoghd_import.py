#!/usr/bin/env python


import sys
import optparse

import kosinski
import sonic2
import os.path

if __name__ == '__main__':
    parser = optparse.OptionParser(usage="%prog: <disassembly repo>")
    
    (options, args) = parser.parse_args()
    if(len(args) != 1):
        parser.error("You must specify a path to the Sonic Retro disassembly repository.")
    
    s2_path = os.path.join(args[0], "Sonic 2 Split Disassembly")
    sonic2 = sonic2.Sonic2(s2_path)


