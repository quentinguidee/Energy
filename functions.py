import datetime
import os
import bpy

from xml.etree.ElementTree import ElementTree, SubElement

from . import info

from .energyreport.classes.color import Color
from .classes.face_type import FaceType


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


def create_xml_file(filepath):
    print("running write_some_data...")
    import shutil
    temp_file = get_path('artoki_peb_temp.xml')
    shutil.copyfile(temp_file, filepath)
    return {'FINISHED'}


def create_html_file(filepath):
    print("running write_some_data...")
    import shutil
    temp_file = get_path('artoki_peb_html_temp.html')
    base_html_folder = get_path('html_files')
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
        bpy.context.scene.render.filepath = os.path.split(filepath)[0] + '/html_files/axono_' + str(vue_nb) + '.jpg'
        bpy.context.scene.camera = j
        bpy.ops.render.opengl(write_still=True)

    # print(cameras_in_scene)
    print('Trying to start Firefox')
    # windows os.startfile(filepath)
    # TODO: Re-enable this line
    # subprocess.call(('xdg-open', filepath))

    return {'FINISHED'}


def get_path(file_name: str):
    return os.path.expanduser('~') + info.INSTALL_PATH + '/' + file_name


def generate_file(tree, file):
    tree.write(file, encoding="UTF-8")


def handle_html(building):
    scene = bpy.context.scene
    date = datetime.datetime.now()

    base_file = get_path('artoki_peb_html_BASE.html')
    temp_file = get_path('artoki_peb_html_temp.html')
    tree = ElementTree(file=base_file)

    values = [
        # (html class, value)
        ("header_left", scene.atk_procedure_type),
        ("header_street", scene.atk_address1),
        ("header_city", scene.atk_address2),
        ("aud1", info.DOCUMENT_AUTHOR),
        ("aud2", info.DOCUMENT_TITLE),
        ("aud3", info.DOCUMENT_ADDRESS_1),
        ("aud4", info.DOCUMENT_ADDRESS_2),
        ("aud5", info.DOCUMENT_EMAIL),
        ("aud7", info.DOCUMENT_PHONE),
        ("aud8", info.DOCUMENT_GSM),
        ("date", date.strftime("%d/%m/%Y")),
    ]

    for value in values:
        for material_slot in tree.findall(".//td[@class='" + value[0] + "']"):
            material_slot.text = str(value[1])

    html_materials = [
        tree.find(".//table[@id='Table_Walls']"),
        tree.find(".//table[@id='Table_Floors']"),
        tree.find(".//table[@id='Table_Roofs']"),
    ]

    for material_slot in bpy.context.object.material_slots:
        xml_surf_mat = 0

        for face in building.faces:
            if material_slot.name[0:4] == face.material:
                xml_surf_mat += face.area

        face_type = FaceType.get_face_type(material_slot.name[0])
        color = Color.from_8_bits_color(material_slot.material.diffuse_color)

        tr = SubElement(html_materials[face_type.get_id()][1], 'tr', id=material_slot.name[0:4])
        td_1 = SubElement(tr, 'td')
        td_1.attrib["class"] = "mat_color"
        td_1.attrib["style"] = "color:" + str(color)
        td_1.text = "\u25A0"
        td_2 = SubElement(tr, 'td')
        td_2.attrib["class"] = "mat_index"
        td_2.text = material_slot.name[0:4]
        td_3 = SubElement(tr, 'td')
        td_3.attrib["class"] = "mat_name"
        td_3.text = material_slot.name[5:]
        td_4 = SubElement(tr, 'td')
        td_4.attrib["class"] = "mat_surf"
        td_4.text = str(round(xml_surf_mat, 2)) + " m²"

    html_volume = tree.find(".//td[@id='general_volume']")
    html_volume.text = "Volume total: " + str(round(building.eval_volume(), 2)) + " m³"
    html_surf_tot = tree.find(".//td[@id='general_surface']")
    html_surf_tot.text = "Surface totale: " + str(round(building.eval_area(), 2)) + " m²"

    projections = [
        tree.find(".//table[@id='walls_values']"),
        tree.find(".//table[@id='floors_projection']"),
        tree.find(".//table[@id='roofs_projection']"),
    ]

    return projections, tree, temp_file


def handle_xml(building):
    scene = bpy.context.scene
    date = datetime.datetime.now()

    base_file = get_path('artoki_peb_BASE.xml')
    temp_file = get_path('artoki_peb_temp.xml')
    tree = ElementTree(file=base_file)

    root = tree.getroot()
    root.attrib['Version'] = info.VERSION

    project = tree.find('Project')
    project.attrib['Name'] = bpy.context.scene.name
    project.attrib['Date'] = date.strftime("%Y-%m-%d %H:%M")

    address1 = tree.find('Project/Address1')
    address1.text = str(scene.atk_address1)
    address2 = tree.find('Project/Address2')
    address2.text = str(scene.atk_address2)

    materials = [
        tree.find('Project/Walls'),
        tree.find('Project/Floors'),
        tree.find('Project/Roofs'),
    ]

    xml_volume = tree.find('Project/Volume')
    xml_volume.text = str(round(building.eval_volume(), 2))
    xml_area = tree.find('Project/Surf_tot')
    xml_area.text = str(round(building.eval_area(), 2))

    projections = [
        tree.find('Project/WallProjections'),
        tree.find('Project/FloorProjections'),
        tree.find('Project/RoofProjections'),
    ]

    tree.write(temp_file, encoding="UTF-8")

    return projections, tree, temp_file
