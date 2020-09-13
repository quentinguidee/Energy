import os
import bpy


class EnergyDeperditions(bpy.types.Panel):
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
        ('Ground', 'Ground', 'Ground'), ('Heated space', 'Heated space', 'Heated space')
    ]

    materials = [
        ('Free air', 'Free air', 'Free air', 0),
        ('Semi Static air', 'Semi Static air', 'Semi Static air', 1),
        ('Static air', 'Static air', 'Static air', 2),
        ('Masonry', 'Masonry', 'Masonry', 3),
        ('Wood', 'Wood', 'Wood', 4),
        ('Insulation', 'Insulation', 'Insulation', 5),
    ]

    bpy.types.Material.mat_color = bpy.types.Material.myColor = bpy.props.FloatVectorProperty(name="myColor",
                                                                                              subtype="COLOR", size=4,
                                                                                              min=0.0, max=1.0,
                                                                                              default=(
                                                                                                  0.75, 0.0, 0.8, 1.0))
    bpy.types.Material.mat_layers = bpy.props.EnumProperty(items=levels, name="Material layers", default='0')
    bpy.types.Material.mat_environnement = bpy.props.EnumProperty(items=environnement, name="Outside conditions",
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
        scene = bpy.context.scene
        mat = bpy.context.object.active_material
        R_tot = 0
        U_tot = 0
        Air = 0
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
        row.prop(mat, 'mat_layers', text="")
        row.label(text="Environnement:")
        row.prop(mat, 'mat_environnement', text="")
        row = layout.row()
        row.label(text="Outside", icon="LIGHT_SUN")

        dirname = os.path.expanduser('~') + '/.blender/ArToKi/labels'

        # Those should be serialized:

        if bpy.data.images.find('ArToKi.png') == -1:
            img = bpy.data.images.load(os.path.join(dirname, 'ArToKi.png'))
            img.use_alpha = True
            img.user_clear()  # Won't get saved into .blend files

        if bpy.data.images.find('A_Plus_Plus.png') == -1:
            img = bpy.data.images.load(os.path.join(dirname, 'A_Plus_Plus.png'))
            img.use_alpha = True
            img.user_clear()  # Won't get saved into .blend files

        if bpy.data.images.find('A_Plus.png') == -1:
            img = bpy.data.images.load(os.path.join(dirname, 'A_Plus.png'))
            img.use_alpha = True
            img.user_clear()  # Won't get saved into .blend files

        if bpy.data.images.find('A.png') == -1:
            img = bpy.data.images.load(os.path.join(dirname, 'A.png'))
            img.use_alpha = True
            img.user_clear()  # Won't get saved into .blend files

        if bpy.data.images.find('B.png') == -1:
            img = bpy.data.images.load(os.path.join(dirname, 'B.png'))
            img.use_alpha = True
            img.user_clear()  # Won't get saved into .blend files

        if bpy.data.images.find('C.png') == -1:
            img = bpy.data.images.load(os.path.join(dirname, 'C.png'))
            img.use_alpha = True
            img.user_clear()  # Won't get saved into .blend files

        if bpy.data.images.find('D.png') == -1:
            img = bpy.data.images.load(os.path.join(dirname, 'D.png'))
            img.use_alpha = True
            img.user_clear()  # Won't get saved into .blend files

        if bpy.data.images.find('E.png') == -1:
            img = bpy.data.images.load(os.path.join(dirname, 'E.png'))
            img.use_alpha = True
            img.user_clear()  # Won't get saved into .blend files

        if bpy.data.images.find('F.png') == -1:
            img = bpy.data.images.load(os.path.join(dirname, 'F.png'))
            img.use_alpha = True
            img.user_clear()  # Won't get saved into .blend files

        if bpy.data.images.find('G.png') == -1:
            img = bpy.data.images.load(os.path.join(dirname, 'G.png'))
            img.use_alpha = True
            img.user_clear()  # Won't get saved into .blend files

        for i in range(int(mat.mat_layers)):
            row = layout.row()
            box = row.box()
            col = box.column()
            subrow = col.row(align=True)
            subrow.alignment = 'EXPAND'
            subrow.label(text="Level " + str(i + 1), icon='SORTSIZE')
            R_mat = 0
            U_mat = 0
            if mat.name[0:1] == 'M' or mat.name[0:1] == 'W':
                if getattr(mat, 'materials_' + str(i + 1)) == 'Semi Static air':
                    Air = 1
                    if getattr(mat, 'mat_depth_' + str(i + 1)) != 0:
                        R_mat = 0.09
                        U_mat = 1 / R_mat

                elif getattr(mat, 'materials_' + str(i + 1)) == 'Static air':
                    Air = 2
                    if getattr(mat, 'mat_depth_' + str(i + 1)) != 0:
                        R_mat = 0.18
                        U_mat = 1 / R_mat
                elif getattr(mat, 'materials_' + str(i + 1)) == 'Free air':
                    Air = 0
                    if getattr(mat, 'mat_depth_' + str(i + 1)) != 0:
                        R_mat = 0
                        U_mat = 0
            if mat.name[0:1] == 'S' or mat.name[0:1] == 'F':
                if getattr(mat, 'materials_' + str(i + 1)) == 'Semi Static air':
                    Air = 1
                    if getattr(mat, 'mat_depth_' + str(i + 1)) != 0:
                        R_mat = 0.1
                        U_mat = 1 / R_mat

                elif getattr(mat, 'materials_' + str(i + 1)) == 'Static air':
                    Air = 2
                    if getattr(mat, 'mat_depth_' + str(i + 1)) != 0:
                        R_mat = 0.19
                        U_mat = 1 / R_mat
                elif getattr(mat, 'materials_' + str(i + 1)) == 'Free air':
                    Air = 0
                    if getattr(mat, 'mat_depth_' + str(i + 1)) != 0:
                        R_mat = 0
                        U_mat = 0
            if mat.name[0:1] == 'T' or mat.name[0:1] == 'R':
                if getattr(mat, 'materials_' + str(i + 1)) == 'Semi Static air':
                    Air = 1
                    if getattr(mat, 'mat_depth_' + str(i + 1)) != 0:
                        R_mat = 0.08
                        U_mat = 1 / R_mat

                elif getattr(mat, 'materials_' + str(i + 1)) == 'Static air':
                    Air = 2
                    if getattr(mat, 'mat_depth_' + str(i + 1)) != 0:
                        R_mat = 0.16
                        U_mat = 1 / R_mat
                elif getattr(mat, 'materials_' + str(i + 1)) == 'Free air':
                    Air = 0
                    if getattr(mat, 'mat_depth_' + str(i + 1)) != 0:
                        R_mat = 0
                        U_mat = 0
            if getattr(mat, 'mat_lambda_i_' + str(i + 1)) != 0:
                R_mat = getattr(mat, 'mat_depth_' + str(i + 1)) / 100 / getattr(mat, 'mat_lambda_i_' + str(i + 1))

                if getattr(mat, 'mat_depth_' + str(i + 1)) != 0:
                    U_mat = 1 / R_mat
            R_levels.append(round(R_mat, 2))

            subrow.label(text="R = " + str(round(R_mat, 3)) + " m².K/W")  # +"mat_R_"+str(i+1))
            # subrow.label(text="U = "+str(round(U_mat,2))+" W/m².K")   #+"mat_R_"+str(i+1))
            subrow.prop(mat, 'materials_' + str(i + 1), text="")

            row = box.row(align=True)
            row.alignment = 'LEFT'
            row.prop(mat, 'mat_depth_' + str(i + 1), text="Depth (cm)")
            row.prop(mat, 'mat_lambda_i_' + str(i + 1), text="λi (W/mK)")

            # for more precision #row.prop(bpy.data.materials[mat.name],'mat_lambda_e_'+str(i+1),text="λe(W/mK)")# function to precise... λe for humidity
            # for more precision #row.prop(bpy.data.materials[mat.name],'mat_exterior_'+str(i+1),text="Exterior")

        row = layout.row()
        row.label(text="Inside", icon='UGLYPACKAGE')
        if mat.mat_environnement == 'Outside' or mat.mat_environnement == 'Ground':
            if Air == 1 or Air == 2:
                W_Rse = 0.04
                G_Rse = 0.04
                R_Rse = 0.04

                # Rtot calculation

        if sum(R_levels) != 0:
            if mat.name[0:1] == 'M' or mat.name[0:1] == 'W':
                R_tot = W_Rse + sum(R_levels) + W_Rsi
            if mat.name[0:1] == 'S' or mat.name[0:1] == 'F':
                R_tot = G_Rse + sum(R_levels) + G_Rsi
            if mat.name[0:1] == 'T' or mat.name[0:1] == 'R':
                R_tot = R_Rse + sum(R_levels) + R_Rsi
            if R_tot != 0:
                U_tot = 1 / R_tot
        row = layout.row()
        box = row.box()
        col = box.column()
        subrow = col.row(align=True)
        subrow.alignment = 'LEFT'
        icon_A_Plus_Plus = self.layout.icon(bpy.data.images['A_Plus_Plus.png'])
        icon_A_Plus = self.layout.icon(bpy.data.images['A_Plus.png'])
        icon_A = self.layout.icon(bpy.data.images['A.png'])
        icon_B = self.layout.icon(bpy.data.images['B.png'])
        icon_C = self.layout.icon(bpy.data.images['C.png'])
        icon_D = self.layout.icon(bpy.data.images['D.png'])
        icon_E = self.layout.icon(bpy.data.images['E.png'])
        icon_F = self.layout.icon(bpy.data.images['F.png'])
        icon_G = self.layout.icon(bpy.data.images['G.png'])

        # Label assign

        if mat.name[0:1] == 'M' or mat.name[0:1] == 'W':
            if round(U_tot, 3) <= 0.15:
                subrow.label(text="", icon_value=icon_A_Plus_Plus)
            #                if scene.atk_therm_col == True:
            #                    mat.diffuse_color=((0,0.215686275,0.090196078))
            elif 0.15 < round(U_tot, 3) <= 0.18:
                subrow.label(text="", icon_value=icon_A_Plus)
                # mat.diffuse_color=((0.02,0.41,0.19))
            elif 0.18 < round(U_tot, 3) <= 0.24:
                subrow.label(text="", icon_value=icon_A)
                # mat.diffuse_color=((0.26,0.54,0.01))
            elif 0.24 < round(U_tot, 3) <= 0.32:
                subrow.label(text="", icon_value=icon_B)
            elif 0.32 < round(U_tot, 3) <= 0.40:
                subrow.label(text="", icon_value=icon_C)
            elif 0.40 < round(U_tot, 3) <= 0.60:
                subrow.label(text="", icon_value=icon_D)
            elif 0.60 < round(U_tot, 3) <= 0.90:
                subrow.label(text="", icon_value=icon_E)
            elif 0.90 < round(U_tot, 3) <= 1.6:
                subrow.label(text="", icon_value=icon_F)
            elif 1.6 < round(U_tot, 3):
                subrow.label(text="", icon_value=icon_G)

        if mat.name[0:1] == 'S' or mat.name[0:1] == 'F':
            if round(U_tot, 3) <= 0.15:
                subrow.label(text="", icon_value=icon_A_Plus_Plus)
                # mat.diffuse_color=((0,0.215686275,0.090196078))
            elif 0.15 < round(U_tot, 3) <= 0.18:
                subrow.label(text="", icon_value=icon_A_Plus)
                # mat.diffuse_color=((0.02,0.41,0.19))
            elif 0.18 < round(U_tot, 3) <= 0.30:
                subrow.label(text="", icon_value=icon_A)
                # mat.diffuse_color=((0.26,0.54,0.01))
            elif 0.30 < round(U_tot, 3) <= 0.35:
                subrow.label(text="", icon_value=icon_B)
            elif 0.35 < round(U_tot, 3) <= 0.40:
                subrow.label(text="", icon_value=icon_C)
            elif 0.40 < round(U_tot, 3) <= 0.60:
                subrow.label(text="", icon_value=icon_D)
            elif 0.60 < round(U_tot, 3) <= 0.90:
                subrow.label(text="", icon_value=icon_E)
            elif 0.90 < round(U_tot, 3) <= 1.6:
                subrow.label(text="", icon_value=icon_F)
            elif 1.6 < round(U_tot, 3):
                subrow.label(text="", icon_value=icon_G)

        if mat.name[0:1] == 'T' or mat.name[0:1] == 'R':
            if round(U_tot, 3) <= 0.15:
                subrow.label(text="", icon_value=icon_A_Plus_Plus)
                # mat.diffuse_color=((0,0.215686275,0.090196078))
            elif 0.15 < round(U_tot, 3) <= 0.18:
                subrow.label(text="", icon_value=icon_A_Plus)
                # mat.diffuse_color=((0.02,0.41,0.19))
            elif 0.18 < round(U_tot, 3) <= 0.24:
                subrow.label(text="", icon_value=icon_A)
                # mat.diffuse_color=((0.26,0.54,0.01))
            elif 0.24 < round(U_tot, 3) <= 0.27:
                subrow.label(text="", icon_value=icon_B)
            elif 0.27 < round(U_tot, 3) <= 0.30:
                subrow.label(text="", icon_value=icon_C)
            elif 0.30 < round(U_tot, 3) <= 0.40:
                subrow.label(text="", icon_value=icon_D)
            elif 0.40 < round(U_tot, 3) <= 0.65:
                subrow.label(text="", icon_value=icon_E)
            elif 0.65 < round(U_tot, 3) <= 1.80:
                subrow.label(text="", icon_value=icon_F)
            elif 1.8 < round(U_tot, 3):
                subrow.label(text="", icon_value=icon_G)

        subrow.label(text="  Rt = " + str(round(R_tot, 3)) + " m².K/W             U= " + str(round(U_tot,
                                                                                                   3)) + " W/m².K          ")  # +str(mat.mat_layers)  +str(W_Rse)+"    "+str(W_Rsi)+"    "+str(Air)+"    "+str(R_levels) )

#        subrow = col.row(align=True)
#        subrow.label(text="#dev Levels: "+str(mat.mat_layers)  +"     W_R se: "+str(W_Rse)+"     W_R si: "+str(W_Rsi)+"     Air : "+str(Air)+"     R levels: "+str(R_levels))
#        subrow = col.row(align=True)
#        subrow.label(text="#dev Levels: "+str(mat.mat_layers)  +"     G_R se: "+str(G_Rse)+"     G_R si: "+str(G_Rsi)+"     Air : "+str(Air)+"     R levels: "+str(R_levels))
#        subrow = col.row(align=True)
#        subrow.label(text="#dev Levels: "+str(mat.mat_layers)  +"     R_R se: "+str(R_Rse)+"     R_R si: "+str(R_Rsi)+"     Air : "+str(Air)+"     R levels: "+str(R_levels))
