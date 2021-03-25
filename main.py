# ArToKi-Energy.py (c) 2015 Thierry Maes (tmaes)

from bpy.utils import register_class, unregister_class

from .energyreport.energy_report import OBJECT_PT_ArToKi_EnergyReport
from .energyreport.operators.export_ot_html import EXPORT_OT_HTML
from .energyreport.operators.export_ot_xml import EXPORT_OT_XML
from .energyreport.operators.export_ot_pace import EXPORT_OT_PACE

from .energydeperditions.energy_deperditions import OBJECT_PT_ArToKi_EnergyDeperditions

classes = (
    OBJECT_PT_ArToKi_EnergyReport,
    OBJECT_PT_ArToKi_EnergyDeperditions,
    EXPORT_OT_XML,
    EXPORT_OT_HTML,
    EXPORT_OT_PACE
)


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in classes:
        unregister_class(cls)
