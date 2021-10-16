import bpy


class OBJECT_OT_OpenPreferences(bpy.types.Operator):
    bl_idname = "object.open_preferences"
    bl_label = "Open preferences"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        area = bpy.context.window_manager.windows[-1].screen.areas[0]
        area.type = 'PREFERENCES'
        bpy.context.preferences.active_section = "ADDONS"
        bpy.context.window_manager.addon_search = "ArToKi"
        return {'FINISHED'}
