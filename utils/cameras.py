import bpy


def get_all_cameras():
    return [obj for obj in bpy.context.scene.objects if obj.type == 'CAMERA']


def render(camera, filepath: str):
    # TODO: Re-enable this line
    # bpy.context.scene.render.alpha_mode = 'TRANSPARENT'

    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    bpy.context.scene.render.resolution_x = 1024
    bpy.context.scene.render.resolution_y = 768
    bpy.context.scene.render.filepath = filepath
    bpy.context.scene.camera = camera
    bpy.ops.render.opengl(write_still=True)
