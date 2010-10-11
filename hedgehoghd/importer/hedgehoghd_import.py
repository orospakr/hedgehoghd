#!/usr/bin/env python

import sys
import optparse
import logging

import kosinski
import sonic2
import os.path

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = optparse.OptionParser(usage="%prog: <disassembly repo> <HedgehogHD game dir>")
    
    (options, args) = parser.parse_args()
    if(len(args) != 2):
        parser.error("You must specify a path to the Sonic Retro disassembly repository, and a target HedgehogHD game directory to write the Sonic 2 level data into")
    
    s2_path = os.path.join(args[0], "Sonic 2 Split Disassembly")
    hhd_game_path = os.path.join(args[1])
    sonic2 = sonic2.Sonic2(s2_path, hhd_game_path)
