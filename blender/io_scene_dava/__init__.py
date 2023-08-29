'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

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

import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper

from os.path import basename

from .FileIO import FileBuffer
from .SCG.SCGReader import SCGReader

'''
Operators
'''
class ImportSCG(Operator, ImportHelper):
    bl_idname = "import_scene.scg"
    bl_label = "Import DAVA geometry"
    bl_description = "Import a DAVA geometry file"

    filter_glob: StringProperty(default="*.scg", options={'HIDDEN'})

    def invoke(self, context, event):
        return ImportHelper.invoke(self, context, event)

    def execute(self, context):
        filepath = self.filepath
        filename = basename(filepath).split(".")[0]
        print(f"Importing DAVA geometry from {filepath}")

        with open(filepath, "rb") as f:
            stream = FileBuffer(f)
            geometry = SCGReader.readFromBuffer(stream)

            # Add geometry to scene
            collection = bpy.data.collections.new(filename)
            for groupId, polyGroup in geometry.polygonGroups.items():
                mesh = bpy.data.meshes.new("mesh")
                mesh.from_pydata(polyGroup.vertices.VERTEX, polyGroup.edges, polyGroup.faces)
                mesh.update()

                obj = bpy.data.objects.new(f"PolygonGroup{groupId}", mesh)
                collection.objects.link(obj)
            bpy.context.scene.collection.children.link(collection)
            self.report({"INFO"}, f"Loaded {len(geometry.polygonGroups)} polygon groups")

        return {"FINISHED"}

class ExportSCG(Operator, ExportHelper):
    bl_idname = "export_scene.scg"
    bl_label = "Export DAVA geometry"
    bl_description = "Export a DAVA geometry file"

    filter_glob: StringProperty(default="*.scg", options={'HIDDEN'})
    filename_ext: StringProperty(default=".scg", options={'HIDDEN'})

    def invoke(self, context, event):
        return ExportHelper.invoke(self, context, event)

    def execute(self, context):
        filepath = self.filepath
        print(f"Exporting DAVA geometry to {filepath}")
        return {'FINISHED'}

'''
Menu
'''
def menu_func_import_scg(self, context):
    self.layout.operator(ImportSCG.bl_idname, text="DAVA scene geometry (.scg)")

def menu_func_export_scg(self, context):
    self.layout.operator(ExportSCG.bl_idname, text="DAVA scene geometry (.scg)")

'''
Register
'''
classes = {
    ExportSCG,
    ImportSCG
}

def register():
    # Register classes
    for c in classes:
        bpy.utils.register_class(c)
    # File > Import-Export
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_scg)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_scg)

def unregister():
    # Unregister classes
    for c in classes:
        bpy.utils.unregister_class(c)
    # Remove `File > Import-Export`
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_scg)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_scg)
