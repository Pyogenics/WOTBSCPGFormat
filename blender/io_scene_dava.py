'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import bmesh
import bpy
from bpy.types import Operator
from bpy.props import (StringProperty,
                       CollectionProperty)
from bpy_extras.io_utils import ImportHelper, ExportHelper

from enum import Enum
from struct import unpack
from io import BytesIO

bl_info = {
    "name": "DAVA Scene File format",
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
        value = int.from_bytes(stream.read(1), signed=True)
        return value

    def readInt16(self, stream):
        value = int.from_bytes(stream.read(2), "little")
        return value

    def readUInt16(self, stream):
        value = int.from_bytes(stream.read(2), "little", signed=True)
        return value

    def readInt32(self, stream):
        value = int.from_bytes(stream.read(4), "little")
        return value

    def readUInt32(self, stream):
        value = int.from_bytes(stream.read(4), "little", signed=True)
        return value

    def readFloat(self, stream):
        value = unpack("f", stream.read(4))
        return value

    def readFloat64(self, stream):
        value = unpack("f", stream.read(8))
        return value

    def readString(self, stream):
        length = self.readUInt32(stream)
        value = stream.read(length)
        return value.decode("utf-8")

    def readWideString(self, stream):
        length = self.readUInt32(stream)
        value = stream.read(lenght*2)
        return value.decode("utf-16") #XXX: Maybe?

    def readByteArray(self, stream):
        length = self.readUInt32(stream)
        value = stream.read(length)
        return value

    def readKeyedArchive(self, stream):
        length = self.readUInt32()
        value = KeyedArchive()
        value.loadFromFileStream(stream)
        return value

    def readInt64(self, stream):
        value = int.from_bytes(stream.read(8), "little")
        return value

    def readUInt64(self, stream):
        value = int.from_bytes(stream.read(8), "little", signed=True)
        return value

    def readValue(self, stream):
        valueType = int.from_bytes(stream.read(1))

        # read value
        match valueType:
            case Types.NONE.value:
                return None
            case Types.BOOLEAN.value:
                return self.readBoolean(stream)
            case Types.INT8.value:
                return self.readInt8(stream)
            case Types.UINT8.value:
                return self.readUInt8(stream)
            case Types.INT16.value:
                return self.readInt16(stream)
            case Types.UINT16.value:
                return self.readUInt16(stream)
            case Types.INT32.value:
                return self.readInt32(stream)
            case Types.UINT32.value:
                return self.readUInt32(stream)
            case Types.FLOAT.value:
                return self.readFloat(stream)
            case Types.FLOAT64.value:
                return self.readFloat64(stream)
            case Types.STRING.value:
                return self.readString(stream)
            case Types.WIDE_STRING.value:
                return self.readWideString(stream)
            case Types.BYTE_ARRAY.value:
                return self.readByteArray(stream)
            case Types.KEYED_ARCHIVE.value:
                return self.readKeyedArchive(stream)
            case Types.INT64.value:
                return self.readInt64(stream)
            case Types.UINT64.value:
                return self.readUInt64(stream)
            case other:
                raise ImportError(f"Unknown type {str(valueType)} @ {stream.tell()}")

    def loadFromFileStream(self, stream):
        print(f"KA entered at: {stream.tell()}")
        # Check magic
        if (stream.read(2) != b"KA"):
            raise ImportError(f"Invalid keyed archive magic @ {stream.tell()}! Is the file corrupted?") #XXX: Potentially unhandled functionality

        # Read header
        version = int.from_bytes(stream.read(2), "little")
        itemCount = int.from_bytes(stream.read(4), "little")
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

class vertexTypes(Enum):
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

class SCGImporter:
    vertices = []
    meshes = []

    def parseVertexFormat(self, fmt):
        stride = 0
        
        if (fmt & vertexTypes.VERTEX.value):
            stride += 3 * 4
        if (fmt & vertexTypes.NORMAL.value):
            stride += 3 * 4
        if (fmt & vertexTypes.COLOR.value):
            stride += 4
        if (fmt & vertexTypes.TEXCOORD0.value):
            stride += 2 * 4
        if (fmt & vertexTypes.TEXCOORD1.value):
            stride += 2 * 4
        if (fmt & vertexTypes.TEXCOORD2.value):
            stride += 2 * 4
        if (fmt & vertexTypes.TEXCOORD3.value):
            stride += 2 * 4

        if (fmt & vertexTypes.TANGENT.value):
            stride += 3 * 4
        if (fmt & vertexTypes.BINORMAL.value):
            stride += 3 * 4
        if (fmt & vertexTypes.HARD_JOINTINDEX.value):
            stride += 4

        if (fmt & vertexTypes.CUBETEXCOORD0.value):
            stride += 3 * 4
        if (fmt & vertexTypes.CUBETEXCOORD1.value):
            stride += 3 * 4
        if (fmt & vertexTypes.CUBETEXCOORD2.value):
            stride += 3 * 4
        if (fmt & vertexTypes.CUBETEXCOORD3.value):
            stride += 3 * 4

        if (fmt & vertexTypes.PIVOT4.value):
            stride += 4 * 4
        if (fmt & vertexTypes.FLEXIBILITY.value):
            stride += 4
        if (fmt & vertexTypes.ANGLE_SIN_COS.value):
            stride += 2 * 4

        if (fmt & vertexTypes.JOINTINDEX.value):
            stride += 4 * 4
        if (fmt & vertexTypes.JOINTWEIGHT.value):
            stride += 4 * 4

        return stride

    def parsePolygonGroup(self, node):
        # Parse vertex format
        stride = self.parseVertexFormat(node["vertexFormat"])

        #TODO: handle: primitive count, cube texture coords (https://github.com/smile4u/dava.engine/blob/development/Sources/Internal/Render/3D/PolygonGroup.cpp#L173)

        # Carve out vertex data
        vertices = node["vertices"]
        logicalSize = stride * node["vertexCount"]
        realSize = len(vertices)
        if node["packing"] != 0:
            raise ImportError("Vertex packing isn't PACKING_NONE!")
        elif logicalSize != realSize:
            raise ImportError(f"Invalid vertex array size, logical: {size} real: {len(vertices)}")
        elif len(vertices) < 1:
            raise ImportError(f"No vertices in this PolygonGroup")

        stream = BytesIO(vertices)
        vertices = []
        for _ in range(node["vertexCount"]):
            xyz = unpack("fff", stream.read(12))

            #TODO: actually handle the other data
            stream.read(stride - 3*4)

            vertices.append(xyz)

        self.meshes.append({"vertices": vertices, "indices": node["indices"]})

    def importFromFileStream(self, stream):
        # Verify magic
        if stream.read(4) != b"SCPG":
            raise ImportError("Invalid header magic")

        # Read header
        version = int.from_bytes(stream.read(4), "little")
        nodeCount = int.from_bytes(stream.read(4), "little")
        nodeCount_two = int.from_bytes(stream.read(4), "little") # This probably is a different type of node?

        self.version = version

        # Read nodes
        nodes = []
        for i in range(nodeCount):
            print(f"Reading node {i} at {stream.tell()}")
            node = KeyedArchive()
            node.loadFromFileStream(stream)
            print(f"@ {stream.tell()}")
            nodes.append(node)

        # Parse nodes
        for node in nodes:
            print(node)
            if node.items["##name"] == "PolygonGroup":
                self.parsePolygonGroup(node.items)

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

    filter_glob: StringProperty(default="*.scg", options={'HIDDEN'})

    files: CollectionProperty(name="File Path", type=bpy.types.OperatorFileListElement)

    def createBMesh(self, vertices, indices):
        bm = bmesh.new()
        for index in indices:
            #raise ImportError(f"{vertices[0:30]}")
            #try:
            bm.verts.new(vertices[index])
            #except:
            #    raise ImportError(f"Out of range: {index}, actual range: {len(vertices)}")
        return bm

    def invoke(self, context, event):
        return ImportHelper.invoke(self, context, event)

    def execute(self, context):
        # import
        importer = SCGImporter()
        with open(self.filepath, "rb") as f:
            importer.importFromFileStream(f)
            self.report({"INFO"}, f"Loaded {len(importer.meshes)} meshes")

            collection = bpy.data.collections.new("dava")
            # Create meshes and add to scene
            for meshData in importer.meshes:
                vertices = meshData["vertices"]
                elementArray = []
                for index in meshData["indices"]:
                    elementArray.append(vertices[index])
                mesh = bpy.data.meshes.new("mesh")
                mesh.from_pydata(elementArray, [], [])
                mesh.update()
                obj = bpy.data.objects.new("object", mesh)
                collection.objects.link(obj)

            bpy.context.scene.collection.children.link(collection)


        return {"FINISHED"}

class ExportSC2(Operator, ExportHelper):
    bl_idname = "export_scene.sc2"
    bl_label = "Export DAVA scene"
    bl_description = "Export a DAVA scene file"

    def execute(self, context):
        return {'FINISHED'}

def menu_func_import_sc2(self, context):
    self.layout.operator(ImportSC2.bl_idname, text="DAVA scene file (.sc2/.scg)")

def menu_func_export_sc2(self, context):
    self.layout.operator(ExportSC2.bl_idname, text="DAVA scene file (.sc2/scg)")

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
