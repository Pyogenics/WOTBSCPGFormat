'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from .KA import *
from ..FileIO import FileBuffer
from ..ErrorWrappers import ReadError

from io import BytesIO
from collections.abc import Mapping

# Class to read keys/values from v1 KAs
class V1DataReader:
    @staticmethod
    def readValue(stream):
        valueType = stream.readInt8(False)

        #TODO: Maybe we should use numpy for some types?
        #XXX: Most of this is untested code
        match valueType:
            case Types.NONE.value:
                return None
            case Types.BOOLEAN.value:
                return bool(stream.readInt8())
            case Types.INT8.value:
                return stream.readInt8()
            case Types.UINT8.value:
                return stream.readInt8(False)
            case Types.INT16.value:
                return stream.readInt16()
            case Types.UINT16.value:
                return stream.readInt16(False)
            case Types.INT32.value:
                return stream.readInt32()
            case Types.UINT32.value:
                return stream.readInt32(False)
            case Types.FLOAT.value:
                return stream.readFloat()
            case Types.FLOAT64.value:
                return stream.readDouble()
            case Types.STRING.value:
                length = stream.readInt32(False)
                return stream.readString(length)
            case Types.WIDE_STRING.value:
                length = stream.readInt32(False) * 2 # UTF-16 is double the size
                value = stream.readBytes(length)
                value = value.decode("utf-16le")
                return value
            case Types.BYTE_ARRAY.value:
                length = stream.readInt32(False)
                return stream.readBytes(length)
            case Types.KEYED_ARCHIVE.value:
                length = stream.readInt32(False)
                value = BytesIO(stream.readBytes(length))
                value = FileBuffer(value)
                return KAReader.readFromBuffer(value)
            case Types.INT64.value:
                return stream.readInt64()
            case Types.UINT64.value:
                return stream.readInt64(False)
            case Types.VECTOR2.value:
                value = (
                    stream.readFloat(),
                    stream.readFloat()
                )
                return value
            case Types.VECTOR3.value:
                value = (
                    stream.readFloat(),
                    stream.readFloat(),
                    stream.readFloat()
                )
                return value
            case Types.VECTOR4.value:
                value = (
                    stream.readFloat(),
                    stream.readFloat(),
                    stream.readFloat(),
                    stream.readFloat()
                )
                return value
            case Types.MATRIX2.value:
                raise ReadError("V1DataReader", "Unimplemented type MATRIX2") #TODO
            case Types.MATRIX3.value:
                raise ReadError("V1DataReader", "Unimplemented type MATRIX3") #TODO
            case Types.MATRIX4.value:
                raise ReadError("V1DataReader", "Unimplemented type MATRIX4") #TODO
            case Types.COLOR.value:
                value = (
                    stream.readFloat(), # r
                    stream.readFloat(), # g
                    stream.readFloat(), # b
                    stream.readFloat()  # a
                )
                return value
            case Types.FASTNAME.value:
                length = stream.readInt32(False)
                value = stream.readString(length)
                return value
            case Types.AABBOX3.value:
                raise ReadError("V1DataReader", "Unimplemented type AABBOX3") #TODO
            case Types.FILEPATH.value:
                length = stream.readInt32(False)
                value = stream.readString(length)
                return value
            case other:
                raise ReadError("V1DataReader", f"Unknown data type of id: {valueType}")

class V2DataReader:
    @staticmethod
    def readValue(stream):
        length = stream.readInt16(False)
        return stream.readString(length)

    def readHierarchyValue(stream):
        return V258DataReader.readValue(stream)

# Practically like v1
class V258DataReader:
    @staticmethod
    def readKey(stream):
        key = V258UnresolvedString(stream.readInt32(False))
        return key

    @staticmethod
    def resolveStrings(stringTable, ka):
        resolvedKa = {}
        for key, value in ka.items():
            if isinstance(key, V258UnresolvedString):
                key = stringTable[key.stringTableIndex]
            if isinstance(value, V258UnresolvedString):
                value = stringTable[value.stringTableIndex]
            elif isinstance(value, Mapping):
                # Resolve nested KA
                value = V258DataReader.resolveStrings(stringTable, value)

            resolvedKa[key] = value

        return resolvedKa

    @staticmethod
    def readValue(stream):
        valueType = stream.readInt8(False)

        #TODO: Maybe we should use numpy for some types?
        #XXX: Most of this is untested code
        match valueType:
            case Types.NONE.value:
                return None
            case Types.BOOLEAN.value:
                return bool(stream.readInt8())
            case Types.INT8.value:
                return stream.readInt8()
            case Types.UINT8.value:
                return stream.readInt8(False)
            case Types.INT16.value:
                return stream.readInt16()
            case Types.UINT16.value:
                return stream.readInt16(False)
            case Types.INT32.value:
                return stream.readInt32()
            case Types.UINT32.value:
                return stream.readInt32(False)
            case Types.FLOAT.value:
                return stream.readFloat()
            case Types.FLOAT64.value:
                return stream.readDouble()
            case Types.STRING.value:
                stringTableIndex = stream.readInt32(False)
                return V258UnresolvedString(stringTableIndex)
            case Types.WIDE_STRING.value:
                stringTableIndex = stream.readInt32(False)
                return V258UnresolvedString(stringTableIndex)
            case Types.BYTE_ARRAY.value:
                length = stream.readInt32(False)
                return stream.readBytes(length)
            case Types.KEYED_ARCHIVE.value:
                length = stream.readInt32(False)
                value = BytesIO(stream.readBytes(length))
                value = FileBuffer(value)
                return KAReader.readFromBuffer(value)
            case Types.INT64.value:
                return stream.readInt64()
            case Types.UINT64.value:
                return stream.readInt64(False)
            case Types.VECTOR2.value:
                value = (
                    stream.readFloat(),
                    stream.readFloat()
                )
                return value
            case Types.VECTOR3.value:
                value = (
                    stream.readFloat(),
                    stream.readFloat(),
                    stream.readFloat()
                )
                return value
            case Types.VECTOR4.value:
                value = (
                    stream.readFloat(),
                    stream.readFloat(),
                    stream.readFloat(),
                    stream.readFloat()
                )
                return value
            case Types.MATRIX2.value:
                raise ReadError("V258DataReader", "Unimplemented type MATRIX2") #TODO
            case Types.MATRIX3.value:
                raise ReadError("V258DataReader", "Unimplemented type MATRIX3") #TODO
            case Types.MATRIX4.value:
                raise ReadError("V258DataReader", "Unimplemented type MATRIX4") #TODO
            case Types.COLOR.value:
                value = (
                    stream.readFloat(), # r
                    stream.readFloat(), # g
                    stream.readFloat(), # b
                    stream.readFloat()  # a
                )
                return value
            case Types.FASTNAME.value:
                stringTableIndex = stream.readInt32(False)
                return V258UnresolvedString(stringTableIndex)
            case Types.AABBOX3.value:
                #TODO: This is a quick solution to get SC2 reads working
                value = [
                    stream.readFloat(), stream.readFloat(), stream.readFloat(),
                    stream.readFloat(), stream.readFloat(), stream.readFloat()
                ]
                return value
                #raise ReadError("V258DataReader", "Unimplemented type AABBOX3") #TODO
            case Types.FILEPATH.value:
                stringTableIndex = stream.readInt32(False)
                return V258UnresolvedString(stringTableIndex)
            case Types.ARRAY.value:
                print("Reading array")
                length = stream.readInt32(False)
                members = []
                for _ in range(length):
                    member = V258DataReader.readValue(stream)
                    members.append(member)
                return members
            case other:
                print(stream.tell())
                raise ReadError("V258DataReader", f"Unknown data type of id: {valueType}")

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
