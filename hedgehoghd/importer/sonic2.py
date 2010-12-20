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

import array
import logging
import os.path
import os
import struct
import json

import kosinski

import collision_array
import collision_index
import level_layout
import zone
import chunk_array

from xmlwitch import builder

class EmeraldHillZone(zone.Zone):
    acts = 2
    title = "Emerald Hill"
    code = "EHZ"
    chunk_array = "EHZ_HTZ"

class ChemicalPlantZone(zone.Zone):
    acts = 2
    title = "Chemical Plant"
    code = "CPZ"
    chunk_array = "CPZ_DEZ"

class AquaticRuinZone(zone.Zone):
    acts = 2
    title = "Aquatic Ruin"
    code = "ARZ"
    chunk_array = "ARZ"

class CasinoNightZone(zone.Zone):
    acts = 2
    title = "Casino Night"
    code = "CNZ"
    chunk_array = "CNZ"

class HillTopZone(zone.Zone):
    acts = 2
    title = "Hill Top"
    code = "HTZ"
    chunk_array = "EHZ_HTZ"

class MysticCaveZone(zone.Zone):
    acts = 2
    title = "Mystic Cave"
    code = "MCZ"
    chunk_array = "MCZ"

class OilOceanZone(zone.Zone):
    acts = 2
    title = "Oil Ocean"
    code = "OOZ"
    chunk_array = "OOZ"

class MetropolisZone(zone.Zone):
    acts = 3
    title = "Metropolis"
    code = "MTZ"
    chunk_array = "MTZ"

class SkyChaseZone(zone.Zone):
    acts = 1
    title = "Sky Chase"
    code = "SCZ"
    chunk_array = "WFZ_SCZ"

class WingFortressZone(zone.Zone):
    acts = 1
    title = "Wing Fortress"
    code = "WFZ"
    chunk_array = "WFZ_SCZ"

class DeathEggZone(zone.Zone):
    acts = 1
    title = "Death Egg"
    code = "DEZ"
    chunk_array = "CPZ_DEZ"

def mkdirs(path):
    try:
        os.makedirs(path)
    except OSError, e:
        if e.errno != 17:
            logging.error("Couldn't create output directory: %s" % str(e))  
            exit(-1)

class Sonic2(object):
    def __init__(self, s2_split_disassembly_dir, hhd_game_path):
        self.hhd_game_path = hhd_game_path
        mkdirs(hhd_game_path)
        self.s2_split_disassembly_dir = s2_split_disassembly_dir
        if not os.path.isdir(s2_split_disassembly_dir):
            raise Exception("%s: invalid Sonic 2 split disassembly directory!" % s2_split_disassembly_dir)
        print "Loading Sonic 2 game data."

        logging.info("Loading Collision Arrays...")
        logging.info("... 1")
        coll1_fd = open(os.path.join(s2_split_disassembly_dir, "collision", "Collision array 1.bin"), "rb")
        self.coll1 = collision_array.CollisionArray(coll1_fd.read())
        coll1_fd.close()

        logging.info("... 2 (I don't really use it, but whatever...)")
        coll2_fd = open(os.path.join(s2_split_disassembly_dir, "collision", "Collision array 2.bin"), "rb")
        self.coll2 = collision_array.CollisionArray(coll2_fd.read())
        coll2_fd.close()

        self.chunk_arrays = {}

        ca_id = 0
        for cname in ["ARZ", "CNZ", "CPZ_DEZ", "EHZ_HTZ", "MCZ", "OOZ", "MTZ", "WFZ_SCZ"]:
            self.loadChunkArray(cname, ca_id)
            ca_id += 1
        
        self.zones = {}
        self.zones["ehz"] = EmeraldHillZone(self, self.chunk_arrays["EHZ_HTZ"])
        self.zones["cpz"] = ChemicalPlantZone(self, self.chunk_arrays["CPZ_DEZ"])
        self.zones["arz"] = AquaticRuinZone(self, self.chunk_arrays["ARZ"])
        self.zones["cnz"] = CasinoNightZone(self, self.chunk_arrays["CNZ"])
        self.zones["htz"] = HillTopZone(self, self.chunk_arrays["EHZ_HTZ"])
        self.zones["mcz"] = MysticCaveZone(self, self.chunk_arrays["MCZ"])
        self.zones["ooz"] = OilOceanZone(self, self.chunk_arrays["OOZ"])
        self.zones["mtz"] = MetropolisZone(self, self.chunk_arrays["MTZ"])
        self.zones["scz"] = SkyChaseZone(self, self.chunk_arrays["WFZ_SCZ"])
        self.zones["wfz"] = WingFortressZone(self, self.chunk_arrays["WFZ_SCZ"])
        self.zones["dez"] = DeathEggZone(self, self.chunk_arrays["CPZ_DEZ"])

        for zc in self.zones.keys():
            z = self.zones[zc]
            z.writeHHD(os.path.join(self.hhd_game_path, "zones"))

        # self.ehz.toSVG("/tmp/ehz.svg")



        # collxml = builder(version="1.0", encoding="utf-8")

        # with collxml.svg(**{'xmlns:dc':"http://purl.org/dc/elements/1.1/",
        #                 'xmlns:rdf':"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        #                 'xmlns:svg':"http://www.w3.org/2000/svg",
        #                 'xmlns':"http://www.w3.org/2000/svg",
        #                 'version':"1.1",
        #                 'width':"%d" % ((16*len(self.coll1.tiles)) + (4*(len(self.coll1.tiles)))), 'height':"%d" % (32 + 4)}):
        #     with collxml.g(id="collision1"):
        #         self.coll1.toSVG(collxml)
        #     with collxml.g(id="collision2", transform="translate(0, 20)"):
        #         self.coll2.toSVG(collxml)

        # coll_svg_fd = open(os.path.join(self.hhd_game_path, "collision.svg"), "wb")
        # coll_svg_fd.write(str(collxml))
        # coll_svg_fd.close()

        # coll1_dir = os.path.join(self.hhd_game_path, "collision")
        # mkdirs(coll1_dir)
        # self.coll1.writeSVGs(coll1_dir)

        jmdfn = open(os.path.join(self.hhd_game_path, "game.json"), "wb")
        jmdfn.write(json.dumps(self.jsonMetadata()))
        jmdfn.close()

        # TODO instantiate each Zone, which will itself instantiate each act
        # they will look up chunks in the chunkarrays above.

    def loadChunkArray(self, name, c_id):
        logging.info("Loading 128x128 chunk array: %s" % name)
        collision_index_name = name
        if(name == "CPZ_DEZ"):
            collision_index_name = "CPZ and DEZ"
        elif(name == "EHZ_HTZ"):
            collision_index_name = "EHZ and HTZ"
        elif(name == "WFZ_SCZ"):
            collision_index_name = "WFZ and SCZ"

        index_fn_pattern = os.path.join(self.s2_split_disassembly_dir, "collision", "%s %s 16x16 collision index.bin" % (collision_index_name, "%s"))
        
        c_p_idx_fd = open(index_fn_pattern % "primary", "rb")
        primary_index = collision_index.CollisionIndex(self, c_p_idx_fd.read())
        c_p_idx_fd.close()
        
        secondary_index = None
        # MCZ, OOZ, MTZ, and WFZ_SCZ don't have secondary indexes...
        if(not (name == "MCZ" or name == "OOZ" or name == "MTZ" or name == "WFZ_SCZ")):
            c_s_idx_fd = open(index_fn_pattern % "secondary", "rb")
            secondary_index = collision_index.CollisionIndex(self, c_s_idx_fd.read())
            c_s_idx_fd.close()
                                        
        chunk_fd = open(os.path.join(self.s2_split_disassembly_dir, "mappings", "128x128", "%s.bin" % name), "rb")
        ca = chunk_array.ChunkArray(self, name, c_id, chunk_fd.read(), primary_index, secondary_index)
        self.chunk_arrays[name] = ca
        chunk_fd.close()
        svg_path = os.path.join(self.hhd_game_path, "chunks", str(c_id))
        mkdirs(svg_path)
        ca.writeSVGs(svg_path)

    def jsonMetadata(self):
        def collect_zone_metadata():
            results = []
            for code, z in self.zones.iteritems():
                results.append(z.jsonMetadata())
            return results
        def collect_chunk_array_metadata():
            results = []
            for name, ca in self.chunk_arrays.iteritems():
                results.append(ca.jsonMetadata())
            return results
        md = {"title": "Sonic the Hedgehog 2",
              "copyrights": [{"date": "1992",
                             "owner": "Sega Enterprises",
                             "license": "All Rights Reserved"}],
              "hhd_version": 0,
              "zones": collect_zone_metadata(),
              "chunksets": collect_chunk_array_metadata()
              }
        return md
