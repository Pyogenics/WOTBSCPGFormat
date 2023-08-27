'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from .SCG import *
from ..KA.KAReader import KAReader
from ..FileIO import FileBuffer

# Class that reads SCG files
class SCGReader:
    @staticmethod
    def readFromBuffer(stream):
        # Verify magic
        if (stream.readString(4) != "SCPG"):
            raise ReadError("SCGReader", "Bad magic string")
        
        # Read header
        version = stream.readInt32(False)
        nodeCount = stream.readInt32(False)
        stream.readInt32(False) #Second node count? TODO

        # Read nodes
        polygonGroups = {}
        for _ in range(nodeCount):
            ka = KAReader.readFromStream(stream)
            if ka["##name"] != "PolygonGroup":
                raise ReadError("SCGReader", "Unknown data node type, data node isn't a polygon group")

            polyGroup = SCGReader.readPolygonGroup(ka)
            polygonGroups[ka["#id"]] = polyGroup

        # Create and populate an SCG object
        scg = SCG()
        scg.version = version
        scg.polygonGroups = polygonGroups

        return scg
   
    #TODO: Read all types of known vertices
    @staticmethod
    def readPolygonGroup(ka):
        primitiveType = ka["rhi_primitiveType"]
        indexFormat = indexFormatLUT[ka["indexFormat"]]
        vertexFormat = SCGReader.parseVertexFormat(ka["vertexFormat"])

        # Read buffers
        indexBuffer = BytesIO(ka["indices"])
        indexBuffer = FileBuffer(indexBuffer)
        vertexBuffer = BytesIO(ka["vertices"])
        vertexBuffer = FileBuffer(vertexBuffer)

        indices = []
        if indexFormat == 2:
            for _ in range(ka["indexCount"]): indices.append(indexBuffer.readInt16(False))
        else:
            for _ in range(ka["indexCount"]): indices.append(indexBuffer.readInt32(False))
        vertices = VertexReader.readVertexDataFromBuffer(vertexBuffer) 

        # Generate primitves
        edges = []
        faces = []

        if primitiveType == PrimitiveType.TRIANGLELIST.value:
            faces = SCGReader.generateTriangleList(indices)
        elif primitiveType == PrimitiveType.TRIANGLESTRIP.value:
            faces = SCGReader.generateTriangleStrip(indices)
        elif primitiveType == PrimitiveType.LINELIST.value:
            edges = SCGReader.generateLineList(indices)
        else:
            raise ReadError("SCGReader", f"Unknown primitive type of value {primitiveType}")

        # Populate object
        polyGroup = PolygonGroup()
        polyGroup.vertices = vertices
        polyGroup.edges = edges
        polyGroup.faces = faces

        return polyGroup

    @staticmethod
    def parseVertexFormat(fmt):
        vertexFormat = VertexFormat()
        stride = 0

        if (fmt & VertexTypes.VERTEX.value):
            vertexFormat.VERTEX = stride
            stride += 3 * 4
        if (fmt & VertexTypes.NORMAL.value):
            vertexFormat.NORMAL = stride
            stride += 3 * 4
        if (fmt & VertexTypes.COLOR.value):
            vertexFormat.COLOR = stride
            stride += 4
        if (fmt & VertexTypes.TEXCOORD0.value):
            vertexFormat.TEXCOORD0 = stride
            stride += 2 * 4
        if (fmt & VertexTypes.TEXCOORD1.value):
            vertexFormat.TEXCOORD1 = stride
            stride += 2 * 4
        if (fmt & VertexTypes.TEXCOORD2.value):
            vertexFormat.TEXCOORD2 = stride
            stride += 2 * 4
        if (fmt & VertexTypes.TEXCOORD3.value):
            vertexFormat.TEXCOORD3 = stride
            stride += 2 * 4

        if (fmt & VertexTypes.TANGENT.value):
            vertexFormat.TANGENT = stride
            stride += 3 * 4
        if (fmt & VertexTypes.BINORMAL.value):
            vertexFormat.BINORMAL = stride
            stride += 3 * 4
        if (fmt & VertexTypes.HARD_JOINTINDEX.value):
            vertexFormat.HARD_JOINTINDEX = stride
            stride += 4

        if (fmt & VertexTypes.CUBETEXCOORD0.value):
            vertexFormat.CUBETEXCOORD0 = stride
            stride += 3 * 4
        if (fmt & VertexTypes.CUBETEXCOORD1.value):
            vertexFormat.CUBETEXCOORD1 = stride
            stride += 3 * 4
        if (fmt & VertexTypes.CUBETEXCOORD2.value):
            vertexFormat.CUBETEXCOORD2 = stride
            stride += 3 * 4
        if (fmt & VertexTypes.CUBETEXCOORD3.value):
            vertexFormat.CUBETEXCOORD3 = stride
            stride += 3 * 4

        if (fmt & VertexTypes.PIVOT4.value):
            vertexFormat.PIVOT4 = stride
            stride += 4 * 4
        if (fmt & VertexTypes.FLEXIBILITY.value):
            vertexFormat.FLEXIBILITY = stride
            stride += 4
        if (fmt & VertexTypes.ANGLE_SIN_COS.value):
            vertexFormat.ANGLE_SIN_COS = stride
            stride += 2 * 4

        if (fmt & VertexTypes.JOINTINDEX.value):
            vertexFormat.JOINTINDEX = stride
            stride += 4 * 4
        if (fmt & VertexTypes.JOINTWEIGHT.value):
            vertexFormat.JOINTWEIGHT = stride
            stride += 4 * 4

        vertexTypes.stride = stride

    '''
    Primitive builders
    '''
    @staticmethod
    def generateTriangleList(indices, count):
        faces = []
        for i in range(0, count, 3):
            faces.append(
                indices[i],
                indices[i+1],
                indices[i+2]
            )

        return faces

    @staticmethod
    def generateTriangleStrip(indices, count): #TODO
        faces = []
        return faces

    @staticmethod
    def generateLineList(indices, count): #TODO
        edges = []
        return edges
