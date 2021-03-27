# ArToKi-Energy.py (c) 2015 Thierry Maes (tmaes)

from bpy.utils import register_class, unregister_class

from .energyreport.energy_report import ARTOKI_PT_EnergyReport
from .energyreport.operators.export_ot_html import EXPORT_OT_HTML
from .energyreport.operators.export_ot_xml import EXPORT_OT_XML
from .energyreport.operators.export_ot_pace import EXPORT_OT_PACE

from .energydeperditions.energy_deperditions import ARTOKI_PT_EnergyDeperditions

from .mana.mana import ARTOKI_PT_create_material, ARTOKI_OT_add_basic

classes = (
    ARTOKI_PT_EnergyReport,
    ARTOKI_PT_EnergyDeperditions,
    EXPORT_OT_XML,
    EXPORT_OT_HTML,
    EXPORT_OT_PACE,
    ARTOKI_PT_create_material,
    ARTOKI_OT_add_basic
)


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in classes:
        unregister_class(cls)
