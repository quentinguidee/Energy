import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree

from info import DEBUG
from .paceobjects.pace_object import PaceObject


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

    def register(self, pace_object: PaceObject):
        self.populate_template(
            template_filename=pace_object.template_filename,
            find=pace_object.path,
            replace_queries=pace_object.replace_queries)

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
