'''
Copyright (C) 2023  Pyogenics <https://github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from enum import Enum

from common import ImportError

class Types(Enum):
    #TODO: Get actual values for these, using placeholders for now
    NONE = 0
    BOOLEAN = 1
    INT32 = 2
    FLOAT = 3
    STRING = 4
    WIDE_STRING = 5
    BYTE_ARRAY = 6
    UINT32 = 7
    KEYED_ARCHIVE = 8
    INT64 = 9
    UINT64 = 10
    VECTOR2 = 11
    VECTOR3 = 12
    VECTOR4 = 13
    MATRIX2 = 14
    MATRIX3 = 15
    MATRIX4 = 16
    COLOR = 17
    FASTNAME = 18
    AABBOX3 = 19
    FILEPATH = 20
    FLOAT64 = 21
    INT8 = 22
    UINT8 = 23
    INT16 = 24
    UINT16 = 25
    COUNT = 26

class KeyedArchive:
    items = {}

    def readBoolean(self, stream):
        value = int.from_bytes(stream.read(1))
        return bool(value)

    def readInt8(self, stream):
        value = int.from_bytes(stream.read(1))
        return value

    def readUInt8(self, stream):
        value = int.from_bytes(stream.read(1), True)
        return value

    def readInt16(self, stream):
        value = int.from_bytes(stream.read(2), "little")
        return value

    def readUInt16(self, stream):
        value = int.from_bytes(stream.read(2), "little", True)
        return value

    def readInt32(self, stream):
        value = int.from_bytes(stream.read(4), "little")
        return value

    def readUInt32(self, stream):
        value = int.from_bytes(stream.read(4), "little", True)
        return value

    def readValue(self, stream):
        valueType = int.from_bytes(stream.read(1))

        # read value
        match valueType:
            case Types.NONE.value:
                value = stream.read(4) #XXX: Take a wild guess
                return value
            case Types.BOOL.value:
                return self.readBoolean(stream)
            case Types.INT32.value:
                return self.readInt32(stream)
            case Types.FLOAT.value:
                return self.readFloat(stream)
            case Types.STRING.value:
                length = int.from_bytes(stream.read(4), "little")
                raise ImportError(f"l{length}")
                string = stream.read(length)
                return string
            case other:
                raise ImportError(f"Unknown type {str(valueType)} @ {stream.tell()}")

    def loadFromFileStream(self, stream):
        # Check magic
        if (stream.read(2) != b"KA"):
            raise ImportError(f"Invalid keyed archive magic @ {stream.tell()}! Is the file corrupted?") #XXX: Potentially unhandled functionality

        # Read header
        version = int.from_bytes(stream.read(2), "little")
        itemCount = int.from_bytes(stream.read(4), "little")
        print(f"KA version: {version} count: {itemCount}")
        if version != 1:
            raise ImportError(f"Invalid keyed archive version: '{version}', version isn't '1', we don't implement version 2 yet!")
        elif itemCount == 0:
            return

        self.version = version
        self.itemCount = itemCount

        # Read items
        for _ in range(itemCount):
            key = self.readValue(stream)
            value = self.readValue(stream)

            self.items[key] = value

        raise ImportError(self.items)
