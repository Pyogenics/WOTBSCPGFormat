'''
Copyright (C) 2023 Pyogenics <https://www.github.com/Pyogenics>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import bpy

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

'''
IO drivers
'''
class ImportSC2(bpy.types.Operator):
    bl_idname = "import_scene.sc2"
    bl_label = "Import DAVA scene file v2"
    bl_description = "Import a DAVA scene file"

    def execute(self, context):
        return {'FINISHED'}

class ExportSC2(bpy.types.Operator):
    bl_idname = "export_scene.sc2"
    bl_label = "Export DAVA scene file v2"
    bl_description = "Export a DAVA scene file"

    def execute(self, context):
        return {'FINISHED'}

'''
UI
'''

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
    print("Goodbye, cruel world!")

if __name__ == "__main__":
    register()
