'''
Copyright (C) 2023  Pyogenics <https://github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
from sys import argv

from keyedArchive import KeyedArchive
from common import ImportError


def readHeader(stream):
    if stream.read(4) != b"SCPG":
        raise ImportError("Invalid header magic")

    version = int.from_bytes(stream.read(4), "little")
    nodeCount = int.from_bytes(stream.read(4), "little")
    nodeCount_two = int.from_bytes(stream.read(4), "little") # This probably is a different type of node?

    print(f"SCPG version: {version}; node count: {nodeCount}; node count 2: {nodeCount_two};")
    
    return nodeCount

with open(argv[1], "rb") as f:
    nodeCount = readHeader(f)
    keyedArchives = []
    for i in range(nodeCount):
        print(f"Node {i}:")
        ka = KeyedArchive()
        ka.loadFromFileStream(f)
        keyedArchives.append(ka)

    print(f"Done! Available archives: {len(keyedArchives)}")
    
    while i := input("Enter the number of a KA to dump: "):
        archive = keyedArchives[int(i)]
        keys = ", ".join(list(archive.items.keys()))
        while j := input(f"Choose one: [{keys}] | "):
            print(archive.items[j])
