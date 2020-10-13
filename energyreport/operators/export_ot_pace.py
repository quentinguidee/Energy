import bpy

from ...functions import create_pace_file


class EXPORT_OT_PACE(bpy.types.Operator):
    bl_idname = "export.pace"  # this is important since its how bpy.ops.export.some_data is constructed
    bl_label = "Export to Pace"

    text: bpy.props.StringProperty(
        name='text',
        default=''
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        return create_pace_file()
