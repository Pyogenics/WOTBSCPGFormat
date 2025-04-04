import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper

from .SCG import SCG
from .BlenderDataImporter import BlenderDataImporter

'''
Operators
'''
class ImportDava(Operator, ImportHelper):
    bl_idname = "import_scene.dava"
    bl_label = "Import DAVA data"
    bl_description = "Import a DAVA scene or geometry file"
    bl_options = {'PRESET', 'UNDO'}

    filter_glob: StringProperty(default="*.scg;*.sc2;*.scg.dvpl;*.sc2.dvpl", options={'HIDDEN'})

    def draw(self, context):
        pass

    def invoke(self, context, event):
        return ImportHelper.invoke(self, context, event)

    def execute(self, context):
        print(f"Reading DAVA data from {self.filepath}")

        # Read data
        geometryData = SCG()
        with open(self.filepath, "rb") as file:
            geometryData.read(file)

        # Import data
        importer = BlenderDataImporter(geometryData)
        objects = importer.importData()
        for ob in objects:
            bpy.context.collection.objects.link(ob)

        return {'FINISHED'}

'''
UI
'''
def menu_func_import_dava_scene(self, context):
    self.layout.operator(ImportDava.bl_idname, text="Dava framework (.scg/.sc2)")

'''
Registration
'''
classes = [
    ImportDava
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import_dava_scene)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import_dava_scene)

if __name__ == "__main__":
    register()