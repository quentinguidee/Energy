# ArToKi-Energy.py (c) 2015 Thierry Maes (tmaes)

import os
import subprocess

import bmesh
import bpy

from .classes.energy_report import EnergyReport
from .classes.energy_deperditions import EnergyDeperditions
from .classes.export_ot_html import ExportOTHTML
from .classes.export_ot_xml import ExportOTXML


def face_projection_area(face, obj):
    """
    Calculate the z projected surface of a face
    :param face: TODO
    :param obj: TODO
    :return: TODO
    """
    area = 0.0
    mat = obj.matrix_world

    vertices_count = len(face.vertices)
    if vertices_count == 4:
        # Quad
        # Get vertex indices
        v1, v2, v3, v4 = face.vertices

        # Get vertex data
        v1 = obj.data.vertices[v1]
        v2 = obj.data.vertices[v2]
        v3 = obj.data.vertices[v3]
        v4 = obj.data.vertices[v4]

        # Apply transform matrix to vertex coordinates.
        v1 = mat * v1.co
        v2 = mat * v2.co
        v3 = mat * v3.co
        v4 = mat * v4.co

        v1[2] = 0
        v2[2] = 0
        v3[2] = 0
        v4[2] = 0

        vec1 = v2 - v1
        vec2 = v4 - v1

        n = vec1.cross(vec2)

        area = n.length / 2.0

        vec1 = v4 - v3
        vec2 = v2 - v3

        n = vec1.cross(vec2)

        area += n.length / 2.0

    elif vertices_count == 3:
        # Triangle
        # Get vertex indices
        v1, v2, v3 = face.vertices

        # Get vertex data
        v1 = obj.data.vertices[v1]
        v2 = obj.data.vertices[v2]
        v3 = obj.data.vertices[v3]

        # Apply transform matrix to vertex coordinates.
        v1 = mat * v1.co
        v2 = mat * v2.co
        v3 = mat * v3.co

        v1[2] = 0
        v2[2] = 0
        v3[2] = 0

        vec1 = v3 - v2
        vec2 = v1 - v2

        n = vec1.cross(vec2)

        area = n.length / 2.0

    return area


# Calculate the volume of a mesh object.
def object_volume(obj):
    if obj and obj.type == 'MESH' and obj.data:
        # New volume method for bmesh 2015 corrected 2017

        bm = bmesh.new()
        bm.from_object(obj, bpy.context.scene)  # could also use from_mesh() if you don't care about deformation etc.
        bmesh.ops.triangulate(bm, faces=bm.faces)
        # print(bm.calc_volume())
        return bm.calc_volume()


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
    bpy.context.scene.render.alpha_mode = 'TRANSPARENT'

    cameras_in_scene = []
    for i in bpy.context.scene.objects:

        if i.type == 'CAMERA':
            cameras_in_scene.append(i)
    vue_nb = 0
    for j in cameras_in_scene:
        vue_nb = vue_nb + 1
        bpy.context.scene.render.filepath = os.path.split(filepath)[0] + '\\html_files\\axono_' + str(vue_nb) + '.jpg'
        bpy.context.scene.camera = j
        bpy.ops.render.opengl(write_still=True)
    # print(cameras_in_scene)
    print('Trying to start Firefox')
    # windows os.startfile(filepath)
    subprocess.call(('xdg-open', filepath))

    return {'FINISHED'}


# registering and menu integration
def register():
    bpy.utils.register_class(EnergyReport)
    bpy.utils.register_class(EnergyDeperditions)
    bpy.utils.register_class(ExportOTXML)
    bpy.utils.register_class(ExportOTHTML)


# unregistering and removing menus
def unregister():
    bpy.utils.unregister_class(EnergyReport)
    bpy.utils.unregister_class(EnergyDeperditions)
    bpy.utils.unregister_class(ExportOTXML)
    bpy.utils.unregister_class(ExportOTHTML)


if __name__ == "__main__":
    register()
