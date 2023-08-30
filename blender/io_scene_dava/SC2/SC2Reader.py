'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from ..ErrorWrappers import ReadError
from ..KA.KAReader import KAReader

from enum import Enum

class DescriptorFileTypes(Enum):
    NONE = -1
    SceneFile = 0
    ModelFile = 1

class SC2Reader:
    @staticmethod
    def readDataNodes(stream, count):
        for _ in range(count):
            node = KAReader.readFromBuffer(stream)
            print(node)

    @staticmethod
    def readFromBuffer(stream):
        # Check magic
        if stream.readString(4) != "SFV2":
            raise ReadError("SC2Reader", "Invalid magic stream")

        # Read header
        version = stream.readInt32(False)
        nodeCount = stream.readInt32(False)

        print(f"KA version: {version}, nodes: {nodeCount}")

        # Read version tags
        versionTags = {}
        if version >= 14:
            versionTags = KAReader.readFromBuffer(stream)
        print(f"KA version tags: {versionTags}")

        # Read descriptor
        descriptorSize = 0
        descriptorFileType = DescriptorFileTypes.NONE
        descriptorUnknowns = b""
        if version >= 10:
            descriptorSize = stream.readInt32(False)
            descriptorFileType = stream.readInt32(False)
            descriptorUnknowns = stream.readBytes(descriptorSize - 8)
        print(f"KA descriptor size: {descriptorSize}, type: {descriptorFileType}, unknowns: {descriptorUnknowns}")

        # Read data nodes
        if version >= 2:
            dataNodeCount = stream.readInt32(False) #TODO: There is something very wrong with this number
            print("KA data node count: {dataNodeCount}")
            SC2Reader.readDataNodes(stream, dataNodeCount)
