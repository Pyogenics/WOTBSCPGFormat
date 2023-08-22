'''
Copyright (C) 2023  Pyogenics <https://github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
from sys import argv
from enum import Enum

from keyedArchive import KeyedArchive
from common import ImportError

class vertexTypes(Enum):
    VERTEX = 1
    NORMAL = 1 << 1
    COLOR = 1 << 2
    TEXCOORD0 = 1 << 3
    TEXCOORD1 = 1 << 4
    TEXCOORD2 = 1 << 5
    TEXCOORD3 = 1 << 6
    TANGENT = 1 << 7
    BINORMAL = 1 << 8
    HARD_JOINTINDEX = 1 << 9
    PIVOT4 = 1 << 10
    FLEXIBILITY = 1 << 12
    ANGLE_SIN_COS = 1 << 13
    JOINTINDEX = 1 << 14
    JOINTWEIGHT = 1 << 15
    CUBETEXCOORD0 = 1 << 16
    CUBETEXCOORD1 = 1 << 17
    CUBETEXCOORD2 = 1 << 18
    CUBETEXCOORD3 = 1 << 19

def readHeader(stream):
    if stream.read(4) != b"SCPG":
        raise ImportError("Invalid header magic")

    version = int.from_bytes(stream.read(4), "little")
    nodeCount = int.from_bytes(stream.read(4), "little")
    nodeCount_two = int.from_bytes(stream.read(4), "little") # This probably is a different type of node?

    print(f"SCPG version: {version}; node count: {nodeCount}; node count 2: {nodeCount_two};")
    
    return nodeCount

def parseVertexFormat(fmt):
    stride = 0
    
    if (fmt & vertexTypes.VERTEX.value):
        stride += 3 * 4
    if (fmt & vertexTypes.NORMAL.value):
        stride += 3 * 4
    if (fmt & vertexTypes.COLOR.value):
        stride += 4
    if (fmt & vertexTypes.TEXCOORD0.value):
        stride += 2 * 4
    if (fmt & vertexTypes.TEXCOORD1.value):
        stride += 2 * 4
    if (fmt & vertexTypes.TEXCOORD2.value):
        stride += 2 * 4
    if (fmt & vertexTypes.TEXCOORD3.value):
        stride += 2 * 4

    if (fmt & vertexTypes.TANGENT.value):
        stride += 3 * 4
    if (fmt & vertexTypes.BINORMAL.value):
        stride += 3 * 4
    if (fmt & vertexTypes.HARD_JOINTINDEX.value):
        stride += 4

    if (fmt & vertexTypes.CUBETEXCOORD0.value):
        stride += 3 * 4
    if (fmt & vertexTypes.CUBETEXCOORD1.value):
        stride += 3 * 4
    if (fmt & vertexTypes.CUBETEXCOORD2.value):
        stride += 3 * 4
    if (fmt & vertexTypes.CUBETEXCOORD3.value):
        stride += 3 * 4

    if (fmt & vertexTypes.PIVOT4.value):
        stride += 4 * 4
    if (fmt & vertexTypes.FLEXIBILITY.value):
        stride += 4
    if (fmt & vertexTypes.ANGLE_SIN_COS.value):
        stride += 2 * 4

    if (fmt & vertexTypes.JOINTINDEX.value):
        stride += 4 * 4
    if (fmt & vertexTypes.JOINTWEIGHT.value):
        stride += 4 * 4

    return stride

def parsePolygonGroup(node):
    # Parse vertex format
    vertexFormat = node["vertexFormat"]
    stride = parseVertexFormat(vertexFormat)

    #TODO: handle: primitive count, cube texture coords (https://github.com/smile4u/dava.engine/blob/development/Sources/Internal/Render/3D/PolygonGroup.cpp#L173)

    # Verify
    size = stride * node["vertexCount"]
    vertices = node["vertices"]
    if node["packing"] != 0:
        raise ImportError("Vertex packing isn't PACKING_NONE!")
    elif size != len(vertices):
        raise ImportError(f"Invalid vertex array size, logical: {size} real: {len(vertices)}")

with open(argv[1], "rb") as f:
    nodeCount = readHeader(f)
    keyedArchives = []
    for i in range(nodeCount):
        print(f"Node {i}:")
        ka = KeyedArchive()
        ka.loadFromFileStream(f)
        keyedArchives.append(ka)

    print(f"Done! Available archives: {len(keyedArchives)}")
    print("Parsing archives")
    for node in keyedArchives:
        items = node.items
        if items["##name"] == "PolygonGroup":
            parsePolygonGroup(items)

'''
while i := input("Enter the number of a KA to dump: "):
    archive = keyedArchives[int(i)]
    keys = ", ".join(list(archive.items.keys()))
    while j := input(f"Choose one: [{keys}] | "):
        print(archive.items[j])
'''
