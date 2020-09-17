import os

import bpy


def face_projection_area(face, obj):
    """
    Calculate the z projected surface of a face
    """
    area = 0.0
    transform_matrix = obj.matrix_world

    vertices_count = len(face.vertices)
    vertices = []

    for i in range(vertices_count):
        vertex_id = face.vertices[i]
        vertex = obj.data.vertices[vertex_id]
        transformed_vertex = transform_matrix @ vertex.co
        transformed_vertex[2] = 0
        vertices.append(transformed_vertex)

    if vertices_count == 4:
        vector0 = vertices[1] - vertices[0]
        vector1 = vertices[3] - vertices[0]

        n = vector0.cross(vector1)

        area = n.length / 2.0

        vector0 = vertices[3] - vertices[2]
        vector1 = vertices[1] - vertices[2]

        n = vector0.cross(vector1)

        area += n.length / 2.0

    elif vertices_count == 3:
        vector0 = vertices[2] - vertices[1]
        vector1 = vertices[0] - vertices[1]

        n = vector0.cross(vector1)

        area = n.length / 2.0

    return area


def create_xml_file(context, filepath):
    print("running write_some_data...")
    import shutil
    temp_file = os.path.expanduser('~/') + '/.blender/ArToKi/artoki_peb_temp.xml'
    shutil.copyfile(temp_file, filepath)
    return {'FINISHED'}


def create_html_file(context, filepath):
    print("running write_some_data...")
    import shutil
    temp_file = os.path.expanduser('~/') + '/.blender/ArToKi/artoki_peb_html_temp.html'
    base_html_folder = os.path.expanduser('~/') + '/.blender/ArToKi/html_files'
    shutil.copyfile(temp_file, filepath)
    print(os.path.split(filepath)[0])

    if os.path.isdir(os.path.split(filepath)[0] + '/html_files'):
        shutil.rmtree(os.path.split(filepath)[0] + '/html_files')

    shutil.copytree(base_html_folder, os.path.split(filepath)[0] + '/html_files')

    shutil.copy2(bpy.context.scene.atk_aerial, os.path.split(filepath)[0] + '/html_files/aerial.jpg')
    shutil.copy2(bpy.context.scene.atk_elevation, os.path.split(filepath)[0] + '/html_files/elevation.jpg')

    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    bpy.context.scene.render.resolution_x = 1024
    bpy.context.scene.render.resolution_y = 768

    # TODO: Re-enable this line
    # bpy.context.scene.render.alpha_mode = 'TRANSPARENT'

    cameras_in_scene = []
    for i in bpy.context.scene.objects:

        if i.type == 'CAMERA':
            cameras_in_scene.append(i)
    vue_nb = 0
    for j in cameras_in_scene:
        vue_nb = vue_nb + 1
        # TODO
        # bpy.context.scene.render.filepath = os.path.split(filepath)[0] + '\\html_files\\axono_' + str(vue_nb) + '.jpg'
        bpy.context.scene.render.filepath = os.path.split(filepath)[0] + '/html_files/axono_' + str(vue_nb) + '.jpg'
        bpy.context.scene.camera = j
        bpy.ops.render.opengl(write_still=True)
    # print(cameras_in_scene)
    print('Trying to start Firefox')
    # windows os.startfile(filepath)
    # TODO: Re-enable this line
    # subprocess.call(('xdg-open', filepath))

    return {'FINISHED'}
