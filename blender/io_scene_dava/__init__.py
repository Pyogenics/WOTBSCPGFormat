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

from .FileIO.StreamBuffer import StreamBuffer
from .FileIO.SCG import readSCG
from .Geometry.PolygonGroup import PrimitiveTypes, PolygonGroup

'''
Operators
'''
class ImportDAVA(Operator, ImportHelper):
    bl_idname = "import_scene.scg"
    bl_label = "Import DAVA geometry"
    bl_description = "Import a DAVA scene file"

    filter_glob: StringProperty(default="*.scg", options={'HIDDEN'})

    def invoke(self, context, event):
        return ImportHelper.invoke(self, context, event)

    # Just import SCG whilst we get proper full imports working
    def execute(self, context):
        filepath = self.filepath
        print(f"Importing DAVA scene from {filepath}")
        
        with open(filepath, "rb") as scg:
            polyGroups = readSCG(
                StreamBuffer(scg)
            )

            # Parse polygon groups
            for groupID in polyGroups.keys():
                polyGroups[groupID] = PolygonGroup( polyGroups[groupID] )

            # Add polygon groups to scene
            collection = bpy.data.collections.new("DAVAMesh")
            for groupID in polyGroups.keys():
                group = polyGroups[groupID]
                mesh = bpy.data.meshes.new("mesh")

                if group.primitiveType == PrimitiveTypes.TRIANGLELIST:
                    mesh.from_pydata(group.vertices, [], group.getTriangleList())
                elif group.primitiveType == PrimitiveTypes.TRIANGLESTRIP:
                    mesh.from_pydata(group.vertices, [], group.getTriangleStrip())
                elif group.primitiveType == PrimitiveTypes.LINELIST:
                    mesh.from_pydata(group.vertices, group.getLineList(), [])
                mesh.update()

                obj = bpy.data.objects.new(f"PolygonGroup{groupID}", mesh)
                collection.objects.link(obj)
            bpy.context.scene.collection.children.link(collection)
            self.report({"INFO"}, f"Loaded {len(polyGroups)} polygon groups")

        return {"FINISHED"}

class ExportDAVA(Operator, ExportHelper):
    bl_idname = "export_scene.sc2"
    bl_label = "Export DAVA geometry"
    bl_description = "Export a scene file"

    filter_glob: StringProperty(default="*.sc2", options={'HIDDEN'})
    filename_ext: StringProperty(default=".sc2", options={'HIDDEN'})

    def invoke(self, context, event):
        return ExportHelper.invoke(self, context, event)

    def execute(self, context):
        filepath = self.filepath
        print(f"Exporting DAVA scene to {filepath}")
        return {'FINISHED'}

'''
Menu
'''
def menu_func_import_dava(self, context):
    self.layout.operator(ImportDAVA.bl_idname, text="DAVA scene (.sc2/.scg)")

def menu_func_export_dava(self, context):
    self.layout.operator(ExportDAVA.bl_idname, text="DAVA scene (.sc2/.scg)")

'''
Register
'''
classes = {
    ExportDAVA,
    ImportDAVA
}

def register():
    # Register classes
    for c in classes:
        bpy.utils.register_class(c)
    # File > Import-Export
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_dava)
#    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_dava)

def unregister():
    # Unregister classes
    for c in classes:
        bpy.utils.unregister_class(c)
    # Remove `File > Import-Export`
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_dava)
#    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_dava)
