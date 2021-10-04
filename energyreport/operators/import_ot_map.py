import bpy
from bpy.props import *


class IMPORT_OT_MAP(bpy.types.Operator):
    bl_idname = "import.map"
    bl_label = "Import scaled aerial map as plane"
    

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        return bpy.ops.import_image.to_plane(files=[{'name':bpy.data.scenes["Scene"].atk_aerial}],align_axis='Z+',height=41.095)

