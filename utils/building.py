import math
import bmesh
import bpy

from typing import List, Tuple, TypedDict
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
    :return: A list formatted like this:
    [
        "orientation": Orientation.N
        "faces": [face1, face2...],
        "projected_area": 12.3,
        "materials": [
            { "name": "M-01", "area": 2 },
            ...
        ]
    ]
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


def get_all_floors_materials(floors: List[Face]) -> Tuple[float, List[Material]]:
    """
    :param floors:
    :return: Tuple with area + list of materials.
    """
    total_area = sum([floor.projection_area for floor in floors])
    if total_area == 0:
        return total_area, []

    material_names: List[str] = []
    materials: List[Material] = []

    for floor in floors:
        if material_names.count(str(floor.material)) == 0:
            material_names.append(floor.material)

    for material in sorted(material_names):
        area = 0
        for floor in floors:
            if floor.material == material:
                area += floor.projection_area

        if area != 0:
            materials.append({
                'name': material,
                'area': area
            })

    return total_area, materials


class RoofMaterial(TypedDict):
    name: str
    area: float
    orientation: Orientation
    angle: float
    projected_area: float


def get_all_roofs(roofs: List[Face]) -> Tuple[float, List[RoofMaterial]]:
    """
    :param roofs:
    :return: Tuple with projected area + list of materials.
    """
    total_area = 0
    total_projected_area = 0

    material_names = []
    materials: List[RoofMaterial] = []

    for roof in roofs:
        total_area += roof.area
        total_projected_area += roof.projection_area

    if total_area == 0:
        return total_projected_area, []

    for roof in roofs:
        if material_names.count(str(roof.material)) == 0:
            material_names.append(roof.material)

    for material in sorted(material_names):
        area: float = 0
        projected_area: float = 0
        angle: float = 0
        orientation: Orientation = None

        for roof in roofs:
            if roof.material == material:
                area += roof.area
                projected_area += roof.projection_area
                angle = roof.angle
                orientation = roof.orientation

        if orientation is not None:
            materials.append({
                'name': material,
                'area': area,
                'orientation': orientation,
                'angle': angle,
                'projected_area': projected_area
            })

    return total_projected_area, materials


def add_walls_to_html(walls, html_projections):
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


def add_floors_to_html(floors, html_projections, html_tree):
    face_type_id = FaceType.FLOOR.get_id()
    total_area, materials = get_all_floors_materials(floors)
    if total_area == 0:
        return

    total_area = str(round(total_area, 2))

    html_projections[face_type_id].attrib['Surf'] = total_area

    caption = html_tree.find(".//table[@id='floors_values']/tbody/caption")
    caption.text = 'Projection Sols: ' + total_area + ' m²'

    for material in materials:
        name = material['name']
        area = material['area']
        area = str(round(area, 2))

        tr = SubElement(html_projections[face_type_id][0], 'tr')
        td_1 = SubElement(tr, 'td')
        td_1.attrib["class"] = "mat_color"

        color = Color()
        for material_slot in bpy.context.object.material_slots:
            if material_slot.name[0:4] == material:
                color = Color.from_8_bits_color(material_slot.material.diffuse_color)

        td_1.attrib["style"] = "color:" + str(color)
        td_1.text = "\u25A0"
        td_2 = SubElement(tr, 'td')
        td_2.attrib["class"] = "mat_index"
        td_2.text = name
        td_3 = SubElement(tr, 'td')
        td_3.attrib["class"] = "mat_surf"
        td_3.text = area + " m²"


def add_roofs_to_html(roofs, html_projections, html_tree):
    face_type_id = FaceType.ROOF.get_id()
    total_projected_area, materials = get_all_roofs(roofs)
    if total_projected_area == 0:
        return

    total_projected_area = str(round(total_projected_area, 2))

    html_projections[face_type_id].attrib['Surf'] = total_projected_area

    caption = html_tree.find(".//table[@id='roofs_values']/tbody/caption")
    caption.text = 'Projection Toitures: ' + total_projected_area + ' m²'

    for material in materials:
        name = material['name']
        area = str(round(material['area'], 2))
        orientation = material['orientation']
        angle = material['angle']
        projected_area = str(round(material['projected_area'], 2))

        tr = SubElement(html_projections[face_type_id], 'tr')
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
        td_2.text = name
        td_3 = SubElement(tr, 'td')
        td_3.attrib["class"] = "mat_surf_brute"
        td_3.text = area + " m²"
        td_4 = SubElement(tr, 'td')
        td_4.attrib["class"] = "mat_angle"
        td_4.text = str(round(math.fabs(math.degrees(angle)), 1)) + " °"
        td_5 = SubElement(tr, 'td')
        td_5.attrib["class"] = "mat_orient"
        td_5.text = str(orientation.name)
        td_6 = SubElement(tr, 'td')
        td_6.attrib["class"] = "mat_surf_proj"
        td_6.text = projected_area + " m²"
