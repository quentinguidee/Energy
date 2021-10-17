import math
import os
import bpy

from typing import List

from bpy.props import StringProperty, EnumProperty, BoolProperty
from bpy.types import Panel

from ..utils.building import Building, add_walls_to_html, add_floors_to_html, add_roofs_to_html
from ..utils.building import get_all_floors_materials, get_all_roofs, get_walls_grouped_by_orientation

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
        if total_area == 0:
            return

        total_area = str(round(total_area, 2))

        row = self.layout.row()
        row.alignment = 'EXPAND'

        box = row.box()
        column = box.column()

        sub_row = column.row(align=True)
        sub_row.label(text="Floors Projection     Surface : " + total_area + " m\xb2", icon="TEXTURE")
        sub_row = column.row(align=True)
        sub_row.separator()

        for material in materials:
            name = material['name']
            area = material['area']

            sub_row = column.row(align=True)
            sub_row.label(text=5 * ' ' + name + ' : ' + str(round(area, 2)) + " m\xb2", icon="ASSET_MANAGER")

    def draw_roofs(self, roofs: List[Face]):
        total_projected_area, materials = get_all_roofs(roofs)
        if total_projected_area == 0:
            return

        total_projected_area = str(round(total_projected_area, 2))

        row = self.layout.row()
        row.alignment = 'EXPAND'

        box = row.box()
        column = box.column()

        sub_row = column.row(align=True)
        sub_row.label(text="Roofs Projection     Surface : " + total_projected_area + " m\xb2", icon="LINCURVE")
        sub_row = column.row(align=True)
        sub_row.separator()

        for material in materials:
            sub_row = column.row(align=True)

            name = material['name']
            area = str(round(material['area'], 2))
            orientation = material['orientation']
            angle = material['angle']
            projected_area = str(round(material['projected_area'], 2))

            sub_row.label(text=name + ' : ' + area + " m\xb2", icon="MOD_ARRAY")
            sub_row.label(text='Proj. : ' + str(orientation.name))
            sub_row.label(text='Angle : ' + str(round(math.fabs(math.degrees(angle)), 1)) + " \xb0")
            sub_row.label(text='Proj. surf. : ' + projected_area + " m\xb2")

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

        self.draw_properties()

        self.draw_volume_and_area(building.eval_volume(), building.eval_area())

        self.draw_subtitle(text=FaceType.WALL.get_name())
        self.draw_walls(walls)

        self.draw_subtitle(text=FaceType.FLOOR.get_name())
        self.draw_floors(floors)

        self.draw_subtitle(text=FaceType.ROOF.get_name())
        self.draw_roofs(roofs)

        self.draw_subtitle(text="Summary")
        self.draw_summary(building.faces)

        self.draw_processor_info(context)

        self.layout.separator()

        self.draw_exports()
        self.draw_credits()

        self.save(building)
