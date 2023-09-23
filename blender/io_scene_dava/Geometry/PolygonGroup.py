'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from ..FileIO.StreamBuffer import StreamBuffer

class VertexTypes:
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

class VertexFormat:
    def __init__(self, fmt):
        # Stride values
        self.stride = 0
        self.VERTX = -1
        self.NORMAL = -1
        self.COLOR = -1
        self.TEXCOORD0 = -1
        self.TEXCOORD1 = -1
        self.TEXCOORD2 = -1
        self.TEXCOORD3 = -1
        self.TANGENT = -1
        self.BINORMAL = -1
        self.HARD_JOINTINDEX = -1
        self.CUBETEXCOORD0 = -1
        self.CUBETEXCOORD1 = -1
        self.CUBETEXCOORD2 = -1
        self.CUBETEXCOORD3 = -1
        self.PIVOT4 = -1
        self.FLEXIBILITY = -1
        self.ANGLE_SIN_COS = -1
        self.JOINTINDEX = -1
        self.JOINTWEIGHT = -1

        # Parse format
        if (fmt & VertexTypes.VERTEX):
            self.VERTEX = stride
            stride += 3 * 4
        if (fmt & VertexTypes.NORMAL):
            self.NORMAL = stride
            stride += 3 * 4
        if (fmt & VertexTypes.COLOR):
            self.COLOR = stride
            stride += 4
        if (fmt & VertexTypes.TEXCOORD0):
            self.TEXCOORD0 = stride
            stride += 2 * 4
        if (fmt & VertexTypes.TEXCOORD1):
            self.TEXCOORD1 = stride
            stride += 2 * 4
        if (fmt & VertexTypes.TEXCOORD2):
            self.TEXCOORD2 = stride
            stride += 2 * 4
        if (fmt & VertexTypes.TEXCOORD3):
            self.TEXCOORD3 = stride
            stride += 2 * 4

        if (fmt & VertexTypes.TANGENT):
            self.TANGENT = stride
            stride += 3 * 4
        if (fmt & VertexTypes.BINORMAL):
            self.BINORMAL = stride
            stride += 3 * 4
        if (fmt & VertexTypes.HARD_JOINTINDEX):
            self.HARD_JOINTINDEX = stride
            stride += 4

        if (fmt & VertexTypes.CUBETEXCOORD0):
            self.CUBETEXCOORD0 = stride
            stride += 3 * 4
        if (fmt & VertexTypes.CUBETEXCOORD1):
            self.CUBETEXCOORD1 = stride
            stride += 3 * 4
        if (fmt & VertexTypes.CUBETEXCOORD2):
            self.CUBETEXCOORD2 = stride
            stride += 3 * 4
        if (fmt & VertexTypes.CUBETEXCOORD3):
            self.CUBETEXCOORD3 = stride
            stride += 3 * 4

        if (fmt & VertexTypes.PIVOT4):
            self.PIVOT4 = stride
            stride += 4 * 4
        if (fmt & VertexTypes.FLEXIBILITY):
            self.FLEXIBILITY = stride
            stride += 4
        if (fmt & VertexTypes.ANGLE_SIN_COS):
            self.ANGLE_SIN_COS = stride
            stride += 2 * 4

        if (fmt & VertexTypes.JOINTINDEX):
            self.JOINTINDEX = stride
            stride += 4 * 4
        if (fmt & VertexTypes.JOINTWEIGHT):
            self.JOINTWEIGHT = stride
            stride += 4 * 4

        self.stride = stride

class PrimitiveTypes:
    TRIANGLELIST = 1
    TRIANGLESTRIP = 2
    LINELIST = 10

class PolygonGroup:
    def __init__(self, polyGroup):
        self.id = polyGroup["#id"]
        self.cubeTextureCoordCount = polyGroup["cubeTextureCoordCount"]
        self.primitiveType = polyGroup["rhi_primitiveType"]

        # Vertices
        self.vertices = []
        self.normals = []
        self.colors = []
        self.texcoords = []
        self.tangents = []
        self.binormals = []
        self.hard_jointindices = []
        self.pivot4 = []
        self.flexibilities = []
        self.angles_sin_cos = []
        self.jointindices = []
        self.jointweights = []
        self.cubetexcoords = []

        # Parse vertex format
        vertexFormat = VertexFormat(polyGroup["self"])

        # Parse vertices TODO
        stream = StreamBuffer( BytesIO(polyGroup["vertices"]) )
        for _ in range(polyGroup["vertexCount"]):
            if vertexFormat.VERTEX > -1:
                self.vertices.append(
                        (stream.readFloat(), stream.readFloat(), stream.readFloat())
                )

        # Parse indices
        # 0 = uint16_t
        # 1 = uint32_t
        stream = StreamBuffer( BytesIO(polyGroup["indices"]) )
        self.indices = []
        if polyGroup["indexFormat"] == 0:
            for _ in range(polyGroup["indexCount"]): self.indices.append( stream.readInt16(False) )
        if polyGroup["indexFormat"] == 1:
            for _ in range(polyGroup["indexCount"]): self.indices.append( stream.readInt32(False) )

        '''
        Primitive builders

        line list, triangle list, triangle strip
        '''
        # Turn indices + vertices into a single vertex array
        def collectVertices(self, indices):
            vertexArray = []
            for index in indices:
                vertexArray.append( self.vertices[index] )
            return vertexArray

        def generateTriangleList(self):
            faceIndices = []
            for i in range(0, count, 3):
                faceIndices.append([
                    self.indices[i],
                    self.indices[i+1],
                    self.indices[i+2]
                ])

            return self.collectVertices(faceIndices)

        #NOTE: We convert trianglestrip to trianglist to make the import easier
        def generateTriangleStrip(self): 
            faceIndices = []

            # First triangle
            faceIndices.append([
                self.indices[0],
                self.indices[1],
                self.indices[2]
            ])

            # Digest triangestrip into trianglelist
            for i in range(3, count):
                faceIndices.append([
                    self.indices[i-2],
                    self.indices[i-1],
                    self.indices[i]
                ])

            return self.collectVertices(indices)

        def generateLineList(self):
            edgeIndices = []
            for i in range(0, count, 2):
                edgeIndices.append([
                    self.indices[i],
                    self.indices[i+1]
                ])


            return self.collectVertices(edgeIndices)
