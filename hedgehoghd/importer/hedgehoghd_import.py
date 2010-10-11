#!/usr/bin/env python
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
