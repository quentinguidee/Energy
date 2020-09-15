import datetime
import math
import os
from collections import namedtuple
from enum import Enum
from typing import overload
from xml.etree.ElementTree import SubElement, ElementTree

from bpy.props import StringProperty, EnumProperty, BoolProperty
from ..functions import face_projection_area, object_volume
from .. import info

import bpy


class Orientation(Enum):
    S = (-191.25, -168.75)
    SSW = (-168.75, -146.25)
    SW = (-146.25, -123.75)
    WSW = (-123.75, -101.25)
    W = (-101.25, -78.75)
    WNW = (-78.75, -56.25)
    NW = (-56.25, -33.75)
    NNW = (-33.75, -11.25)
    N = (-11.25, 11.25)
    NNE = (-11.25, 33.75)
    NE = (33.75, 56.25)
    ENE = (56.25, 78.75)
    E = (78.75, 101.25)
    ESE = (101.25, 123.75)
    SE = (123.75, 146.25)
    SSE = (146.25, 168.75)

    @staticmethod
    def get_direction(angle_proj: float) -> 'Orientation':
        if 168.75 <= angle_proj < 191.25:
            return Orientation.S

        for direction in Orientation:
            if direction.value[0] <= angle_proj < direction.value[1]:
                return direction


class FaceType(Enum):
    WALL = (0, 'Walls', 'MOD_BUILD', ['M', 'W'])
    FLOOR = (1, 'Floors', 'TEXTURE', ['S', 'F'])
    ROOF = (2, 'Roofs', 'LINCURVE', ['T', 'R'])

    def get_id(self):
        return self.value[0]

    def get_name(self):
        return self.value[1]

    def get_icon(self):
        return self.value[2]

    def get_letters(self):
        return self.value[3]

    @staticmethod
    def get_face_type(letter: str) -> 'FaceType':
        for face_type in FaceType:
            if letter in face_type.get_letters():
                return face_type


class Face:
    index: int
    area: float
    orientation: Orientation
    material: str  # ?
    type: FaceType
    angle: float
    projection_area: float
    material_name: str

    def __init__(self, index: int, area: float, orientation: Orientation, material: str, face_type: FaceType,
                 angle: float, projection_area: float, material_name: str):
        self.index = index
        self.area = area
        self.orientation = orientation
        self.material = material
        self.type = face_type
        self.angle = angle
        self.projection_area = projection_area
        self.material_name = material_name


class Color:
    def __init__(self, red: int = 0, green: int = 0, blue: int = 0):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        return "rgb(" + str(self.red) + "," + str(self.green) + "," + str(self.blue) + ")"

    @staticmethod
    def from_8_bits(red: float, green: float, blue: float) -> 'Color':
        return Color(int(red * 255), int(green * 255), int(blue * 255))

    @staticmethod
    def from_8_bits_color(color: list) -> 'Color':
        return Color.from_8_bits(color[0], color[1], color[2])


class OBJECT_PT_ArToKi_EnergyReport(bpy.types.Panel):
    bl_label = "ArToKi - Energy - Report"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    bpy.types.Scene.atk_aerial \
        = StringProperty(name="Aerial", description="Aerial view path", default="", subtype='FILE_PATH')
    bpy.types.Scene.atk_elevation \
        = StringProperty(name="Elevation", description="Elevation view path", default="", subtype='FILE_PATH')
    bpy.types.Scene.atk_address1 \
        = StringProperty(name="Address 1", description="Street, nb", default="")
    bpy.types.Scene.atk_address2 \
        = StringProperty(name="Address 2", description="PostCode City", default="")
    bpy.types.Scene.atk_therm_col \
        = BoolProperty(name="Therm col", description="Assign materials colors by performance", default=0)
    bpy.types.Scene.atk_procedure_type \
        = EnumProperty(items=[('PAE', 'PAE', 'Procédure d\'audit énergétique'),
                              ('PEB', 'PEB', 'Performances énergétiques des batiments')],
                       name="Procedure type",
                       description="Changes the upper left text logo",
                       default="PEB"
                       )

    def draw(self, context):
        document_properties = {
            "author": 'Maes Thierry',
            "title": 'Auditeur PAE, Certificateur PEB',
            "address1": 'Rue Joseph Berger, 6',
            "address2": 'B-1470 Genappe',
            "email": 'info@tmaes.be',
            "phone": '+32 (0)67/ 63 68 50',
            "gsm": '+32 (0)475/ 30 36 51',
        }

        # préparation du fichier xml et html temporaires
        obj = context.object
        scene = bpy.context.scene
        date = datetime.datetime.now()

        base_file = os.path.expanduser('~') + '/.blender/ArToKi/artoki_peb_BASE.xml'
        temp_file = os.path.expanduser('~') + '/.blender/ArToKi/artoki_peb_temp.xml'

        tree = ElementTree(file=base_file)

        base_file_html = os.path.expanduser('~') + '/.blender/ArToKi/artoki_peb_html_BASE.html'
        temp_file_html = os.path.expanduser('~') + '/.blender/ArToKi/artoki_peb_html_temp.html'

        tree_html = ElementTree(file=base_file_html)

        # Bases du fichier xml et html
        root = tree.getroot()
        root_html = tree_html.getroot()
        root.attrib['Version'] = info.VERSION

        project = tree.find('Project')
        project.attrib['Name'] = bpy.context.scene.name
        project.attrib['Date'] = date.strftime("%Y-%m-%d %H:%M")

        address1 = tree.find('Project/Address1')
        address1.text = str(scene.atk_address1)
        address2 = tree.find('Project/Address2')
        address2.text = str(scene.atk_address2)

        # Place static elements of the HTML (coordinates, date...)
        for material_slot in tree_html.findall(".//td[@class='header_left']"):
            material_slot.text = str(scene.atk_procedure_type)
        for material_slot in tree_html.findall(".//td[@class='header_street']"):
            material_slot.text = str(scene.atk_address1)
        for material_slot in tree_html.findall(".//td[@class='header_city']"):
            material_slot.text = str(scene.atk_address2)
        for material_slot in tree_html.findall(".//td[@class='aud1']"):
            material_slot.text = str(document_properties["author"])
        for material_slot in tree_html.findall(".//td[@class='aud2']"):
            material_slot.text = str(document_properties["title"])
        for material_slot in tree_html.findall(".//td[@class='aud3']"):
            material_slot.text = str(document_properties["address1"])
        for material_slot in tree_html.findall(".//td[@class='aud4']"):
            material_slot.text = str(document_properties["address2"])
        for material_slot in tree_html.findall(".//td[@class='aud5']"):
            material_slot.text = str(document_properties["email"])
        for material_slot in tree_html.findall(".//td[@class='aud7']"):
            material_slot.text = str(document_properties["phone"])
        for material_slot in tree_html.findall(".//td[@class='aud8']"):
            material_slot.text = str(document_properties["gsm"])
        for material_slot in tree_html.findall(".//td[@class='date']"):
            material_slot.text = date.strftime("%d/%m/%Y")

        faces: [Face] = []

        for a in obj.data.polygons:
            angle_proj = round(math.degrees(math.atan2(a.normal[0], a.normal[1])))
            angle_proj_orientation = Orientation.get_direction(angle_proj)
            material_id = context.object.material_slots[a.material_index].name[0:1]

            if round(math.atan2(a.normal[1], a.normal[2]), 3) == 0:
                angle_roof = math.atan2(a.normal[0], a.normal[2])
            else:
                hypoth = math.sqrt(math.pow(a.normal[0], 2) + math.pow(a.normal[1], 2))
                angle_roof = math.atan2(hypoth, a.normal[2])

            face = Face(
                index=a.index,
                area=a.area,
                orientation=angle_proj_orientation,
                material=bpy.context.object.material_slots[a.material_index].name[0:4],
                face_type=FaceType.get_face_type(material_id),
                angle=angle_roof,
                projection_area=face_projection_area(a, obj),
                material_name=bpy.context.object.material_slots[a.material_index].name[5:],
            )

            faces.append(face)

        ### 1.1 LISTE DES MURS SOLS TOITS POUR L'EXPORT XML

        xml_materials = [
            tree.find('Project/Walls'),
            tree.find('Project/Floors'),
            tree.find('Project/Roofs'),
        ]

        html_materials = [
            tree_html.find(".//table[@id='Table_Walls']"),
            tree_html.find(".//table[@id='Table_Floors']"),
            tree_html.find(".//table[@id='Table_Roofs']"),
        ]

        for material_slot in bpy.context.object.material_slots:
            xml_surf_mat = 0

            for face in faces:
                if material_slot.name[0:4] == face.material:
                    xml_surf_mat += face.area

            face_type = FaceType.get_face_type(material_slot.name[0])
            color = Color.from_8_bits_color(material_slot.material.diffuse_color)

            tr = SubElement(html_materials[face_type.get_id()][1], 'tr', id=material_slot.name[0:4])
            td_1 = SubElement(tr, 'td')
            td_1.attrib["class"] = "mat_color"
            td_1.attrib["style"] = "color:" + str(color)
            td_1.text = "\u25A0"
            td_2 = SubElement(tr, 'td')
            td_2.attrib["class"] = "mat_index"
            td_2.text = material_slot.name[0:4]
            td_3 = SubElement(tr, 'td')
            td_3.attrib["class"] = "mat_name"
            td_3.text = material_slot.name[5:]
            td_4 = SubElement(tr, 'td')
            td_4.attrib["class"] = "mat_surf"
            td_4.text = str(round(xml_surf_mat, 2)) + " m²"

        ### 2 LISTE DES PROJECTIONS ET DES SURFACES

        properties = [
            ('atk_procedure_type', "Procedure"),
            ('atk_aerial', "Aerial view path"),
            ('atk_elevation', "Elevation view path"),
            ('atk_address1', "Street, Nb"),
            ('atk_address2', "PostCode City"),
            ('atk_therm_col', "Use thermic colors")
        ]

        layout = self.layout

        for prop in properties:
            row = layout.row()
            row.prop(scene, prop[0], text=prop[1])

        # row = layout.row()
        volume = math.fabs(object_volume(obj))

        total_area = 0
        for face in faces:
            total_area += face.area

        row = layout.row()
        row.alignment = 'EXPAND'

        box = row.box()

        column = box.column()

        sub_row = column.row(align=True)
        sub_row.label(text="Volume of the enveloppe:   " + str(round(volume, 2)) + " m\xb3", icon='VIEW3D')
        sub_row.label(text="Surface of the enveloppe:   " + str(round(total_area, 2)) + " m\xb2", icon='MESH_GRID')

        xml_volume = tree.find('Project/Volume')
        html_volume = tree_html.find(".//td[@id='general_volume']")

        xml_volume.text = str(round(volume, 2))
        html_volume.text = "Volume total: " + str(round(volume, 2)) + " m³"

        xml_surf_tot = tree.find('Project/Surf_tot')
        html_surf_tot = tree_html.find(".//td[@id='general_surface']")

        xml_surf_tot.text = str(round(total_area, 2))
        html_surf_tot.text = "Surface totale: " + str(round(total_area, 2)) + " m²"

        xml_projections = [
            tree.find('Project/WallProjections'),
            tree.find('Project/FloorProjections'),
            tree.find('Project/RoofProjections'),
        ]

        html_projections = [
            tree_html.find(".//table[@id='walls_values']"),
            tree_html.find(".//table[@id='floors_projection']"),
            tree_html.find(".//table[@id='roofs_projection']"),
        ]

        ### 2.1 MURS
        projection_id = 0
        face_type_id = FaceType.WALL.get_id()

        for orientation in Orientation:
            faces_proj: [Face] = []
            mat_proj = []
            surf_proj = 0

            # déterminer les faces de la projection et la surface de la projection
            for face in faces:
                if face.orientation == orientation and face.type == FaceType.WALL:
                    faces_proj.append(face)
                    surf_proj += face.area

            if surf_proj != 0:
                row = layout.row()
                row.alignment = 'EXPAND'

                box = row.box()

                column = box.column()

                sub_row = column.row(align=True)
                sub_row.label(
                    text=str(orientation.name) + " Projection          Surface  : " + str(
                        round(surf_proj, 2)) + " m\xb2",
                    icon='CURSOR')
                # on peut refaire le moteur apd ici...
                sub_row = column.row(align=True)
                sub_row.label(text="" + 75 * "-")
                projection = SubElement(xml_projections[face_type_id], 'WallProjection', Id=str(projection_id),
                                        Orientation=str(orientation.name), Surf=str(round(surf_proj, 2)))

                projection_id += 1

                for face_proj in faces_proj:
                    # si le matériau de la face n'existe pas encore dans mat_proj
                    if mat_proj.count(str(face_proj.material)) == 0:
                        # ajouter le matériau dans mat_proj [@name='a']
                        mat_proj.append(face_proj.material)

                for material_proj in sorted(mat_proj):
                    sub_row = column.row(align=True)
                    surf_mat = 0
                    for face_proj in faces_proj:
                        if face_proj.material == material_proj:
                            surf_mat += face_proj.area

                    sub_row.label(text=5 * ' ' + material_proj + ' : ' + str(round(surf_mat, 2)) + " m\xb2",
                                  icon='MOD_BUILD')
                    wallpart = SubElement(projection, 'WallPart', id=str(material_proj), Surf=str(round(surf_mat, 2)))

                projection_html_1 = SubElement(
                    html_projections[face_type_id][0][1 if projection_id <= 4 else 2], 'td')
                projection_html_1_table = SubElement(projection_html_1, 'table')
                projection_html_1_table.attrib["id"] = "walls_projection"
                tbody = SubElement(projection_html_1_table, 'tbody')
                caption = SubElement(tbody, 'caption')  # , Orientation=str(p), Surf=str(round(surf_proj,2))
                caption.text = "Az.: " + str(orientation.name) + " - " + str(round(surf_proj, 2)) + " m²"

                for face_proj in faces_proj:
                    # si le matériau de la face n'existe pas encore dans mat_proj
                    if mat_proj.count(str(face_proj.material)) == 0:
                        # ajouter le matériau dans mat_proj [@name='a']
                        mat_proj.append(face_proj.material)

                for material_proj in sorted(mat_proj):
                    surf_mat = 0
                    for face_proj in faces_proj:
                        if face_proj.material == material_proj:
                            surf_mat += face_proj.area

                    tr = SubElement(tbody, 'tr')
                    td_1 = SubElement(tr, 'td')
                    td_1.attrib["class"] = "mat_color"

                    color = Color()
                    for material_slot in bpy.context.object.material_slots:
                        if material_slot.name[0:4] == material_proj:
                            color = Color.from_8_bits_color(material_slot.material.diffuse_color)

                    td_1.attrib["style"] = "color:" + str(color)
                    td_1.text = "\u25A0"
                    td_2 = SubElement(tr, 'td')
                    td_2.attrib["class"] = "mat_index"
                    td_2.text = str(material_proj)
                    td_3 = SubElement(tr, 'td')
                    td_3.attrib["class"] = "mat_surf"
                    td_3.text = str(round(surf_mat, 2)) + " m²"

        ### 2.2 SOLS

        row = layout.row()
        row.alignment = 'EXPAND'

        box = row.box()

        column = box.column()

        area_vert = 0
        faces_vert = []
        mat_vert = []
        face_type_id = FaceType.FLOOR.get_id()

        for face in faces:
            if face.type == FaceType.FLOOR:
                faces_vert.append(face)
                area_vert += face.projection_area

        if area_vert != 0:
            sub_row = column.row(align=True)
            sub_row.label(text="Floors Projection     Surface : " + str(round(area_vert, 2)) + " m\xb2", icon="TEXTURE")
            sub_row = column.row(align=True)
            sub_row.label(text="" + 75 * "-")
            xml_projections[face_type_id].attrib['Surf'] = str(round(area_vert, 2))  #
            html_projections[face_type_id].attrib['Surf'] = str(round(area_vert, 2))  #
            caption = tree_html.find(".//table[@id='floors_values']/tbody/caption")
            caption.text = 'Projection Sols: ' + str(round(area_vert, 2)) + ' m²'

            for face_proj in faces_vert:
                if mat_vert.count(str(face_proj.material)) == 0:
                    mat_vert.append(face_proj.material)

            for material_proj in sorted(mat_vert):
                sub_row = column.row(align=True)
                surf_mat_vert = 0
                for face_proj in faces_vert:
                    if face_proj.material == material_proj:
                        surf_mat_vert += face_proj.projection_area

                sub_row.label(text=5 * ' ' + material_proj + ' : ' + str(round(surf_mat_vert, 2)) + " m\xb2",
                              icon="ASSET_MANAGER")

                tr = SubElement(html_projections[face_type_id][0], 'tr')
                td_1 = SubElement(tr, 'td')
                td_1.attrib["class"] = "mat_color"

                color = Color()
                for material_slot in bpy.context.object.material_slots:
                    if material_slot.name[0:4] == material_proj:
                        color = Color.from_8_bits_color(material_slot.material.diffuse_color)

                td_1.attrib["style"] = "color:" + str(color)
                td_1.text = "\u25A0"
                td_2 = SubElement(tr, 'td')
                td_2.attrib["class"] = "mat_index"
                td_2.text = str(material_proj)
                td_3 = SubElement(tr, 'td')
                td_3.attrib["class"] = "mat_surf"
                td_3.text = str(round(surf_mat_vert, 2)) + " m²"

        ### 2.3 TOITURE

        row = layout.row()
        row.alignment = 'EXPAND'
        box = row.box()
        column = box.column()
        surf_roof = 0
        surf_proj_roof = 0
        faces_roof = []
        mat_roof = []
        face_type_id = FaceType.ROOF.get_id()

        for face in faces:
            if face.type == FaceType.ROOF:
                faces_roof.append(face)
                surf_roof = surf_roof + face.area
                surf_proj_roof = surf_proj_roof + face.projection_area

        if surf_roof != 0:
            sub_row = column.row(align=True)
            sub_row.label(text="Roofs Projection     Surface : " + str(round(surf_proj_roof, 2)) + " m\xb2",
                          icon="LINCURVE")
            sub_row = column.row(align=True)
            sub_row.label(text="" + 75 * "-")
            xml_projections[face_type_id].attrib['Surf'] = str(round(surf_proj_roof, 2))  #
            html_projections[face_type_id].attrib['Surf'] = str(round(surf_proj_roof, 2))  #
            caption = tree_html.find(".//table[@id='roofs_values']/tbody/caption")
            caption.text = 'Projection Toitures: ' + str(round(surf_proj_roof, 2)) + ' m²'

            for face_proj in faces_roof:
                if mat_roof.count(str(face_proj.material)) == 0:
                    mat_roof.append(face_proj.material)
            for material_proj in sorted(mat_roof):
                sub_row = column.row(align=True)
                surf_mat_roof = 0
                surf_proj_mat_roof = 0
                roof_angle = 0
                roof_orientation = ''

                for face_proj in faces_roof:
                    if face_proj.material == material_proj:
                        surf_mat_roof = surf_mat_roof + face_proj.area
                        surf_proj_mat_roof = surf_proj_mat_roof + face_proj.projection_area
                        roof_angle = face_proj.angle
                        roof_orientation = face_proj.orientation

                sub_row.label(text=material_proj + ' : ' + str(round(surf_mat_roof, 2)) + " m\xb2", icon="MOD_ARRAY")
                sub_row.label(text='Proj. : ' + str(roof_orientation.name))
                sub_row.label(text='Angle : ' + str(round(math.fabs(math.degrees(roof_angle)), 1)) + " \xb0")
                sub_row.label(text='Proj. surf. : ' + str(round(surf_proj_mat_roof, 2)) + " m\xb2")
                roofpart = SubElement(
                    xml_projections[face_type_id],
                    'RoofPart',
                    Angle=str(round(math.fabs(math.degrees(roof_angle)), 1)),
                    Id=str(material_proj),
                    Orientation=str(roof_orientation.name),
                    Surf=str(round(surf_mat_roof, 2)),
                    SurfProj=str(round(surf_proj_mat_roof, 2))
                )

                tr = SubElement(html_projections[face_type_id], 'tr')
                td_1 = SubElement(tr, 'td')
                td_1.attrib["class"] = "mat_color"

                color = Color()
                for material_slot in bpy.context.object.material_slots:
                    if material_slot.name[0:4] == material_proj:
                        color = material_slot.material.diffuse_color

                td_1.attrib["style"] = "color:" + str(color)
                td_1.text = "\u25A0"
                td_2 = SubElement(tr, 'td')
                td_2.attrib["class"] = "mat_index"
                td_2.text = str(material_proj)
                td_3 = SubElement(tr, 'td')
                td_3.attrib["class"] = "mat_surf_brute"
                td_3.text = str(round(surf_mat_roof, 2)) + " m²"
                td_4 = SubElement(tr, 'td')
                td_4.attrib["class"] = "mat_angle"
                td_4.text = str(round(math.fabs(math.degrees(roof_angle)), 1)) + " °"
                td_5 = SubElement(tr, 'td')
                td_5.attrib["class"] = "mat_orient"
                td_5.text = str(roof_orientation.name)
                td_6 = SubElement(tr, 'td')
                td_6.attrib["class"] = "mat_surf_proj"
                td_6.text = str(round(surf_proj_mat_roof, 2)) + " m²"

        tree.write(temp_file, encoding="UTF-8")
        tree_html.write(temp_file_html, encoding="UTF-8")

        # Resume surfaces par materiau
        row = layout.row()
        row.alignment = 'EXPAND'
        box = row.box()

        for face_type in FaceType:
            column = box.column()
            sub_row = column.row(align=True)
            sub_row.label(text=face_type.get_name(), icon=face_type.get_icon())

            for material_slot in bpy.context.object.material_slots:
                xml_surf_mat = 0

                for face in faces:
                    if material_slot.name[0:4] == face.material:
                        xml_surf_mat += face.area

                if material_slot.name[0] in face_type.get_letters():
                    sub_row = column.row(align=True)
                    sub_row.label(text=material_slot.name[0:4] + "  " + material_slot.name[5:] + " : ")
                    sub_row.label(text=str(round(xml_surf_mat, 2)) + " m\xb2")

        # buttons & credits

        row = layout.row()
        row.operator("export.xml", text="Save")
        row.operator("export.html", text="Export to pdf...")

        row = layout.row()

        #### Only line to change for lite version for Windows
        dirname = os.path.expanduser('~') + '\.blender\ArToKi\labels'

        if bpy.data.images.find('ArToKi.png') == -1:
            img_A_Plus = bpy.data.images.load(os.path.join(dirname, 'ArToKi.png'))
            # TODO: Uncomment use_alpha, if useful.
            # img_A_Plus.use_alpha = True
            img_A_Plus.user_clear()  # Won't get saved into .blend files
        icon_ArToKi = self.layout.icon(bpy.data.images['ArToKi.png'])
        row.label(text="ArToKi - Energy by tmaes" + 60 * " " + "info@tmaes.be", icon_value=icon_ArToKi)
