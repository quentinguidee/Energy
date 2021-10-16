from bpy.types import Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper

from ..functions import create_xml_file


class EXPORT_OT_XML(Operator, ExportHelper):
    bl_idname = "export.xml"
    bl_label = "Export to .xml"

    filename_ext = ".xml"

    filter_glob: StringProperty(
        default="*.xml",
        options={'HIDDEN'},
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        return create_xml_file(self.filepath)
