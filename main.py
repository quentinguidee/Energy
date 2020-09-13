# ArToKi-Energy.py (c) 2015 Thierry Maes (tmaes)

import importlib

from bpy.utils import register_class, unregister_class

from .classes import energy_report, energy_deperditions, export_ot_xml, export_ot_html

from .classes.energy_report import EnergyReport
from .classes.energy_deperditions import EnergyDeperditions
from .classes.export_ot_html import ExportOTHTML
from .classes.export_ot_xml import ExportOTXML


def register():
    register_class(EnergyReport)
    register_class(EnergyDeperditions)
    register_class(ExportOTXML)
    register_class(ExportOTHTML)


def unregister():
    unregister_class(EnergyReport)
    unregister_class(EnergyDeperditions)
    unregister_class(ExportOTXML)
    unregister_class(ExportOTHTML)


importlib.reload(energy_report)
importlib.reload(energy_deperditions)
importlib.reload(export_ot_xml)
importlib.reload(export_ot_html)
