'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import bpy
from bpy.types import Operator
from bpy.props import (StringProperty,
                       CollectionProperty)
from bpy_extras.io_utils import ImportHelper, ExportHelper

from enum import Enum

bl_info = {
    "name": "DAVA Scene File v2 format",
    "description": "Support for DAVA framework scene files",
    "author": "Pyogenics, https://www.github.com/Pyogenics",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "File > Import-Export",
    "doc_url": "https://github.com/Pyogenics/SCPG-reverse-engineering",
    "tracker_url": "https://github.com/Pyogenics/SCPG-reverse-engineering/issues",
    "category": "Import-Export"
}

class ImportError(RuntimeError): pass

'''
IO drivers
'''
class DescriptorFileTypes(Enum):
    NONE = -1
    SceneFile = 0
    ModelFile = 1

class KeyedArchiveTypes(Enum):
    #TODO: Get actual values for these, using placeholders for now
    NONE = 0
    BOOLEAN = 1
    INT32 = 2
    FLOAT = 3
    STRING = 35 #
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

    def readValue(self, stream):
        valueType = int.from_bytes(stream.read(1))

        # read value
        match valueType:
            case KeyedArchiveTypes.STRING:
                length = stream.read(4)
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
        '''TODO: Version two archives exist!
        if version != 1:
            raise ImportError(f"Invalid keyed archive version: '{version}', version isn't '1'")
        el'''
        if itemCount == 0:
            return

        self.version = version
        self.itemCount = itemCount

        # Read items
        for _ in range(itemCount):
            key = self.readValue(stream)
            value = self.readValue(stream)

            self.items[key] = value

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

class SC2Exporter:
    pass

'''
UI
'''
class ImportSC2(Operator, ImportHelper):
    bl_idname = "import_scene.sc2"
    bl_label = "Import DAVA scene"
    bl_description = "Import a DAVA scene file"

    filter_glob: StringProperty(default="*.sc2", options={'HIDDEN'})

    files: CollectionProperty(name="File Path", type=bpy.types.OperatorFileListElement)

    def invoke(self, context, event):
        return ImportHelper.invoke(self, context, event)

    def execute(self, context):
        # import
        importer = SC2Importer()
        with open(self.filepath, "rb") as f:
            importer.importFromFileStream(f)
            self.report({"INFO"}, f"V{importer.version} Nc{importer.nodeCount}")

        return {"FINISHED"}

class ExportSC2(Operator, ExportHelper):
    bl_idname = "export_scene.sc2"
    bl_label = "Export DAVA scene"
    bl_description = "Export a DAVA scene file"

    def execute(self, context):
        return {'FINISHED'}

def menu_func_import_sc2(self, context):
    self.layout.operator(ImportSC2.bl_idname, text="DAVA scene file v2 (.sc2)")

def menu_func_export_sc2(self, context):
    self.layout.operator(ExportSC2.bl_idname, text="DAVA scene file v2 (.sc2)")

'''
Register
'''
classes = {
    ExportSC2,
    ImportSC2
}

def register():
    # Register classes
    for c in classes:
        bpy.utils.register_class(c)
    # File > Import-Export
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_sc2)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_sc2)

def unregister():
    # Unregister classes
    for c in classes:
        bpy.utils.unregister_class(c)
    # Remove `File > Import-Export`
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_sc2)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_sc2)

if __name__ == "__main__":
    register()
