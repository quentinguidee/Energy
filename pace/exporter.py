import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree

from energyreport.classes.orientation import Orientation
from info import DEBUG


class Roof:
    def __init__(self, name: str, orientation: Orientation, angle: float, width: float, height: float):
        self.name = name
        self.orientation = orientation
        self.angle = angle
        self.width = width
        self.height = height


class PaceExporter:
    def __init__(self):
        self.tree: ElementTree = ET.parse('templates/blank.xml')
        self.root: Element = self.tree.getroot()

    def export(self, filename: str):
        self.tree.write(filename)
        self.fix_ids()

    def fix_ids(self):
        # Rewrite all ids
        pass

    def register_new_roof(self, roof: Roof):
        roof_planes = self.root.find("./building/skin/roofPlanes")
        initial = roof_planes.find('INITIAL')

        # Load roofplane.xml
        roof_planes_template = ET.parse('templates/roofplane.xml')
        roof_planes_template_root = roof_planes_template.getroot()

        # Set info
        roof_planes_template_root.find('shortDescription').text = roof.name

        root_orientation = roof_planes_template_root.find('orientation/INITIAL')
        root_orientation.set('class', 'com.hemmis.mrw.pace.model.enums.Orientation')
        root_orientation.text = roof.orientation.name

        root_angle = roof_planes_template_root.find('slope/INITIAL')
        root_angle.set('class', 'java.math.BigDecimal')
        root_angle.text = str(roof.angle)  # !! format: 32.00

        root_width = roof_planes_template_root.find('width/INITIAL')
        root_width.set('class', 'java.math.BigDecimal')
        root_width.text = str(roof.width)

        root_height = roof_planes_template_root.find('height/INITIAL')
        root_height.set('class', 'java.math.BigDecimal')
        root_height.text = str(roof.height)

        # AUTO: ProjectionSurface
        # AUTO: Rest

        initial.append(roof_planes_template_root)

        if DEBUG:
            ElementTree(roof_planes).write('debug/roofs.xml')
