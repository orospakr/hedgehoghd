#!/usr/bin/env python

import array
import logging
import os.path
import struct

import kosinski

import collision_array
import collision_index
import level_layout
import zone
import chunk_array

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

class Sonic2(object):
    def __init__(self, s2_split_disassembly_dir):
        self.s2_split_disassembly_dir = s2_split_disassembly_dir
        if not os.path.isdir(s2_split_disassembly_dir):
            raise Exception("%s: invalid Sonic 2 split disassembly directory!" % s2_split_disassembly_dir)
        print "Loading Sonic 2 game data."

        logging.info("Loading Collision Arrays...")
        logging.info("... 1")
        coll1_fd = open(os.path.join(s2_split_disassembly_dir, "collision", "Collision array 1.bin"), "rb")
        self.coll1 = collision_array.CollisionArray(coll1_fd.read())
        coll1_fd.close()

        logging.info("... 2")
        coll2_fd = open(os.path.join(s2_split_disassembly_dir, "collision", "Collision array 2.bin"), "rb")
        self.coll2 = collision_array.CollisionArray(coll2_fd.read())
        coll2_fd.close()

        self.chunk_arrays = {}

        for cname in ["ARZ", "CNZ", "CPZ_DEZ", "EHZ_HTZ", "MCZ", "OOZ", "MTZ", "WFZ_SCZ"]:
            self.loadChunkArray(cname)
        
        self.ehz = EmeraldHillZone(self)
        self.cpz = ChemicalPlantZone(self)
        self.arz = AquaticRuinZone(self)
        self.cnz = CasinoNightZone(self)
        self.htz = HillTopZone(self)
        self.mcz = MysticCaveZone(self)
        self.ooz = OilOceanZone(self)
        self.mtz = MetropolisZone(self)
        self.scz = SkyChaseZone(self)
        self.wfz = WingFortressZone(self)
        self.dez = DeathEggZone(self)

        self.ehz.toSVG("/tmp/ehz.svg")

        # TODO instantiate each Zone, which will itself instantiate each act
        # they will look up chunks in the chunkarrays above.

    def loadChunkArray(self, name):
        logging.info("Loading 128x128 chunk array for: %s" % name)
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
        self.chunk_arrays[name] = chunk_array.ChunkArray(self, name, chunk_fd.read(), primary_index, secondary_index)
        chunk_fd.close()
