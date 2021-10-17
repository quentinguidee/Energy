from bpy.types import Operator
from bpy.props import *
from bpy_extras.io_utils import ExportHelper

from ..utils.exports import create_html_file


class EXPORT_OT_HTML(Operator, ExportHelper):
    bl_idname = "export.html"
    bl_label = "Export to .html"

    filename_ext = ".html"

    filter_glob: StringProperty(
        default="*.html",
        options={'HIDDEN'},
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        return create_html_file(self.filepath)
