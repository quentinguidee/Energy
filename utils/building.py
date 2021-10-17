import math
import bmesh
import bpy

from typing import Dict, List, TypedDict
from xml.etree.ElementTree import SubElement

from .calculation import eval_projected_area
from .color import Color
from .element_type import ElementType
from .element_type_factory import ElementTypeFactory
from .face import Face
from .face_type import FaceType
from .orientation import Orientation


class Building:
    def populate_faces(self, obj):
        for a in obj.data.polygons:
            angle_proj = round(math.degrees(math.atan2(a.normal[0], a.normal[1])))
            angle_proj_orientation = Orientation.get_direction(angle_proj)
            material_id = obj.material_slots[a.material_index].name[0:1]

            if round(math.atan2(a.normal[1], a.normal[2]), 3) == 0:
                angle_roof = math.atan2(a.normal[0], a.normal[2])
            else:
                hypotenuse = math.sqrt(math.pow(a.normal[0], 2) + math.pow(a.normal[1], 2))
                angle_roof = math.atan2(hypotenuse, a.normal[2])

            face = Face(
                index=a.index,
                area=a.area,
                orientation=angle_proj_orientation,
                material=bpy.context.object.material_slots[a.material_index].name[0:4],
                type=FaceType.get_face_type(material_id),
                angle=angle_roof,
                projection_area=eval_projected_area(a, obj),
                material_name=bpy.context.object.material_slots[a.material_index].name[5:],
            )

            self.faces.append(face)

    def __init__(self, obj):
        self.obj = obj
        self.faces: List[Face] = []
        self.populate_faces(obj)
        self.element_types: List[ElementType] = []
        self.populate_element_types()

    def populate_element_types(self):
        for material in bpy.context.object.material_slots:
            face_type = FaceType.get_face_type(material.name[0])
            element_type = ElementTypeFactory.serialize(face_type, material.name[0:4], material.name[5:])
            self.element_types.append(element_type)

    def get_faces(self, face_type: FaceType) -> List[Face]:
        return [face for face in self.faces if face.type == face_type]

    def eval_volume(self):
        """
        Calculate the volume of the mesh object.
        """
        if self.obj and self.obj.type == 'MESH' and self.obj.data:
            # New volume method for bmesh 2015 corrected 2017
            bm = bmesh.new()
            # could also use from_mesh() if you don't care about deformation etc.
            bm.from_object(self.obj, bpy.context.evaluated_depsgraph_get())
            bmesh.ops.triangulate(bm, faces=bm.faces)
            return math.fabs(bm.calc_volume())

    def eval_area(self):
        """
        Calculate the area of the mesh object.
        """
        return sum([face.area for face in self.faces])


class Material(TypedDict):
    name: str
    area: float


class WallsGroup(TypedDict):
    orientation: Orientation
    faces: List[Face]
    projected_area: float
    materials: List[Material]


def get_walls_grouped_by_orientation(walls: List[Face]) -> List[WallsGroup]:
    """
    :param walls: Walls to group
    :return: A dictionary formatted like this:
    {
        "faces": [face1, face2...],
        "projected_area": 12.3,
        "materials": {
            "M-01": { area: 2 },
            ...
        }
    }
    """
    walls_grouped: List[WallsGroup] = []

    for orientation in Orientation:
        faces: List[Face] = []
        material_names: List[str] = []
        materials: List[Material] = []
        projected_area = 0

        for wall in walls:
            if wall.orientation == orientation:
                faces.append(wall)
                projected_area += wall.area

        if projected_area != 0:
            for face in faces:
                if material_names.count(str(face.material)) == 0:
                    material_names.append(face.material)

            for material in sorted(material_names):
                area = 0
                for face in faces:
                    if face.material == material:
                        area += face.area

                materials.append({
                    'name': material,
                    'area': area
                })

        if materials:
            walls_grouped.append({
                'orientation': orientation,
                'faces': faces,
                'projected_area': projected_area,
                'materials': materials
            })

    return walls_grouped


def add_walls_to_html(html_projections, walls):
    face_type_id = FaceType.WALL.get_id()
    walls_grouped_by_orientation = get_walls_grouped_by_orientation(walls)

    projection_id = 0
    for walls_group in walls_grouped_by_orientation:
        projection_id += 1

        orientation = walls_group['orientation']
        projected_area = walls_group['projected_area']
        materials = walls_group['materials']

        projection_html_1 = SubElement(html_projections[face_type_id][0][1 if projection_id <= 4 else 2], 'td')
        projection_html_1_table = SubElement(projection_html_1, 'table')
        projection_html_1_table.attrib["id"] = "walls_projection"
        tbody = SubElement(projection_html_1_table, 'tbody')
        caption = SubElement(tbody, 'caption')
        caption.text = "Az.: " + str(orientation.name) + " - " + str(round(projected_area, 2)) + " m²"

        for material in materials:
            name = material['name']
            area = material['area']

            tr = SubElement(tbody, 'tr')
            td_1 = SubElement(tr, 'td')
            td_1.attrib["class"] = "mat_color"

            color = Color()
            for material_slot in bpy.context.object.material_slots:
                if material_slot.name[0:4] == name:
                    color = Color.from_8_bits_color(material_slot.material.diffuse_color)

            td_1.attrib["style"] = "color:" + str(color)
            td_1.text = "\u25A0"
            td_2 = SubElement(tr, 'td')
            td_2.attrib["class"] = "mat_index"
            td_2.text = str(name)
            td_3 = SubElement(tr, 'td')
            td_3.attrib["class"] = "mat_surf"
            td_3.text = str(round(area, 2)) + " m²"
