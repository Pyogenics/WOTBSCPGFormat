from .Utils import unpackStream
from .KeyedArchive import readKeyedArchive

class SC2:
    def __init__(self):
        self.version = 0
        self.versionTags = {}
        self.descriptor = b""
        self.nodes = []

    def read(self, stream):
        print("Reading SC2 data")

        # Verify signature
        signature = stream.read(4)
        if signature != b"SFV2":
            raise RuntimeError(f"Invalid SC2 signature: {signature}")
        
        # Read header
        self.version, nodeCount = unpackStream("<2I", stream) # XXX: Node count can be >1 but this is wrong (all sc2 trees seemingly have one node)
        self.versionTags = readKeyedArchive(stream)
        descriptorLength, = unpackStream("<I", stream)
        self.descriptor = stream.read(descriptorLength)

        # Read nodes
        print(f"Reading {nodeCount} nodes")
        for nodeI in range(1):
            node = readKeyedArchive(stream)
            self.nodes.append(node)

        print(f"[SC2 version={self.version} versionTags={self.versionTags} descriptor={self.descriptor} nodes={len(self.nodes)}]")