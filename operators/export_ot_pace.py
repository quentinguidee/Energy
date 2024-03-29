from bpy.types import Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper

from ..utils.exports import create_pace_file


class EXPORT_OT_PACE(Operator, ExportHelper):
    bl_idname = "export.pace"
    bl_label = "Export to Pace"

    filename_ext = ".pce"

    filter_glob: StringProperty(
        default="*.pce",
        options={'HIDDEN'},
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        return create_pace_file(self.filepath)
