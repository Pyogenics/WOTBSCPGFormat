'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from .blError import ImportError
from .KeyedArchiveIO import KeyedArchive

from enum import Enum
from io import BytesIO
from struct import unpack

indexFormatSize = [
    2,
    4
]

class vertexPacking(Enum):
    NONE = 0
    DEFAULT = 1

class primitiveType(Enum):
    TRIANGLELIST = 1
    TRIANGLESTRIP = 2
    LINELIST = 10

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

class SCGImporter:
    def __init__(self):
        self.polygonGroups = []

    def parseVertexFormat(self, fmt):
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

    def parseTriangleList(self, indexStream, indexSize, primitiveCount):
        triangleList = []
        for triI in range(primitiveCount):
            triangleList.append([
                int.from_bytes(indexStream.read(indexSize), "little"),
                int.from_bytes(indexStream.read(indexSize), "little"),
                int.from_bytes(indexStream.read(indexSize), "little")
            ])
        return triangleList

    def parseTriangleStrip(self, stream):
        pass

    def parseLineList(self, stream):
        pass

    #TODO: This could go into a separate class
    def parsePolygonGroup(self, node):
        # Parse vertex format
        stride = self.parseVertexFormat(node["vertexFormat"])

        #TODO: handle: primitive count, cube texture coords (https://github.com/smile4u/dava.engine/blob/development/Sources/Internal/Render/3D/PolygonGroup.cpp#L173)

        #TODO: Handle vertex packing
        if node["packing"] != vertexPacking.NONE.value:
            raise ImportError(f"Unknown vertex packing {node['packing']}")

        # Carve out polygon data
        vertexArray = node["vertices"]
        indexArray = node["indices"]

        vertices = []
        edges = []
        faces = []

        logicalSize = stride * node["vertexCount"]
        realSize = len(vertexArray)
        if logicalSize != realSize:
            raise ImportError(f"Invalid vertex array size, logical: {logicalSize} real: {realSize}")
        #XXX: We could probably skip this instead?
        elif realSize < 1:
            raise ImportError(f"No vertices in this PolygonGroup")

        ## Compose vertex data
        vertexStream = BytesIO(vertexArray)
        for _ in range(node["vertexCount"]):
            vertex = unpack("fff", vertexStream.read(12))
            vertices.append(vertex)
            #TODO: handle the rest of the data properly
            vertexStream.read(stride-12)

        indexStream = BytesIO(indexArray)
        match node["rhi_primitiveType"]:
            case primitiveType.TRIANGLELIST.value:
                faces = self.parseTriangleList(indexStream, indexFormatSize[node["indexFormat"]], node["primitiveCount"])
            case other:
                raise ImportError(f"Unknown primitve type: {node['rhi_primitiveType']}")

        self.polygonGroups.append({"vertices": vertices, "edges": edges, "faces": faces, "id": int.from_bytes(node["#id"], "little")})

    def importFromFileStream(self, stream):
        # Verify magic
        if stream.read(4) != b"SCPG":
            raise ImportError("Invalid header magic")

        # Read header
        version = int.from_bytes(stream.read(4), "little")
        nodeCount = int.from_bytes(stream.read(4), "little")
        nodeCount_two = int.from_bytes(stream.read(4), "little") # This probably is a different type of node?

        self.version = version

        # Read nodes
        nodes = []
        for i in range(nodeCount):
            node = KeyedArchive()
            node.loadFromFileStream(stream)
            nodes.append(node)

        # Parse nodes
        for node in nodes:
            if node.items["##name"] == "PolygonGroup":
                self.parsePolygonGroup(node.items)
