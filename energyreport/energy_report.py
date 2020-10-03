import math
import os

from xml.etree.ElementTree import SubElement

from bpy.props import StringProperty, EnumProperty, BoolProperty
from bpy.types import Panel

from .classes.building import Building
from .classes.color import Color
from .classes.face import Face
from .classes.orientation import Orientation

from ..classes.face_type import FaceType
from ..functions import get_path, generate_file, handle_xml, handle_html

import bpy


class OBJECT_PT_ArToKi_EnergyReport(Panel):
    bl_label = "ArToKi - Energy - Report"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    properties = [
        ('atk_procedure_type', "Procedure"),
        ('atk_aerial', "Aerial view path"),
        ('atk_elevation', "Elevation view path"),
        ('atk_address1', "Street, Nb"),
        ('atk_address2', "PostCode City"),
        ('atk_therm_col', "Use thermic colors"),
    ]

    bpy.types.Scene.atk_aerial = StringProperty(
        name="Aerial",
        description="Aerial view path",
        default="",
        subtype='FILE_PATH')

    bpy.types.Scene.atk_elevation = StringProperty(
        name="Elevation",
        description="Elevation view path",
        default="",
        subtype='FILE_PATH')

    bpy.types.Scene.atk_address1 = StringProperty(
        name="Address 1",
        description="Street, nb",
        default="")

    bpy.types.Scene.atk_address2 = StringProperty(
        name="Address 2",
        description="PostCode City",
        default="")

    bpy.types.Scene.atk_therm_col = BoolProperty(
        name="Therm col",
        description="Assign materials colors by performance",
        default=0)

    bpy.types.Scene.atk_procedure_type = EnumProperty(
        items=[('PAE', 'PAE', 'Procédure d\'audit énergétique'),
               ('PEB', 'PEB', 'Performances énergétiques des batiments')],
        name="Procedure type",
        description="Changes the upper left text logo",
        default="PEB")

    def draw_properties(self):
        for prop in self.properties:
            row = self.layout.row()
            row.prop(bpy.context.scene, prop[0], text=prop[1])

    def draw_subtitle(self, text):
        self.layout.separator()
        self.layout.label(text=text)

    def draw_volume_and_area(self, volume, area):
        row = self.layout.row()
        row.alignment = 'EXPAND'

        box = row.box()
        column = box.column()

        sub_row = column.row(align=True)
        sub_row.label(text="Volume of the enveloppe:   " + str(round(volume, 2)) + " m\xb3", icon='VIEW3D')
        sub_row.label(text="Surface of the enveloppe:   " + str(round(area, 2)) + " m\xb2", icon='MESH_GRID')

    def draw_walls(self, walls: [Face], xml_projections, html_projections):
        projection_id = 0
        face_type_id = FaceType.WALL.get_id()

        for orientation in Orientation:
            faces_projections: [Face] = []
            materials_projections = []
            area_projection = 0

            for wall in walls:
                if wall.orientation == orientation:
                    faces_projections.append(wall)
                    area_projection += wall.area

            if area_projection != 0:
                row = self.layout.row()
                row.alignment = 'EXPAND'

                box = row.box()
                column = box.column()

                sub_row = column.row(align=True)
                sub_row.label(
                    text=str(orientation.name) + " Projection          Surface : " + str(
                        round(area_projection, 2)) + " m\xb2",
                    icon='CURSOR')
                # on peut refaire le moteur apd ici...
                sub_row = column.row(align=True)
                sub_row.separator()
                projection = SubElement(xml_projections[face_type_id], 'WallProjection',
                                        Id=str(projection_id),
                                        Orientation=str(orientation.name),
                                        Surf=str(round(area_projection, 2)))

                projection_id += 1

                for face_projection in faces_projections:
                    if materials_projections.count(str(face_projection.material)) == 0:
                        materials_projections.append(face_projection.material)

                for material_proj in sorted(materials_projections):
                    sub_row = column.row(align=True)
                    material_area = 0
                    for face_projection in faces_projections:
                        if face_projection.material == material_proj:
                            material_area += face_projection.area

                    sub_row.label(text=5 * ' ' + material_proj + ' : ' + str(round(material_area, 2)) + " m\xb2",
                                  icon='MOD_BUILD')

                    SubElement(projection, 'WallPart', id=str(material_proj), Surf=str(round(material_area, 2)))

                projection_html_1 = SubElement(html_projections[face_type_id][0][1 if projection_id <= 4 else 2], 'td')
                projection_html_1_table = SubElement(projection_html_1, 'table')
                projection_html_1_table.attrib["id"] = "walls_projection"
                tbody = SubElement(projection_html_1_table, 'tbody')
                caption = SubElement(tbody, 'caption')  # , Orientation=str(p), Surf=str(round(surf_proj,2))
                caption.text = "Az.: " + str(orientation.name) + " - " + str(round(area_projection, 2)) + " m²"

                for face_projection in faces_projections:
                    if materials_projections.count(str(face_projection.material)) == 0:
                        materials_projections.append(face_projection.material)

                for material_proj in sorted(materials_projections):
                    material_area = 0
                    for face_projection in faces_projections:
                        if face_projection.material == material_proj:
                            material_area += face_projection.area

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
                    td_3.text = str(round(material_area, 2)) + " m²"

    def draw_floors(self, floors: [Face], xml_projections, html_projections, tree_html):
        row = self.layout.row()
        row.alignment = 'EXPAND'

        box = row.box()
        column = box.column()

        area = 0
        mat_vert = []
        face_type_id = FaceType.FLOOR.get_id()

        for floor in floors:
            area += floor.projection_area

        if area != 0:
            sub_row = column.row(align=True)
            sub_row.label(text="Floors Projection     Surface : " + str(round(area, 2)) + " m\xb2", icon="TEXTURE")
            sub_row = column.row(align=True)
            sub_row.separator()

            xml_projections[face_type_id].attrib['Surf'] = str(round(area, 2))
            html_projections[face_type_id].attrib['Surf'] = str(round(area, 2))

            caption = tree_html.find(".//table[@id='floors_values']/tbody/caption")
            caption.text = 'Projection Sols: ' + str(round(area, 2)) + ' m²'

            for floor in floors:
                if mat_vert.count(str(floor.material)) == 0:
                    mat_vert.append(floor.material)

            for material_proj in sorted(mat_vert):
                sub_row = column.row(align=True)
                area_material_vert = 0
                for floor in floors:
                    if floor.material == material_proj:
                        area_material_vert += floor.projection_area

                sub_row.label(text=5 * ' ' + material_proj + ' : ' + str(round(area_material_vert, 2)) + " m\xb2",
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
                td_3.text = str(round(area_material_vert, 2)) + " m²"

    def draw_roofs(self, roofs: [Face], xml_projections, html_projections, tree_html):
        row = self.layout.row()
        row.alignment = 'EXPAND'

        box = row.box()
        column = box.column()

        area = 0
        area_projection = 0
        materials = []

        face_type_id = FaceType.ROOF.get_id()

        for roof in roofs:
            area += roof.area
            area_projection += roof.projection_area

        if area != 0:
            sub_row = column.row(align=True)
            sub_row.label(text="Roofs Projection     Surface : " + str(round(area_projection, 2)) + " m\xb2",
                          icon="LINCURVE")
            sub_row = column.row(align=True)
            sub_row.separator()

            xml_projections[face_type_id].attrib['Surf'] = str(round(area_projection, 2))
            html_projections[face_type_id].attrib['Surf'] = str(round(area_projection, 2))

            caption = tree_html.find(".//table[@id='roofs_values']/tbody/caption")
            caption.text = 'Projection Toitures: ' + str(round(area_projection, 2)) + ' m²'

            for roof in roofs:
                if materials.count(str(roof.material)) == 0:
                    materials.append(roof.material)

            for material_proj in sorted(materials):
                sub_row = column.row(align=True)
                area_material_roof = 0
                area_projection_material_roof = 0
                roof_angle = 0
                roof_orientation = ''

                for roof in roofs:
                    if roof.material == material_proj:
                        area_material_roof += roof.area
                        area_projection_material_roof += roof.projection_area
                        roof_angle = roof.angle
                        roof_orientation = roof.orientation

                sub_row.label(text=material_proj + ' : ' + str(round(area_material_roof, 2)) + " m\xb2",
                              icon="MOD_ARRAY")
                sub_row.label(text='Proj. : ' + str(roof_orientation.name))
                sub_row.label(text='Angle : ' + str(round(math.fabs(math.degrees(roof_angle)), 1)) + " \xb0")
                sub_row.label(text='Proj. surf. : ' + str(round(area_projection_material_roof, 2)) + " m\xb2")

                SubElement(
                    xml_projections[face_type_id],
                    'RoofPart',
                    Angle=str(round(math.fabs(math.degrees(roof_angle)), 1)),
                    Id=str(material_proj),
                    Orientation=str(roof_orientation.name),
                    Surf=str(round(area_material_roof, 2)),
                    SurfProj=str(round(area_projection_material_roof, 2))
                )

                tr = SubElement(html_projections[face_type_id], 'tr')
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
                td_3.attrib["class"] = "mat_surf_brute"
                td_3.text = str(round(area_material_roof, 2)) + " m²"
                td_4 = SubElement(tr, 'td')
                td_4.attrib["class"] = "mat_angle"
                td_4.text = str(round(math.fabs(math.degrees(roof_angle)), 1)) + " °"
                td_5 = SubElement(tr, 'td')
                td_5.attrib["class"] = "mat_orient"
                td_5.text = str(roof_orientation.name)
                td_6 = SubElement(tr, 'td')
                td_6.attrib["class"] = "mat_surf_proj"
                td_6.text = str(round(area_projection_material_roof, 2)) + " m²"

    def draw_summary(self, faces):
        row = self.layout.row()
        row.alignment = 'EXPAND'
        box = row.box()

        for face_type in FaceType:
            column = box.column()
            sub_row = column.row(align=True)
            sub_row.label(text=face_type.get_name(), icon=face_type.get_icon())

            for material_slot in bpy.context.object.material_slots:
                xml_material_area = 0

                for face in faces:
                    if material_slot.name[0:4] == face.material:
                        xml_material_area += face.area

                if material_slot.name[0] in face_type.get_letters():
                    sub_row = column.row(align=True)
                    sub_row.label(text=material_slot.name[0:4] + "  " + material_slot.name[5:] + " : ")
                    sub_row.label(text=str(round(xml_material_area, 2)) + " m\xb2")

    def draw_exports(self):
        row = self.layout.row()
        row.operator("export.xml", text="Save")
        row.operator("export.html", text="Export to pdf...")

    def draw_credits(self):
        # Only line to change for lite version for Windows
        dirname = get_path('labels')

        img_src = 'ArToKi.png'
        if bpy.data.images.find(img_src) == -1:
            img_a_plus = bpy.data.images.load(os.path.join(dirname, img_src))
            img_a_plus.user_clear()  # Won't get saved into .blend files

        row = self.layout.row()
        icon_artoki = self.layout.icon(bpy.data.images[img_src])
        row.label(text="ArToKi - Energy by tmaes" + 60 * " " + " info@tmaes.be", icon_value=icon_artoki)

    def draw(self, context):
        building = Building(context.object)

        xml_projections, xml_tree, xml_temp_file = handle_xml(building)
        html_projections, html_tree, html_temp_file = handle_html(building)

        self.draw_properties()

        self.draw_volume_and_area(building.eval_volume(), building.eval_area())

        self.draw_subtitle(text=FaceType.WALL.get_name())
        self.draw_walls(building.get_faces(FaceType.WALL), xml_projections, html_projections)

        self.draw_subtitle(text=FaceType.FLOOR.get_name())
        self.draw_floors(building.get_faces(FaceType.FLOOR), xml_projections, html_projections, html_tree)

        self.draw_subtitle(text=FaceType.ROOF.get_name())
        self.draw_roofs(building.get_faces(FaceType.ROOF), xml_projections, html_projections, html_tree)

        self.draw_subtitle(text="Summary")
        self.draw_summary(building.faces)

        self.draw_exports()
        self.draw_credits()

        generate_file(xml_tree, xml_temp_file)
        generate_file(html_tree, html_temp_file)
