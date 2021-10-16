import bpy
import mathutils
import random

from bpy.types import Operator


class ARTOKI_OT_create_material(Operator):
    bl_label = "Create Material"
    bl_idname = "artoki.create_material"

    def execute(self, context):
        scene = bpy.context.scene

        material_name = str(scene.atk_surface_type + "-" + scene.atk_surface_nr + " ")
        if scene.atk_mat_name_preset != "":
            material_name += str(scene.atk_mat_name_preset)
        elif scene.atk_mat_name != "":
            material_name += str(scene.atk_mat_name)

        material_basic = bpy.data.materials.new(name=material_name)

        col = mathutils.Color()
        col.hsv = (round(random.uniform(0, 1), 3)), 1, (round(random.uniform(0, 1), 3))
        material_basic.diffuse_color = col[0], col[1], col[2], 1

        bpy.ops.object.material_slot_add()
        bpy.context.object.active_material = material_basic
        bpy.ops.object.material_slot_assign()
        scene.atk_surface_nr = str(int(scene.atk_surface_nr) + 1).zfill(2)

        return {'FINISHED'}
