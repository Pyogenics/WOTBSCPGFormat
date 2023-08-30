'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from enum import Enum

# Poly group index format LUT
# 0 = uint16
# 1 = uint32
IndexFormatLUT = [
    2,
    4
]

# What type of primitve a poly group stores,
# found in the rhi_primitiveType field
class PrimitiveType(Enum):
    TRIANGLELIST = 1
    TRIANGLESTRIP = 2 #TODO
    LINELIST = 10 #TODO

# NONE = no packing
# DEFAULT = ???? TODO
class VertexPacking(Enum):
    NONE = 0
    DEFAULT = 1

# Vertices packed into the vertex array,
# flags are found in the vertexFormat field
class VertexTypes(Enum):
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

# Class to store a poly group's vertex format
class VertexFormat:
    def __init__(self):
        # Offsets to each element (-1 = not present)
        self.VERTEX = -1
        self.NORMAL = -1
        self.COLOR = -1
        self.TEXCOORD0 = -1
        self.TEXCOORD1 = -1
        self.TEXCOORD2 = -1
        self.TEXCOORD3 = -1
        self.TANGET = -1
        self.BINORMAL = -1
        self.HARD_JOINTINDEX = -1
        self.PIVOT4 = -1
        self.FLEXIBILITY = -1
        self.ANGLE_SIN_COS = -1
        self.JOINTINDEX = -1
        self.JOINTWEIGHT = -1
        self.CUBETEXCOORD0 = -1
        self.CUBETEXCOORD1 = -1
        self.CUBETEXCOORD2 = -1
        self.CUBETEXCOORD3 = -1
        
        # Number of bytes between the start of each section
        self.stride = 0

# Class to store vertex data
class VertexData:
    def __init__(self):
        self.VERTEX = []
        self.NORMAL = []
        self.COLOR = []
        self.TEXCOORD0 = []
        self.TEXCOORD1 = []
        self.TEXCOORD2 = []
        self.TEXCOORD3 = []
        self.TANGET = []
        self.BINORMAL = []
        self.HARD_JOINTINDEX = []
        self.PIVOT4 = []
        self.FLEXIBILITY = []
        self.ANGLE_SIN_COS = []
        self.JOINTINDEX = []
        self.JOINTWEIGHT = []
        self.CUBETEXCOORD0 = []
        self.CUBETEXCOORD1 = []
        self.CUBETEXCOORD2 = []
        self.CUBETEXCOORD3 = []

# Class to house functions to read vertex data
# from a vertex buffer
class VertexReader: #TODO: Handle all data types
    @staticmethod
    def readVertexDataFromBuffer(stream, fmt, count):
        vertexData = VertexData()

        # Read vertex data
        vertexData.VERTEX = VertexReader.readVertices(stream, fmt.stride, count)

        return vertexData
    
    @staticmethod
    def readVertices(stream, stride, count):
        fileStartPos = stream.tell()
        
        stride -= 12
        values = []
        for i in range(count):
            values.append((
                stream.readFloat(),
                stream.readFloat(),
                stream.readFloat()
            ))
            stream.seek(stride, 1)

        stream.seek(0, fileStartPos)
        return values

# Class to store PolygonGroup data
class PolygonGroup:
    def __init__(self):
        self.vertices = None # This gets filled in with a VertexData object
        self.edges = []
        self.faces = []

# Class to store SCG data
class SCG:
    def __init__(self):
        self.version = 0
        self.polygonGroups = {}
