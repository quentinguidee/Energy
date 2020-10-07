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
        pace_object.id = self.current_id + 1
        self.populate_template(
            template_filename=pace_object.template_filename,
            find=pace_object.path,
            replace_queries=pace_object.replace_queries)

    def populate_template(self, template_filename: str, find: str, replace_queries: dict):
        template_root = ''
        root = ''

        if template_filename is not None:
            template_root = ET.parse(template_filename).getroot()
            root = self.root.find(find)

            for query_key, query_item in replace_queries.items():
                element = template_root.find(query_key)
                if query_key != 'MORE':
                    for key, value in query_item.items():
                        if key == 'value':
                            element.text = str(value)
                        else:
                            element.set(key, str(value))

        if 'MORE' in replace_queries.keys():
            more_queries = replace_queries['MORE']

            for path, queries in more_queries.items():
                more_root = self.root.find(path)

                for key, value in queries.items():
                    # element = more_root.find(key)
                    # if element is None:
                    print(str(path) + ": " + str(key) + " " + str(value))
                    element = ET.SubElement(more_root, key)

                    for k, v in value.items():
                        if k == 'value':
                            element.text = str(v)
                        else:
                            if v == 'CURRENT_ID':
                                element.set(k, str(self.current_id + 1))
                            elif 'CURRENT_ID' in str(v):
                                i = self.current_id + int(v[v.index('+') + 1:]) + 1
                                element.set(k, str(i))
                            else:
                                element.set(k, str(v))

        if template_filename is not None:
            # Fix ids
            lines = ET.tostringlist(template_root, encoding='unicode', method='xml')
            self.fix_ids(lines)
            root.append(ET.fromstringlist(lines))

            if DEBUG:
                print(lines)
