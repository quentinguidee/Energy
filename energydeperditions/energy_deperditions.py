import os
import bpy

from .classes.MaterialType import MaterialType

from .. import info
from ..classes.face_type import FaceType


class OBJECT_PT_ArToKi_EnergyDeperditions(bpy.types.Panel):
    bl_label = "ArToKi - Energy - Deperditions (alpha)"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    levels = []
    for i in range(0, 11):
        levels.append((str(i), str(i), "Layers composing walls, roofs etc..."))

    environnement = [
        ('Outside', 'Outside', 'Outside'),
        ('Unprotected space', 'Unprotected space', 'Unprotected space'),
        ('Protected space (no freeze)', 'Protected space (no freeze)', 'Protected space (no freeze)'),
        ('Ground', 'Ground', 'Ground'),
        ('Heated space', 'Heated space', 'Heated space')
    ]

    materials = MaterialType.as_blender_enum()

    bpy.types.Material.mat_color = bpy.types.Material.myColor = bpy.props.FloatVectorProperty(
        name="myColor",
        subtype="COLOR", size=4,
        min=0.0, max=1.0,
        default=(0.75, 0.0, 0.8, 1.0))

    bpy.types.Material.mat_layers = bpy.props.EnumProperty(
        items=levels,
        name="Material layers",
        default='0')

    bpy.types.Material.mat_environnement = bpy.props.EnumProperty(
        items=environnement,
        name="Outside conditions",
        default='Outside')

    bpy.types.Material.mat_depth_1 = bpy.props.FloatProperty(name="Material 1 depth", precision=1)
    bpy.types.Material.mat_depth_2 = bpy.props.FloatProperty(name="Material 2 depth", precision=1)
    bpy.types.Material.mat_depth_3 = bpy.props.FloatProperty(name="Material 3 depth", precision=1)
    bpy.types.Material.mat_depth_4 = bpy.props.FloatProperty(name="Material 4 depth", precision=1)
    bpy.types.Material.mat_depth_5 = bpy.props.FloatProperty(name="Material 5 depth", precision=1)
    bpy.types.Material.mat_depth_6 = bpy.props.FloatProperty(name="Material 6 depth", precision=1)
    bpy.types.Material.mat_depth_7 = bpy.props.FloatProperty(name="Material 7 depth", precision=1)
    bpy.types.Material.mat_depth_8 = bpy.props.FloatProperty(name="Material 8 depth", precision=1)
    bpy.types.Material.mat_depth_9 = bpy.props.FloatProperty(name="Material 9 depth", precision=1)
    bpy.types.Material.mat_depth_10 = bpy.props.FloatProperty(name="Material 10 depth", precision=1)

    bpy.types.Material.mat_lambda_i_1 = bpy.props.FloatProperty(name="Material 1 lambda_i", precision=3)
    bpy.types.Material.mat_lambda_i_2 = bpy.props.FloatProperty(name="Material 2 lambda_i", precision=3)
    bpy.types.Material.mat_lambda_i_3 = bpy.props.FloatProperty(name="Material 3 lambda_i", precision=3)
    bpy.types.Material.mat_lambda_i_4 = bpy.props.FloatProperty(name="Material 4 lambda_i", precision=3)
    bpy.types.Material.mat_lambda_i_5 = bpy.props.FloatProperty(name="Material 5 lambda_i", precision=3)
    bpy.types.Material.mat_lambda_i_6 = bpy.props.FloatProperty(name="Material 6 lambda_i", precision=3)
    bpy.types.Material.mat_lambda_i_7 = bpy.props.FloatProperty(name="Material 7 lambda_i", precision=3)
    bpy.types.Material.mat_lambda_i_8 = bpy.props.FloatProperty(name="Material 8 lambda_i", precision=3)
    bpy.types.Material.mat_lambda_i_9 = bpy.props.FloatProperty(name="Material 9 lambda_i", precision=3)
    bpy.types.Material.mat_lambda_i_10 = bpy.props.FloatProperty(name="Material 10 lambda_i", precision=3)

    bpy.types.Material.mat_lambda_e_1 = bpy.props.FloatProperty(name="Material 1 lambda_e", precision=3)
    bpy.types.Material.mat_lambda_e_2 = bpy.props.FloatProperty(name="Material 2 lambda_e", precision=3)
    bpy.types.Material.mat_lambda_e_3 = bpy.props.FloatProperty(name="Material 3 lambda_e", precision=3)
    bpy.types.Material.mat_lambda_e_4 = bpy.props.FloatProperty(name="Material 4 lambda_e", precision=3)
    bpy.types.Material.mat_lambda_e_5 = bpy.props.FloatProperty(name="Material 5 lambda_e", precision=3)
    bpy.types.Material.mat_lambda_e_6 = bpy.props.FloatProperty(name="Material 6 lambda_e", precision=3)
    bpy.types.Material.mat_lambda_e_7 = bpy.props.FloatProperty(name="Material 7 lambda_e", precision=3)
    bpy.types.Material.mat_lambda_e_8 = bpy.props.FloatProperty(name="Material 8 lambda_e", precision=3)
    bpy.types.Material.mat_lambda_e_9 = bpy.props.FloatProperty(name="Material 9 lambda_e", precision=3)
    bpy.types.Material.mat_lambda_e_10 = bpy.props.FloatProperty(name="Material 10 lambda_e", precision=3)

    bpy.types.Material.mat_R_1 = 0
    bpy.types.Material.mat_R_2 = bpy.props.FloatProperty(name="Material 2 R", precision=2)
    bpy.types.Material.mat_R_3 = bpy.props.FloatProperty(name="Material 3 R", precision=2)
    bpy.types.Material.mat_R_4 = bpy.props.FloatProperty(name="Material 4 R", precision=2)
    bpy.types.Material.mat_R_5 = bpy.props.FloatProperty(name="Material 5 R", precision=2)
    bpy.types.Material.mat_R_6 = bpy.props.FloatProperty(name="Material 6 R", precision=2)
    bpy.types.Material.mat_R_7 = bpy.props.FloatProperty(name="Material 7 R", precision=2)
    bpy.types.Material.mat_R_8 = bpy.props.FloatProperty(name="Material 8 R", precision=2)
    bpy.types.Material.mat_R_9 = bpy.props.FloatProperty(name="Material 9 R", precision=2)
    bpy.types.Material.mat_R_10 = bpy.props.FloatProperty(name="Material 10 R", precision=2)

    bpy.types.Material.materials_1 = bpy.props.EnumProperty(items=materials, name="Materials", default='Free air')
    bpy.types.Material.materials_2 = bpy.props.EnumProperty(items=materials, name="Materials", default='Free air')
    bpy.types.Material.materials_3 = bpy.props.EnumProperty(items=materials, name="Materials", default='Free air')
    bpy.types.Material.materials_4 = bpy.props.EnumProperty(items=materials, name="Materials", default='Free air')
    bpy.types.Material.materials_5 = bpy.props.EnumProperty(items=materials, name="Materials", default='Free air')
    bpy.types.Material.materials_6 = bpy.props.EnumProperty(items=materials, name="Materials", default='Free air')
    bpy.types.Material.materials_7 = bpy.props.EnumProperty(items=materials, name="Materials", default='Free air')
    bpy.types.Material.materials_8 = bpy.props.EnumProperty(items=materials, name="Materials", default='Free air')
    bpy.types.Material.materials_9 = bpy.props.EnumProperty(items=materials, name="Materials", default='Free air')
    bpy.types.Material.materials_10 = bpy.props.EnumProperty(items=materials, name="Materials", default='Free air')

    def draw(self, context):
        layout = self.layout

        material = bpy.context.object.active_material
        material_type: MaterialType = MaterialType.FreeAir
        face_type: FaceType = FaceType.get_face_type(material.name[0:1])

        R_tot = 0
        U_tot = 0
        W_Rse = 0.13
        W_Rsi = 0.13
        G_Rse = 0.17
        G_Rsi = 0.17
        R_Rse = 0.1
        R_Rsi = 0.1
        R_levels = []

        row = layout.row(align=True)
        row.alignment = 'LEFT'
        row.label(text="Levels:")
        row.prop(material, 'mat_layers', text="")
        row.label(text="Environnement:")
        row.prop(material, 'mat_environnement', text="")
        row = layout.row()
        row.label(text="Outside", icon="LIGHT_SUN")

        dirname = os.path.expanduser('~') + info.INSTALL_PATH + '/labels'

        # Those should be serialized:

        images_src = [
            'ArToKi',
            'A_Plus_Plus',
            'A_Plus',
            'A', 'B', 'C', 'D', 'E', 'F', 'G'
        ]

        for image_src in images_src:
            if bpy.data.images.find(image_src + ".png") == -1:
                img = bpy.data.images.load(os.path.join(dirname, image_src + ".png"))
                img.user_clear()  # Won't get saved into .blend files

        for i in range(int(material.mat_layers)):
            row = layout.row()
            box = row.box()
            col = box.column()
            subrow = col.row(align=True)
            subrow.alignment = 'EXPAND'
            subrow.label(text="Level " + str(i + 1), icon='SORTSIZE')
            R_mat = 0
            U_mat = 0

            material_type_name = getattr(material, 'materials_' + str(i + 1))
            material_depth = getattr(material, 'mat_depth_' + str(i + 1))

            if material_type_name == MaterialType.SemiStaticAir.get_name():
                material_type = MaterialType.SemiStaticAir
                if material_depth != 0:
                    if face_type == FaceType.WALL:
                        R_mat = 0.09
                    elif face_type == FaceType.FLOOR:
                        R_mat = 0.1
                    elif face_type == FaceType.ROOF:
                        R_mat = 0.08

            elif material_type_name == MaterialType.StaticAir.get_name():
                material_type = MaterialType.StaticAir
                if material_depth != 0:
                    if face_type == FaceType.WALL:
                        R_mat = 0.18
                    elif face_type == FaceType.FLOOR:
                        R_mat = 0.19
                    elif face_type == FaceType.ROOF:
                        R_mat = 0.16

            elif getattr(material, 'materials_' + str(i + 1)) == MaterialType.FreeAir.get_name():
                material_type = MaterialType.FreeAir
                R_mat = 0
                U_mat = 0

            if getattr(material, 'mat_lambda_i_' + str(i + 1)) != 0:
                R_mat = \
                    getattr(material, 'mat_depth_' + str(i + 1)) / 100 / getattr(material, 'mat_lambda_i_' + str(i + 1))

            if material_depth != 0 and R_mat != 0:
                U_mat = 1 / R_mat

            R_levels.append(round(R_mat, 2))

            subrow.label(text="R = " + str(round(R_mat, 3)) + " m².K/W")  # +"mat_R_"+str(i+1))
            # subrow.label(text="U = "+str(round(U_mat,2))+" W/m².K")   #+"mat_R_"+str(i+1))
            subrow.prop(material, 'materials_' + str(i + 1), text="")

            row = box.row(align=True)
            row.alignment = 'LEFT'
            row.prop(material, 'mat_depth_' + str(i + 1), text="Depth (cm)")
            row.prop(material, 'mat_lambda_i_' + str(i + 1), text="λi (W/mK)")

            # for more precision:
            # row.prop(bpy.data.materials[mat.name],'mat_lambda_e_'+str(i+1),text="λe(W/mK)")# function to precise... λe for humidity

            # for more precision:
            # row.prop(bpy.data.materials[mat.name],'mat_exterior_'+str(i+1),text="Exterior")

        row = layout.row()
        row.label(text="Inside", icon='UGLYPACKAGE')
        if material.mat_environnement == 'Outside' or material.mat_environnement == 'Ground':
            if material_type == MaterialType.SemiStaticAir or material_type == MaterialType.StaticAir:
                W_Rse = 0.04
                G_Rse = 0.04
                R_Rse = 0.04

        if sum(R_levels) != 0:

            if face_type == FaceType.WALL:
                R_tot = W_Rse + sum(R_levels) + W_Rsi
            elif face_type == FaceType.FLOOR:
                R_tot = G_Rse + sum(R_levels) + G_Rsi
            elif face_type == FaceType.ROOF:
                R_tot = R_Rse + sum(R_levels) + R_Rsi

            if R_tot != 0:
                U_tot = 1 / R_tot

        row = layout.row()
        box = row.box()
        col = box.column()
        subrow = col.row(align=True)
        subrow.alignment = 'LEFT'

        icon_a_plus_plus = self.layout.icon(bpy.data.images['A_Plus_Plus.png'])
        icon_a_plus = self.layout.icon(bpy.data.images['A_Plus.png'])
        icon_a = self.layout.icon(bpy.data.images['A.png'])
        icon_b = self.layout.icon(bpy.data.images['B.png'])
        icon_c = self.layout.icon(bpy.data.images['C.png'])
        icon_d = self.layout.icon(bpy.data.images['D.png'])
        icon_e = self.layout.icon(bpy.data.images['E.png'])
        icon_f = self.layout.icon(bpy.data.images['F.png'])
        icon_g = self.layout.icon(bpy.data.images['G.png'])

        # Label assign

        if face_type == FaceType.WALL:
            if round(U_tot, 3) <= 0.15:
                subrow.label(text="", icon_value=icon_a_plus_plus)
            #                if scene.atk_therm_col == True:
            #                    mat.diffuse_color=((0,0.215686275,0.090196078))
            elif 0.15 < round(U_tot, 3) <= 0.18:
                subrow.label(text="", icon_value=icon_a_plus)
                # mat.diffuse_color=((0.02,0.41,0.19))
            elif 0.18 < round(U_tot, 3) <= 0.24:
                subrow.label(text="", icon_value=icon_a)
                # mat.diffuse_color=((0.26,0.54,0.01))
            elif 0.24 < round(U_tot, 3) <= 0.32:
                subrow.label(text="", icon_value=icon_b)
            elif 0.32 < round(U_tot, 3) <= 0.40:
                subrow.label(text="", icon_value=icon_c)
            elif 0.40 < round(U_tot, 3) <= 0.60:
                subrow.label(text="", icon_value=icon_d)
            elif 0.60 < round(U_tot, 3) <= 0.90:
                subrow.label(text="", icon_value=icon_e)
            elif 0.90 < round(U_tot, 3) <= 1.6:
                subrow.label(text="", icon_value=icon_f)
            elif 1.6 < round(U_tot, 3):
                subrow.label(text="", icon_value=icon_g)

        if face_type == FaceType.FLOOR:
            if round(U_tot, 3) <= 0.15:
                subrow.label(text="", icon_value=icon_a_plus_plus)
                # mat.diffuse_color=((0,0.215686275,0.090196078))
            elif 0.15 < round(U_tot, 3) <= 0.18:
                subrow.label(text="", icon_value=icon_a_plus)
                # mat.diffuse_color=((0.02,0.41,0.19))
            elif 0.18 < round(U_tot, 3) <= 0.30:
                subrow.label(text="", icon_value=icon_a)
                # mat.diffuse_color=((0.26,0.54,0.01))
            elif 0.30 < round(U_tot, 3) <= 0.35:
                subrow.label(text="", icon_value=icon_b)
            elif 0.35 < round(U_tot, 3) <= 0.40:
                subrow.label(text="", icon_value=icon_c)
            elif 0.40 < round(U_tot, 3) <= 0.60:
                subrow.label(text="", icon_value=icon_d)
            elif 0.60 < round(U_tot, 3) <= 0.90:
                subrow.label(text="", icon_value=icon_e)
            elif 0.90 < round(U_tot, 3) <= 1.6:
                subrow.label(text="", icon_value=icon_f)
            elif 1.6 < round(U_tot, 3):
                subrow.label(text="", icon_value=icon_g)

        if face_type == FaceType.ROOF:
            if round(U_tot, 3) <= 0.15:
                subrow.label(text="", icon_value=icon_a_plus_plus)
                # mat.diffuse_color=((0,0.215686275,0.090196078))
            elif 0.15 < round(U_tot, 3) <= 0.18:
                subrow.label(text="", icon_value=icon_a_plus)
                # mat.diffuse_color=((0.02,0.41,0.19))
            elif 0.18 < round(U_tot, 3) <= 0.24:
                subrow.label(text="", icon_value=icon_a)
                # mat.diffuse_color=((0.26,0.54,0.01))
            elif 0.24 < round(U_tot, 3) <= 0.27:
                subrow.label(text="", icon_value=icon_b)
            elif 0.27 < round(U_tot, 3) <= 0.30:
                subrow.label(text="", icon_value=icon_c)
            elif 0.30 < round(U_tot, 3) <= 0.40:
                subrow.label(text="", icon_value=icon_d)
            elif 0.40 < round(U_tot, 3) <= 0.65:
                subrow.label(text="", icon_value=icon_e)
            elif 0.65 < round(U_tot, 3) <= 1.80:
                subrow.label(text="", icon_value=icon_f)
            elif 1.8 < round(U_tot, 3):
                subrow.label(text="", icon_value=icon_g)

        subrow.label(text="  Rt = " + str(round(R_tot, 3)) + " m².K/W             U= " + str(
            round(U_tot, 3)) + " W/m².K          ")