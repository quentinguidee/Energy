# ArToKi-Energy.py (c) 2015 Thierry Maes (tmaes)

from bpy.utils import register_class, unregister_class

from .classes.energy_report import OBJECT_PT_ArToKi_EnergyReport
from .classes.energy_deperditions import OBJECT_PT_ArToKi_EnergyDeperditions
from .classes.export_ot_html import EXPORT_OT_HTML
from .classes.export_ot_xml import EXPORT_OT_XML

classes = (
    OBJECT_PT_ArToKi_EnergyReport,
    OBJECT_PT_ArToKi_EnergyDeperditions,
    EXPORT_OT_XML,
    EXPORT_OT_HTML,
)


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in classes:
        unregister_class(cls)

# import importlib
# from .classes import energy_report, energy_deperditions, export_ot_xml, export_ot_html

# importlib.reload(energy_report)
# importlib.reload(energy_deperditions)
# importlib.reload(export_ot_xml)
# importlib.reload(export_ot_html)
