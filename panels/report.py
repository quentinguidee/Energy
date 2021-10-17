import math
import os
import bpy

from typing import List

from xml.etree.ElementTree import SubElement

from bpy.props import StringProperty, EnumProperty, BoolProperty
from bpy.types import Panel

from ..utils.building import Building, add_walls_to_html, add_floors_to_html, get_all_floors_materials, \
    get_walls_grouped_by_orientation
from ..utils.color import Color
from ..utils.exports import write_tree_in_file, handle_html
from ..utils.face import Face
from ..utils.face_type import FaceType
from ..utils.files import get_path
from ..utils.save import Save


class ARTOKI_PT_EnergyReport(Panel):
    bl_label = "ArToKi - Energy - Report"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ArToKi"

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
        row = self.layout.row()
        row.operator("import.map", text="Import and scale aerial view")

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

    def draw_walls(self, walls: List[Face]):
        walls_grouped_by_orientation = get_walls_grouped_by_orientation(walls)

        for walls_group in walls_grouped_by_orientation:
            row = self.layout.row()
            row.alignment = 'EXPAND'

            box = row.box()
            column = box.column()

            orientation = walls_group['orientation']
            projected_area = walls_group['projected_area']
            materials = walls_group['materials']

            sub_row = column.row(align=True)
            sub_row.label(
                text=str(orientation.name) + " Projection" + (' ' * 10) + "Surface : " + str(
                    round(projected_area, 2)) + " m\xb2",
                icon='CURSOR')

            sub_row = column.row(align=True)
            sub_row.separator()

            for material in materials:
                name = material['name']
                area = material['area']

                sub_row = column.row(align=True)
                sub_row.label(text=5 * ' ' + name + ' : ' + str(round(area, 2)) + " m\xb2", icon='MOD_BUILD')

    def draw_floors(self, floors: List[Face]):
        total_area, materials = get_all_floors_materials(floors)
        total_area = str(round(total_area, 2))

        row = self.layout.row()
        row.alignment = 'EXPAND'

        box = row.box()
        column = box.column()

        if total_area == 0:
            return

        sub_row = column.row(align=True)
        sub_row.label(text="Floors Projection     Surface : " + total_area + " m\xb2", icon="TEXTURE")
        sub_row = column.row(align=True)
        sub_row.separator()

        for material in materials:
            name = material['name']
            area = material['area']

            sub_row = column.row(align=True)
            sub_row.label(text=5 * ' ' + name + ' : ' + str(round(area, 2)) + " m\xb2", icon="ASSET_MANAGER")

    def draw_roofs(self, roofs: List[Face], html_projections, tree_html):
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
                material_area = 0
                for face in faces:
                    if material_slot.name[0:4] == face.material:
                        material_area += face.area

                if material_slot.name[0] in face_type.get_letters():
                    sub_row = column.row(align=True)
                    sub_row.label(text=material_slot.name[0:4] + "  " + material_slot.name[5:] + " : ")
                    sub_row.label(text=str(round(material_area, 2)) + " m\xb2")

    def draw_processor_info(self, context):
        layout = self.layout
        properties = context.preferences.addons["energy"].preferences

        last_name = properties["atk_processor_last_name"]
        first_name = properties["atk_processor_first_name"]

        layout.row().label(text="Will be signed as " + last_name + " " + first_name + ".", icon="USER")
        layout.row().operator("object.open_preferences", text="Edit signature")

    def draw_exports(self):
        row = self.layout.row()
        row.operator("export.html", text="Export to pdf...")
        row.operator("export.pace", text="Export to Pace...")

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

    def save(self, building: Building):
        Save.reset()
        Save.building = building

    def draw(self, context):
        building = Building(context.object)

        walls = building.get_faces(FaceType.WALL)
        floors = building.get_faces(FaceType.FLOOR)
        roofs = building.get_faces(FaceType.ROOF)

        html_projections, html_tree, html_temp_file = handle_html(building)
        add_walls_to_html(walls, html_projections)
        add_floors_to_html(floors, html_projections, html_tree)

        self.draw_properties()

        self.draw_volume_and_area(building.eval_volume(), building.eval_area())

        self.draw_subtitle(text=FaceType.WALL.get_name())
        self.draw_walls(walls)

        self.draw_subtitle(text=FaceType.FLOOR.get_name())
        self.draw_floors(floors)

        self.draw_subtitle(text=FaceType.ROOF.get_name())
        self.draw_roofs(roofs, html_projections, html_tree)

        self.draw_subtitle(text="Summary")
        self.draw_summary(building.faces)

        self.draw_processor_info(context)

        self.layout.separator()

        self.draw_exports()
        self.draw_credits()

        self.save(building)

        write_tree_in_file(html_tree, html_temp_file)
