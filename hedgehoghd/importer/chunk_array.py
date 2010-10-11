import logging
from xmlwitch import builder
import chunk
import kosinski

class ChunkArray(object):
    '''Array of Chunks, used by either one or two Zones.

    Owns equivalent collision indexes.
    '''
    def __init__(self, sonic2, name, data, primary_collision_index, secondary_collision_index):
        self.name = name
        self.sonic2 = sonic2
        self.primary_collision_index = primary_collision_index
        self.secondary_collision_index = secondary_collision_index

        bm = kosinski.decompress_string(data).tostring()

        if((len(bm) % 128) != 0):
            logging.error("Inappropriately sized level map: %d" % bmfs)
            exit(-1)

        blocks = len(bm) / 128

        logging.debug("There are %d blocks in this ChunkArray." % blocks)

        self.chunks = []
        chunk_no = 0
        for block in range(0, blocks):
            logging.debug("... chunk %d: " % chunk_no)
            chunk_no += 1
            block_data = bm[block*128:(block*128) + 128]
            self.chunks.append(chunk.Chunk(self, block_data, chunk_no))
    
    def writeSVG(self):
        logging.info("Writing SVG for chunk array: %s" % self.name)
        chunk_xml = builder(version="1.0", encoding="utf-8")
        with chunk_xml.svg(**{'xmlns:dc':"http://purl.org/dc/elements/1.1/",
                        'xmlns:rdf':"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                        'xmlns:svg':"http://www.w3.org/2000/svg",
                        'xmlns':"http://www.w3.org/2000/svg",
                        'version':"1.1",
                        'width':"%d" % (128*len(self.chunks)), 'height':"%d" % (128)}):
            self.toSVG(chunk_xml)
        
        chunk_xml_fd = open("/tmp/%s_chunks.svg" % self.name, "wb")
        chunk_xml_fd.write(str(chunk_xml))
        chunk_xml_fd.close()

    def toSVG(self, xml):
        chunkpos = 0
        for chunk in self.chunks:
            with xml.g(id="chunk_%x" % chunkpos, transform="translate(%d, 0)" % (chunkpos * 128)):
                chunk.toSVG(xml)
            chunkpos += 1


