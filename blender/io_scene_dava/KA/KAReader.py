'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from .KA import *
from .types import AABBox3
from ..FileIO import FileBuffer
from ..ErrorWrappers import ReadError

from io import BytesIO

# Class to turn KAs into dictionaries
class KAReader:
    @staticmethod
    def readFromBuffer(stream, keyMap = {}):
        # Verify magic
        if stream.readString(2) != "KA":
            raise ReadError("KAReader", "Bad magic string")

        # Read header
        version = stream.readInt16(False)
        itemCount = stream.readInt32(False)

        # Read data
        if itemCount == 0:
            return {}
        data = {}
        if version == 1:
            KAReader.readV1Data(stream, itemCount, data)
        elif version == 2:
            KAReader.readV2Data(stream, itemCount, data)
        elif version == 258:
            KAReader.readV258Data(stream, itemCount, data)
        else:
            raise ReadError("KAReader", f"Unknown KA version: {version}")

        return data

    '''
    Data readers
    '''

    @staticmethod
    def readV1Data(stream, count, data):
        for _ in range(count):
            key = V1DataReader.readValue(stream)
            value = V1DataReader.readValue(stream)
            data[key] = value

    #NOTE: String table resolution happens in SC2Reader,
    # we just provide the raw data!
    @staticmethod
    def readV2Data(stream, count, data):
        # Read strings
        strings = []
        for _ in range(count):
            string = V2DataReader.readValue(stream)
            strings.append(string)

        # Build string table
        stringTable = {}
        for stringI in range(count):
            index = stream.readInt32(False)
            stringTable[index] = strings[stringI]

        # Read hierarchy
        hierarchy = {}
        hierarchyNodeCount = stream.readInt32(False)        
        for _ in range(hierarchyNodeCount):
            nodeName = stringTable[stream.readInt32(False)]
            print(F"V2HR reading {nodeName}")

            nodes = V2DataReader.readHierarchyValue(stream)

            # Resolve strings
            resolvedNodes = []
            for node in nodes:
                if isinstance(node, Mapping):
                    resolvedNodes.append(V258DataReader.resolveStrings(stringTable, node))
                elif isinstance(node, V258UnresolvedString):
                    resolvedNodes.append(stringTable[node.stringTableIndex])
                else:
                    resolvedNodes.append(node)

            data[nodeName] = resolvedNodes

    #NOTE: String table resolution happens in SC2Reader,
    # we just provide the raw data!
    @staticmethod
    def readV258Data(stream, count, data):
        for _ in range(count):
            key = V258DataReader.readKey(stream)
            value = V258DataReader.readValue(stream)
            data[key] = value

'''
Data readers
'''

class V1DataReader:
    # This is split from the actual reading code to allow for
    # additional types to be added in by other classes
    @classmethod
    def readValue(self, stream):
        valueType = stream.readInt8(False)
        return self.readFromValueType(stream, valueType)

    # This should be called after all other typechecking
    # code in any classes that implement this class
    @classmethod
    def readFromValueType(self, stream, valueType):
        match valueType:
            case Types.BOOLEAN:
                return bool(stream.readInt8())
            case Types.INT32:
                return stream.readInt32()
            case Types.FLOAT:
                return stream.readFloat()
            case Types.STRING:
                length = stream.readInt32(False)
                return stream.readString(length)
            case Types.WIDE_STRING:
                #TODO: Make this use UTF16
                length = stream.readInt32(False)
                return stream.readString(length)
            case Types.BYTE_ARRAY:
                length = stream.readInt32(False)
                return stream.readBytes(length)
            case Types.UINT32:
                return stream.readInt32(False)
            case Types.KEYED_ARCHIVE:
                length = stream.readInt32(False)
                buffer = BytesIO(stream.readBytes(length))
                buffer = FileBuffer(buffer)
                return KAReader.readFromBuffer(buffer)
            case Types.INT64:
                return stream.readInt64()
            case Types.UINT64:
                return stream.readInt64(False)
            case Types.VECTOR2:
                return np.array([
                    stream.readFloat(), stream.readFloat()
                ])
            case Types.VECTOR3:
                return np.array([
                    stream.readFloat(), stream.readFloat(), stream.readFloat()
                ])
            case Types.VECTOR4:
                return np.array([
                    stream.readFloat(), stream.readFloat(), stream.readFloat(), stream.readFloat()
                ])
            case Types.MATRIX2:
                return np.matrix([
                    [stream.readFloat(), stream.readFloat()],
                    [stream.readFloat(), stream.readFloat()]
                ])
            case Types.MATRIX3:
                return np.matrix([
                    [stream.readFloat(), stream.readFloat(), stream.readFloat()],
                    [stream.readFloat(), stream.readFloat(), stream.readFloat()],
                    [stream.readFloat(), stream.readFloat(), stream.readFloat()]
                ])
            case Types.MATRIX4:
                return np.matrix([
                    [stream.readFloat(), stream.readFloat(), stream.readFloat(), stream.readFloat()],
                    [stream.readFloat(), stream.readFloat(), stream.readFloat(), stream.readFloat()],
                    [stream.readFloat(), stream.readFloat(), stream.readFloat(), stream.readFloat()],
                    [stream.readFloat(), stream.readFloat(), stream.readFloat(), stream.readFloat()]
                ])
            case Types.COLOR:
                return np.array([
                    stream.readFloat(), stream.readFloat(), stream.readFloat(), stream.readFloat() #RGBA
                ])
            case Types.FASTNAME:
                length = stream.readInt32(False)
                return stream.readString(length)
            case Types.AABBOX3:
                minimum = DataReader.readVector3(stream)
                maximum = DataReader.readVector3(stream)
                return AABBox3(minimum, maximum)
            case Types.FILEPATH:
                length = stream.readInt32(False)
                return stream.readString(length)
            case Types.FLOAT64:
                return stream.readDouble()
            case Types.INT8:
                return stream.readInt8()
            case Types.UINT8:
                return stream.readInt8(False)
            case Types.INT16:
                return stream.readInt16()
            case Types.UINT16:
                return stream.readInt16(False)
            case Types.ARRAY:
                length = stream.readInt32(False)
                array = []
                for _ in range(length):
                    array.append(self.readValue(stream))
                return array
            case other:
                raise ReadError("KA.KAReader.V1DataReader", f"Unknown data type of id: {valueType}")

class V2DataReader:
    @staticmethod
    def readStringTable(stream, count):
        # Read strings
        strings = []
        for _ in range(count):
            length = stream.readInt32(False)
            string = stream.readString(length)
            strings.append(string)

        # Read keys and form table
        stringTable = {}
        for stringI in range(count):
            key = stream.readInt32(False)
            stringTable[key] = string[stringI]

        return stringTable

class V258DataReader(V1DataReader):
    @staticmethod
    def readValue(stream):
        valueType = stream.readInt8(False)
        match valueType:
            case Types.STRING:
                return stream.readInt32(False)
            case Types.WIDE_STRING:
                return stream.readInt32(False)
            case Types.FASTNAME:
                return stream.readInt32(False)
            case Types.FILEPATH:
                return stream.readInt32(False)
            case other:
                return super().readFromValueType(stream, valueType)
