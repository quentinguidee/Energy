import bpy
import random
import mathutils

from bpy.types import Panel


class ARTOKI_PT_create_material(Panel):
    bl_label = "Material Creation"
    bl_idname = "ARTOKI_PT_create_material"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ArToKi'

    bpy.types.Scene.atk_surface_type = bpy.props.EnumProperty(
        items=[
            ('M', 'M', 'Murs'),
            ('T', 'T', 'Toitures'),
            ('S', 'S', 'Sols')
        ],
        name="Surface type",
        description="Changes the first lettre of material name",
        default="M"
    )

    bpy.types.Scene.atk_surface_nr = bpy.props.EnumProperty(
        items=[
            ('01', '01', '01'),
            ('02', '02', '02'),
            ('03', '03', '03'),
            ('04', '04', '04'),
            ('05', '05', '05'),
            ('06', '06', '06'),
            ('07', '07', '07'),
            ('08', '08', '08'),
            ('09', '09', '09'),
            ('10', '10', '10'),
            ('11', '11', '11'),
            ('12', '12', '12'),
            ('13', '13', '13'),
            ('14', '14', '14'),
            ('15', '15', '15'),
            ('16', '16', '16'),
            ('17', '17', '17'),
            ('18', '18', '18'),
            ('19', '19', '19'),
            ('20', '20', '20')
        ],
        name="Surface type",
        description="Changes the first lettre of material name",
        default="01"
    )

    bpy.types.Scene.atk_mat_name_preset = bpy.props.EnumProperty(
        items=[
            ('', '', ''),
            ('Façade Avant', 'Façade Avant', 'Façade Avant'),
            ('Façade Arrière', 'Façade Arrière', 'Façade Arrière'),
            ('Pignon Droite', 'Pignon Droite', 'Pignon Droite'),
            ('Pignon Gauche', 'Pignon Gauche', 'Pignon Gauche'),
            ('Mur Contre Terre', 'Mur Contre Terre', 'Mur Contre Terre'),
            ('Mur Mitoyen', 'Mur Mitoyen', 'Mur Mitoyen'),
            ('Cloison Cave', 'Cloison Cave', 'Cloison Cave'),
            ('Cloison Grenier', 'Cloison Grenier', 'Cloison Grenier'),
            ('Mur Cave', 'Mur Cave', 'Mur Cave'),
            ('Mur Grenier', 'Mur Grenier', 'Mur Grenier'),
            ('Mur Garage', 'Mur Garage', 'Mur Garage'),
            ('Contremarches', 'Contremarches', 'Contremarches'),
            ('Toiture Avant', 'Toiture Avant', 'Toiture Avant'),
            ('Toiture Arrière', 'Toiture Arrière', 'Toiture Arrière'),
            ('Toiture Droite', 'Toiture Droite', 'Toiture Droite'),
            ('Toiture Gauche', 'Toiture Gauche', 'Toiture Gauche'),
            ('Toiture Chien-Assis Droite', 'Toiture Chien-Assis Droite', 'Toiture Chien-Assis Droite'),
            ('Toiture Chien-Assis Gauche', 'Toiture Chien-Assis Gauche', 'Toiture Chien-Assis Gauche'),
            ('Toiture Plate', 'Toiture Plate', 'Toiture Plate'),
            ('Toiture Annexe', 'Toiture Annexe', 'Toiture Annexe Plate'),
            ('Plancher Grenier', 'Plancher Grenier', 'Plancher Grenier'),
            ('Sol sur terre plein', 'Sol sur terre plein', 'Sol sur terre plein'),
            ('Marches Escalier', 'Marches Escalier', 'Marches Escalier'),
            ('Sol sur Garage', 'Sol sur Garage', 'Sol sur Garage'),
            ('Sol sur Cave', 'Sol sur Cave', 'Sol sur Vave')
        ],
        name="Surface type",
        description="Changes the first lettre of material name",
        default=""
    )

    bpy.types.Scene.atk_mat_name = bpy.props.StringProperty(name="Material name", description="Nom", default="")

    def draw(self, context):
        layout = self.layout
        scene = bpy.context.scene
        obj = context.object

        row = layout.row()
        row.label(text="Change material name:")
        row = layout.row()
        row = layout.row(align=True)
        sub = row.row()

        sub.prop(scene, 'atk_surface_type', text="")
        sub.prop(scene, 'atk_surface_nr', text="")

        sub.scale_x = 2.0
        sub.prop(scene, 'atk_mat_name_preset', text="")
        sub.prop(scene, 'atk_mat_name', text="")
        row = layout.row()

        layout.operator("artoki.create_material")


class ARTOKI_OT_add_basic(bpy.types.Operator):
    bl_label = "Create Material"
    bl_idname = "artoki.create_material"

    def execute(self, context):
        scene = bpy.context.scene

        Material_Name = ""
        Material_Name = Material_Name + str(scene.atk_surface_type + "-" + scene.atk_surface_nr + " ")
        if scene.atk_mat_name_preset != "":
            Material_Name = Material_Name + str(scene.atk_mat_name_preset)
        else:
            if scene.atk_mat_name != "":
                Material_Name = Material_Name + str(scene.atk_mat_name)

        material_basic = bpy.data.materials.new(name=Material_Name)

        col = mathutils.Color()
        col.hsv = (round(random.uniform(0, 1), 3)), 1, (round(random.uniform(0, 1), 3))
        material_basic.diffuse_color = col[0], col[1], col[2], 1

        bpy.ops.object.material_slot_add()
        bpy.context.object.active_material = material_basic
        bpy.ops.object.material_slot_assign()
        scene.atk_surface_nr = str(int(scene.atk_surface_nr) + 1).zfill(2)

        return {'FINISHED'}
