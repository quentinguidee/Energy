# ArToKi-Energy.py (c) 2015 Thierry Maes (tmaes)

from bpy.utils import register_class, unregister_class

from .panels.energy_report import ARTOKI_PT_EnergyReport
from .panels.energy_deperditions import ARTOKI_PT_EnergyDeperditions
from .panels.mana import ARTOKI_PT_create_material, ARTOKI_OT_add_basic

from .operators.export_ot_html import EXPORT_OT_HTML
from .operators.export_ot_xml import EXPORT_OT_XML
from .operators.export_ot_pace import EXPORT_OT_PACE
from .operators.import_ot_map import IMPORT_OT_MAP
from .operators.object_ot_open_preferences import OBJECT_OT_OpenPreferences

from .preferences import Preferences

classes = (
    ARTOKI_PT_EnergyReport,
    ARTOKI_PT_EnergyDeperditions,
    EXPORT_OT_XML,
    EXPORT_OT_HTML,
    EXPORT_OT_PACE,
    IMPORT_OT_MAP,
    ARTOKI_PT_create_material,
    ARTOKI_OT_add_basic,
    OBJECT_OT_OpenPreferences,
    Preferences
)


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in classes:
        unregister_class(cls)
