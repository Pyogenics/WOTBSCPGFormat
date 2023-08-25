'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from .SCGImporter import SCGImporter

import bpy
from bpy.types import Operator
from bpy.props import (StringProperty, CollectionProperty)
from bpy_extras.io_utils import ImportHelper, ExportHelper

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

'''
Operators
'''
class ImportSCG(Operator, ImportHelper):
    bl_idname = "import_scene.scg"
    bl_label = "Import DAVA scene"
    bl_description = "Import a DAVA scene file"

    filter_glob: StringProperty(default="*.scg", options={'HIDDEN'})
    files: CollectionProperty(name="File Path", type=bpy.types.OperatorFileListElement)

    def buildCollection(self, importer):
        objCollection = bpy.data.collections.new("model")
        elementArrays = importer.polygonGroups
        for elements in elementArrays:
            mesh = bpy.data.meshes.new("PolygonGroup")
            mesh.from_pydata(elements["vertices"], elements["edges"], elements["faces"])
            mesh.update()
            
            obj = bpy.data.objects.new("object", mesh)
            objCollection.objects.link(obj)
        bpy.context.scene.collection.children.link(objCollection)

        return len(importer.polygonGroups)

    def invoke(self, context, event):
        return ImportHelper.invoke(self, context, event)

    def execute(self, context):
        # import
        with open(self.filepath, "rb") as f:
            importer = SCGImporter()
            importer.importFromFileStream(f)

            meshesLoaded = self.buildCollection(importer)

            self.report({"INFO"}, f"Loaded {meshesLoaded} polygon groups")

        return {"FINISHED"}

class ExportSCG(Operator, ExportHelper):
    bl_idname = "export_scene.scg"
    bl_label = "Export DAVA scene"
    bl_description = "Export a DAVA scene file"

    def execute(self, context):
        return {'FINISHED'}

'''
Menu
'''
def menu_func_import_scg(self, context):
    self.layout.operator(ImportSCG.bl_idname, text="DAVA scene file (.scg)")

def menu_func_export_scg(self, context):
    self.layout.operator(ExportSCG.bl_idname, text="DAVA scene file (.scg)")

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
