'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from struct import unpack, pack

# Utility class that provides a nice
# abstraction for common binary IO tasks
class FileBuffer:
    def __init__(self, stream, endian="little"):
        self.stream = stream
        self.endian = endian

    '''
    io passthrough functions
    '''
    def tell(self):
        return self.stream.tell()

    def seek(self, offset, mode):
        self.stream.seek(offset, mode)

    '''
    Int functions
    '''
    def readInt8(self, signed=True):
        value = self.stream.read(1)
        value = int.from_bytes(value, byteorder=self.endian, signed=signed)
        return value

    def readInt16(self, signed=True):
        value = self.stream.read(2)
        value = int.from_bytes(value, byteorder=self.endian, signed=signed)
        return value

    def readInt32(self, signed=True):
        value = self.stream.read(4)
        value = int.from_bytes(value, byteorder=self.endian, signed=signed)
        return value

    def readInt64(self, signed=True):
        value = self.stream.read(8)
        value = int.from_bytes(value, byteorder=self.endian, signed=signed)
        return value

    def writeInt8(self, value):
        binData = value.to_bytes(1)
        self.stream.write(binData)

    def writeInt16(self, value):
        binData = value.to_bytes(2, self.endian)
        self.stream.write(binData)

    def writeInt32(self, value):
        binData = value.to_bytes(4, self.endian)
        self.stream.write(binData)

    def writeInt64(self, value):
        binData = value.to_bytes(8, self.endian)
        self.stream.write(binData)

    '''
    Decimal
    '''
    def readFloat(self):
        value = self.stream.read(4)
        value = unpack("f", value)
        (value,) = value
        return value

    def writeFloat(self, value):
        binData = bytearray(pack("f", value))
        self.stream.write(binData)

    def readDouble(self):
        value = self.stream.read(8)
        value = unpack("d", value)
        (value,) = value
        return value

    def writeFloat(self, value):
        binData = bytearray(pack("d", value))
        self.stream.write(binData)

    '''
    String
    '''
    def readString(self, count):
        value = self.stream.read(count)
        value = value.decode("utf-8")
        return value

    def writeString(self, value):
        binData = bytearray(value, "utf-8")
        self.stream.write(binData)

    '''
    Binary
    '''
    def readBytes(self, count):
        value = self.stream.read(count)
        return value

    def writeBytes(self, value):
        self.stream.write(value)
