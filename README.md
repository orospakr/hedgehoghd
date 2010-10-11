HedgehogHD
==========

An attempt to reimplement the famous YU2 Sonic platformer engine from
the Sega Genesis, with an emphasis on supporting pixel independent
vector graphics.

Copyright 2010 Andrew Clunis <andrew@orospakr.ca>
Distributed under the terms of the GNU General Public License v3.

Please see file COPYING for details.

Please note that the xmlwitch module included in the importer is BSD
licensed (please see file for details).

Importer
--------

The only existing component currently is the importer facility, which
is a Python program that reads game geometry from the "Split
Disassembly" provided by the good folks at Sonic Retro.  This can be
acquired with:
    svn co https://sonicretro.org/asm_svn

To produce collision geometry SVG from Sonic 2, run from the root of the HedgehogHD repo:

    hedgehoghd/importer/hedgehoghd_import.py ~/path/to/asm_svn ~/svg_output/

To produce HTML documentation:

    cd doc
    make html

References:

* http://stephenuk.hacking-cult.org/SCHG/General/CollisionFormat/CollisionFormat.htm
* http://forums.sonicretro.org/index.php?showtopic=3095
* http://info.sonicretro.org/SCHG:Sonic_2/Level_Editing