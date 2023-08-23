'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from .blError import ImportError
from .KeyedArchiveIO import KeyedArchive

from enum import Enum

class DescriptorFileTypes(Enum):
    NONE = -1
    SceneFile = 0
    ModelFile = 1

class SC2Importer:
    def readDataNodes(self, stream, count):
        for _ in range(count):
            node = KeyedArchive()
            node.loadFromFileStream(stream)

    def importFromFileStream(self, stream):
        # Check magic
        if stream.read(4) != b"SFV2":
            raise ImportError("Invalid magic! Are you sure this is a Scene File v2?")

        # Read header
        version = int.from_bytes(stream.read(4), "little")
        nodeCount = int.from_bytes(stream.read(4), "little")

        self.version = version
        self.nodeCount = nodeCount

        # Read version tags
        versionTags = {}
        if version >= 14:
            versionTagsArchive = KeyedArchive()
            versionTagsArchive.loadFromFileStream(stream)
            versionTags = versionTagsArchive.items

        # Read descriptor
        descriptorSize = 0
        descriptorFileType = DescriptorFileTypes.NONE
        if version >= 10:
            descriptorSize = int.from_bytes(stream.read(4), "little")
            descriptorFileType = int.from_bytes(stream.read(4), "little")
            unknownField = int.from_bytes(stream.read(4), "little") #TODO: Investigate this

        # Read data nodes
        if version >= 2:
            dataNodeCount = int.from_bytes(stream.read(4), "little")
            self.readDataNodes(stream, dataNodeCount)
