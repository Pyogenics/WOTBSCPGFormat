'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

'''
Primitive data readers
'''
class V1DataReader:
    @classmethod
    def readPair(self, stream):
        key = self.readValue(
            stream, stream.readInt8(False)
        )
        value = self.readValue(
            stream, stream.readInt8(False)
        )

        return (key, value)

    @classmethod
    def readValue(self, stream, valueType):
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
                raise KAReadError(f"Unknown data type id: {valueType}")

'''
Errors
'''
class KAReadError(RuntimeError): pass
class KAWriteError(RuntimeError): pass

'''
KA Readers
'''
def readKAHeader(stream):
    if stream.readBytes(2) != b"KA":
        raise KAReadError("Invalid magic string")

    version = stream.readInt32(False)
    nodeCount = stream.readInt32(False)
    stream.readInt32(False) #TODO: duplicate of node count?

    return (version, nodeCount)

def readKA1(stream): pass
    version, nodeCount = readKAHeader(stream)
    if version != 1:
        raise KAReadError(f"Version mismatch: expected 1 but got {version}")
    elif nodeCount == 0:
        return {}

    archive = {}
    for _ in range(nodeCount):
        key, value = V1DataReader.readPair(stream)
        archive[key] = value

    return archive

def readKA2(stream):
    version, stringCount = readKAHeader(stream)
    if version != 2:
        raise KAReadError(f"Version mismatch: expected 2 but got {version}")
    elif stringCount == 0:
        return {}

    strings = []
    for _ in range(nodeCount):
        length = stream.readInt16(False)
        strings.append(
            stream.readString(length)
        )

    stringTable = {}
    for stringI in range(nodeCount):
        key = stream.readInt32(False)
        stringTable[key] = strings[stringI]

    archiveNodeCount = stream.readInt32(False)

    archive = {}
    for _ in range(archiveNodeCount):
        key, value = V2DataReader.readPair(stream, stringTable)
        archive[key] = value
    

def readKA258(stream, stringTable): pass

'''
KA Writers
'''
def writeKAHeader(stream): pass

def writeKA1(stream): pass

def writeKA2(stream): pass

def writeKA258(stream): pass
