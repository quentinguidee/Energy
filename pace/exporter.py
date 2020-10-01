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


class Wall:
    def __init__(self, name: str, orientation: Orientation, width: float, height: float):
        self.name = name
        self.orientation = orientation
        self.width = width
        self.height = height


class PaceExporter:
    # TODO: Auto assignment
    LAST_ID = 15720

    def __init__(self):
        self.current_id = self.LAST_ID
        self.tree: ElementTree = ET.parse('templates/blank.xml')
        self.root: Element = self.tree.getroot()

    def export(self, filename: str):
        self.tree.write(filename)

    # OLD SYSTEM: Replacing ids in the entire document.
    # def fix_ids(self, filename):
    #     """
    #     Rewrite all ids. This considers that there is only one ID in each line.
    #     """
    #     with open(filename) as file:
    #         lines = file.read().splitlines()
    #
    #     with open(filename, 'w') as file:
    #         for line in lines:
    #             if 'id=\"' in line:
    #                 start = line.index('id="')
    #                 end = line.index('"', start + 4) + 1
    #                 old_id = line[start:end]
    #                 new_id = 'id="' + str(self.next_id()) + '"'
    #                 new_line = line.replace(old_id, new_id)
    #
    #                 # if DEBUG:
    #                 if False:
    #                     print(old_id + " with " + str(start) + " and " + str(end))
    #                     print(new_id)
    #                     print("New line: " + new_line)
    #
    #             else:
    #                 new_line = line
    #
    #             file.write(new_line + "\n")

    def fix_ids(self, lines):
        """
        Rewrite all ids. This considers that there is only one ID in each line.
        """
        for i in range(len(lines)):
            line = lines[i]
            if 'id=\"' in line:
                start = line.index('id="')
                end = line.index('"', start + 4) + 1
                old_id = line[start:end]
                old_id_int = old_id[4:-1]
                new_id_int = self.next_id()
                new_id = 'id="' + str(new_id_int) + '"'
                new_line = line.replace(old_id, new_id)

                if DEBUG:
                    print(old_id + " with " + str(start) + " and " + str(end))
                    print(new_id)
                    print("New line: " + new_line)

                lines[i] = new_line

                for j in range(len(lines)):
                    line = lines[j]
                    r = 'reference="' + str(old_id_int) + '"'
                    if r in line:
                        new_reference_line = line.replace(str(old_id_int), str(new_id_int))

                        if DEBUG:
                            print(new_reference_line)

                        lines[j] = new_reference_line

    def next_id(self) -> int:
        self.current_id += 1
        return self.current_id

    def register_new_wall(self, wall: Wall):
        wall_planes = self.root.find('./building/skin/wallPlanes')
        initial = wall_planes.find('INITIAL')

        # Load wallplane.xml
        wall_planes_template = ET.parse('templates/wallplane.xml')
        wall_planes_template_root = wall_planes_template.getroot()

        # Set info
        wall_planes_template_root.find('shortDescription').text = wall.name

        root_orientation = wall_planes_template_root.find('orientation/INITIAL')
        root_orientation.set('class', 'com.hemmis.mrw.pace.model.enums.Orientation')
        root_orientation.text = wall.orientation.name

        root_width = wall_planes_template_root.find('width/INITIAL')
        root_width.set('class', 'java.math.BigDecimal')
        root_width.text = str(wall.width)

        root_height = wall_planes_template_root.find('height/INITIAL')
        root_height.set('class', 'java.math.BigDecimal')
        root_height.text = str(wall.height)

        # Fix ids
        lines = ET.tostringlist(wall_planes_template_root, encoding='unicode', method='xml')
        self.fix_ids(lines)

        initial.append(ET.fromstringlist(lines))

        if DEBUG:
            print(lines)

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

        # Fix ids
        lines = ET.tostringlist(roof_planes_template_root, encoding='unicode', method='xml')
        self.fix_ids(lines)

        initial.append(ET.fromstringlist(lines))

        if DEBUG:
            print(ET.fromstringlist(lines).getchildren())
            print(lines)
