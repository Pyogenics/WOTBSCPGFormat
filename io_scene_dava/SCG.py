from .Utils import unpackStream
from .KeyedArchive import readKeyedArchive

class SCG:
    def __init__(self):
        self.version = 0
        self.nodes = []

    def read(self, stream):
        print("Reading SCG data")

        # Verify signature
        signature = stream.read(4)
        if signature != b"SCPG":
            raise RuntimeError(f"Invalid SCG signature: {signature}")
        
        # Read header
        self.version, nodeCount, _ = unpackStream("<3I", stream)
        if self.version > 1:
            raise RuntimeError(f"Unsupported SCG version: {self.version}")
        
        # Read nodes
        print(f"Reading {nodeCount} nodes")
        for nodeI in range(nodeCount):
            node = readKeyedArchive(stream)
            self.nodes.append(node)