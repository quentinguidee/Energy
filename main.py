# ArToKi-Energy.py (c) 2015 Thierry Maes (tmaes)

import importlib

from bpy.utils import register_class, unregister_class

from .classes import energy_report, energy_deperditions, export_ot_xml, export_ot_html

from .classes.energy_report import OBJECT_PT_ArToKi_EnergyReport
from .classes.energy_deperditions import OBJECT_PT_ArToKi_EnergyDeperditions
from .classes.export_ot_html import EXPORT_OT_HTML
from .classes.export_ot_xml import EXPORT_OT_XML


def register():
    register_class(OBJECT_PT_ArToKi_EnergyReport)
    register_class(OBJECT_PT_ArToKi_EnergyDeperditions)
    register_class(EXPORT_OT_XML)
    register_class(EXPORT_OT_HTML)


def unregister():
    unregister_class(OBJECT_PT_ArToKi_EnergyReport)
    unregister_class(OBJECT_PT_ArToKi_EnergyDeperditions)
    unregister_class(EXPORT_OT_XML)
    unregister_class(EXPORT_OT_HTML)


importlib.reload(energy_report)
importlib.reload(energy_deperditions)
importlib.reload(export_ot_xml)
importlib.reload(export_ot_html)
