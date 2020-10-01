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
        self.populate_template(
            template_filename='templates/wallplane.xml',
            find='./building/skin/wallPlanes/INITIAL',
            replace_queries={
                'shortDescription': {
                    'value': wall.name
                },
                'orientation/INITIAL': {
                    'class': 'com.hemmis.mrw.pace.model.enums.Orientation',
                    'value': wall.orientation.name
                },
                'width/INITIAL': {
                    'class': 'java.math.BigDecimal',
                    'value': wall.width
                },
                'height/INITIAL': {
                    'class': 'java.math.BigDecimal',
                    'value': wall.height
                }
            })

    def register_new_roof(self, roof: Roof):
        self.populate_template(
            template_filename='templates/roofplane.xml',
            find='./building/skin/roofPlanes/INITIAL',
            replace_queries={
                'shortDescription': {
                    'value': roof.name
                },
                'orientation/INITIAL': {
                    'class': 'com.hemmis.mrw.pace.model.enums.Orientation',
                    'value': roof.orientation.name
                },
                'slope/INITIAL': {
                    'class': 'java.math.BigDecimal',
                    'value': roof.angle
                },
                'width/INITIAL': {
                    'class': 'java.math.BigDecimal',
                    'value': roof.width
                },
                'height/INITIAL': {
                    'class': 'java.math.BigDecimal',
                    'value': roof.height
                }
            }
        )
        # AUTO: ProjectionSurface
        # AUTO: Rest

    def populate_template(self, template_filename: str, find: str, replace_queries: dict):
        template_root = ET.parse(template_filename).getroot()
        root = self.root.find(find)

        for query_key, query_item in replace_queries.items():
            element = template_root.find(query_key)
            for key, value in query_item.items():
                if key == 'value':
                    element.text = str(value)
                else:
                    element.set(key, value)

        # Fix ids
        lines = ET.tostringlist(template_root, encoding='unicode', method='xml')
        self.fix_ids(lines)
        root.append(ET.fromstringlist(lines))

        if DEBUG:
            print(lines)
