import datetime
import math
import os
from xml.etree.ElementTree import SubElement, ElementTree

from ..functions import face_projection_area, object_volume
from .. import info

import bpy


class OBJECT_PT_ArToKi_EnergyReport(bpy.types.Panel):
    bl_label = "ArToKi - Energy - Report"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    bpy.types.Scene.atk_aerial = bpy.props.StringProperty(name="Aerial", description="Aerial view path", default="",
                                                          subtype='FILE_PATH')
    bpy.types.Scene.atk_elevation = bpy.props.StringProperty(name="Elevation", description="Elevation view path",
                                                             default="", subtype='FILE_PATH')
    bpy.types.Scene.atk_address1 = bpy.props.StringProperty(name="Address 1", description="Street, nb", default="")
    bpy.types.Scene.atk_address2 = bpy.props.StringProperty(name="Address 2", description="PostCode City", default="")
    bpy.types.Scene.atk_therm_col = bpy.props.BoolProperty(name="Therm col",
                                                           description="Assign materials colors by performance",
                                                           default=0)
    bpy.types.Scene.atk_procedure_type = bpy.props.EnumProperty(
        items=[('PAE', 'PAE', 'Procédure d\'audit énergétique'),
               ('PEB', 'PEB', 'Performances énergétiques des batiments')],
        name="Procedure type",
        description="Changes the upper left text logo",
        default="PEB"
    )
    def draw(self, context):

        author = 'Maes Thierry'
        author_titles = 'Auditeur PAE, Certificateur PEB'
        author_adress_1 = 'Rue Joseph Berger, 6'
        author_adress_2 = 'B-1470 Genappe'
        author_e_mail = 'info@tmaes.be'
        author_phone = '+32 (0)67/ 63 68 50'
        author_gsm = '+32 (0)475/ 30 36 51'

        # préparation du fichier xml et html temporaires
        obj = context.object
        scene = bpy.context.scene
        now = datetime.datetime.now()
        base_file = os.path.expanduser('~') + '/.blender/ArToKi/artoki_peb_BASE.xml'
        temp_file = os.path.expanduser('~') + '/.blender/ArToKi/artoki_peb_temp.xml'
        tree = ElementTree(file=base_file)
        base_file_html = os.path.expanduser('~') + '/.blender/ArToKi/artoki_peb_html_BASE.html'
        temp_file_html = os.path.expanduser('~') + '/.blender/ArToKi/artoki_peb_html_temp.html'
        tree_html = ElementTree(file=base_file_html)
        # Bases du fichier xml et html
        root = tree.getroot()
        root_html = tree_html.getroot()
        root.attrib['Version'] = info.VERSION
        project = tree.find('Project')
        project.attrib['Name'] = bpy.context.scene.name
        project.attrib['Date'] = now.strftime("%Y-%m-%d %H:%M")
        address1 = tree.find('Project/Address1')
        address1.text = str(scene.atk_address1)
        address2 = tree.find('Project/Address2')
        address2.text = str(scene.atk_address2)

        # placement des éléments statiques du html coordonnées, date etc... header_left
        for i in tree_html.findall(".//td[@class='header_left']"):
            i.text = str(scene.atk_procedure_type)
        for i in tree_html.findall(".//td[@class='header_street']"):
            i.text = str(scene.atk_address1)
        for i in tree_html.findall(".//td[@class='header_city']"):
            i.text = str(scene.atk_address2)
        for i in tree_html.findall(".//td[@class='aud1']"):
            i.text = str(author)
        for i in tree_html.findall(".//td[@class='aud2']"):
            i.text = str(author_titles)
        for i in tree_html.findall(".//td[@class='aud3']"):
            i.text = str(author_adress_1)
        for i in tree_html.findall(".//td[@class='aud4']"):
            i.text = str(author_adress_2)
        for i in tree_html.findall(".//td[@class='aud5']"):
            i.text = str(author_e_mail)
        for i in tree_html.findall(".//td[@class='aud7']"):
            i.text = str(author_phone)
        for i in tree_html.findall(".//td[@class='aud8']"):
            i.text = str(author_gsm)
        for i in tree_html.findall(".//td[@class='date']"):
            i.text = now.strftime("%d/%m/%Y")

        layout = self.layout

        # début de la table, titres et tout et tout
        # préparation des sélections avec des listes
        faces_base = [face for face in bpy.context.object.data.polygons]
        faces_walls = []
        faces_floors = []
        faces_roofs = []
        faces_temp = []
        faces_types = ['WALLS', 'FLOORS', 'ROOFS']
        PROJECTIONS = ['S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE',
                       'SSE']
        FACES = []

        ### 1 Création d'une liste contenant: index, surface, orientation, matériau, type de la face, angle, surface projetée et nom du matériau

        for a in obj.data.polygons:
            properties = []
            properties.append(a.index)
            properties.append(a.area)
            angle_proj = round(math.degrees(math.atan2(a.normal[0], a.normal[1])))
            angle_proj_name = ''  # pourrait etre ameliore par une fonction

            if angle_proj >= -191.25 and angle_proj < -168.75:
                angle_proj_name = 'S'

            if angle_proj >= -168.75 and angle_proj < -146.25:
                angle_proj_name = 'SSW'

            if angle_proj >= -146.25 and angle_proj < -123.75:
                angle_proj_name = 'SW'

            if angle_proj >= -123.75 and angle_proj < -101.25:
                angle_proj_name = 'WSW'

            if angle_proj >= -101.25 and angle_proj < -78.75:
                angle_proj_name = 'W'

            if angle_proj >= -78.75 and angle_proj < -56.25:
                angle_proj_name = 'WNW'

            if angle_proj >= -56.25 and angle_proj < -33.75:
                angle_proj_name = 'NW'

            if angle_proj >= -33.75 and angle_proj < -11.25:
                angle_proj_name = 'NNW'

            if angle_proj >= -11.25 and angle_proj < 11.25:
                angle_proj_name = 'N'

            if angle_proj >= 11.25 and angle_proj < 33.75:
                angle_proj_name = 'NNE'

            if angle_proj > 33.75 and angle_proj < 56.25:
                angle_proj_name = 'NE'

            if angle_proj >= 56.25 and angle_proj < 78.75:
                angle_proj_name = 'ENE'

            if angle_proj >= 78.75 and angle_proj < 101.25:
                angle_proj_name = 'E'

            if angle_proj >= 101.25 and angle_proj < 123.75:
                angle_proj_name = 'ESE'

            if angle_proj >= 123.75 and angle_proj < 146.25:
                angle_proj_name = 'SE'

            if angle_proj >= 146.25 and angle_proj < 168.75:
                angle_proj_name = 'SSE'

            if angle_proj >= 168.75 and angle_proj < 191.25:
                angle_proj_name = 'S'

            properties.append(angle_proj_name)
            properties.append(bpy.context.object.material_slots[a.material_index].name[0:4])

            if context.object.material_slots[a.material_index].name[0:1] == 'M' or context.object.material_slots[
                                                                                       a.material_index].name[
                                                                                   0:1] == 'W':
                properties.append(faces_types[0])
            elif context.object.material_slots[a.material_index].name[0:1] == 'S' or context.object.material_slots[
                                                                                         a.material_index].name[
                                                                                     0:1] == 'F':
                properties.append(faces_types[1])
            elif context.object.material_slots[a.material_index].name[0:1] == 'T' or context.object.material_slots[
                                                                                         a.material_index].name[
                                                                                     0:1] == 'R':
                properties.append(faces_types[2])
            if round(math.atan2(a.normal[1], a.normal[2]), 3) == 0:
                angle_roof = math.atan2(a.normal[0], a.normal[2])
            else:
                hypoth = math.sqrt(math.pow(a.normal[0], 2) + math.pow(a.normal[1], 2))
                angle_roof = math.atan2(hypoth, a.normal[2])
            properties.append(angle_roof)
            properties.append(face_projection_area(a, obj))
            properties.append(bpy.context.object.material_slots[a.material_index].name[5:])
            FACES.append(properties)

        ### 1.1 LISTE DES MURS SOLS TOITS POUR L'EXPORT XML

        xml_walls_materials = tree.find('Project/Walls')
        html_walls_materials = tree_html.find(".//table[@id='Table_Walls']")
        xml_floors_materials = tree.find('Project/Floors')
        html_floors_materials = tree_html.find(".//table[@id='Table_Floors']")
        xml_roofs_materials = tree.find('Project/Roofs')
        html_roofs_materials = tree_html.find(".//table[@id='Table_Roofs']")
        for i in bpy.context.object.material_slots:
            xml_surf_mat = 0

            for j in FACES:
                if i.name[0:4] == j[3]:
                    xml_surf_mat = xml_surf_mat + j[1]

            if i.name[0] == 'M' or i.name[0] == 'W':
                wall = SubElement(xml_walls_materials, 'Wall', Id=i.name[0:4], Name=i.name[5:],
                                  Surf=str(round(xml_surf_mat, 2)))
                tr = SubElement(html_walls_materials[1], 'tr', id=i.name[0:4])
                td_1 = SubElement(tr, 'td')
                td_1.attrib["class"] = "mat_color"
                td_1.attrib["style"] = "color:rgb(" + str(int(i.material.diffuse_color[0] * 255)) + "," + str(
                    int(i.material.diffuse_color[1] * 255)) + "," + str(int(i.material.diffuse_color[2] * 255)) + ")"
                td_1.text = "\u25A0"
                td_2 = SubElement(tr, 'td')
                td_2.attrib["class"] = "mat_index"
                td_2.text = i.name[0:4]
                td_3 = SubElement(tr, 'td')
                td_3.attrib["class"] = "mat_name"
                td_3.text = i.name[5:]
                td_4 = SubElement(tr, 'td')
                td_4.attrib["class"] = "mat_surf"
                td_4.text = str(round(xml_surf_mat, 2)) + " m²"

            if i.name[0] == 'S' or i.name[0] == 'F':
                floor = SubElement(xml_floors_materials, 'Floor', Id=i.name[0:4], Name=i.name[5:],
                                   Surf=str(round(xml_surf_mat, 2)))
                tr = SubElement(html_floors_materials[1], 'tr', id=i.name[0:4])
                td_1 = SubElement(tr, 'td')
                td_1.attrib["class"] = "mat_color"
                td_1.attrib["style"] = "color:rgb(" + str(int(i.material.diffuse_color[0] * 255)) + "," + str(
                    int(i.material.diffuse_color[1] * 255)) + "," + str(int(i.material.diffuse_color[2] * 255)) + ")"
                td_1.text = "\u25A0"
                td_2 = SubElement(tr, 'td')
                td_2.attrib["class"] = "mat_index"
                td_2.text = i.name[0:4]
                td_3 = SubElement(tr, 'td')
                td_3.attrib["class"] = "mat_name"
                td_3.text = i.name[5:]
                td_4 = SubElement(tr, 'td')
                td_4.attrib["class"] = "mat_surf"
                td_4.text = str(round(xml_surf_mat, 2)) + " m²"

            if i.name[0] == 'T' or i.name[0] == 'R':
                roof = SubElement(xml_roofs_materials, 'Roof', Id=i.name[0:4], Name=i.name[5:],
                                  Surf=str(round(xml_surf_mat, 2)))
                tr = SubElement(html_roofs_materials[1], 'tr', id=i.name[0:4])
                td_1 = SubElement(tr, 'td')
                td_1.attrib["class"] = "mat_color"
                td_1.attrib["style"] = "color:rgb(" + str(int(i.material.diffuse_color[0] * 255)) + "," + str(
                    int(i.material.diffuse_color[1] * 255)) + "," + str(int(i.material.diffuse_color[2] * 255)) + ")"
                td_1.text = "\u25A0"
                td_2 = SubElement(tr, 'td')
                td_2.attrib["class"] = "mat_index"
                td_2.text = i.name[0:4]
                td_3 = SubElement(tr, 'td')
                td_3.attrib["class"] = "mat_name"
                td_3.text = i.name[5:]
                td_4 = SubElement(tr, 'td')
                td_4.attrib["class"] = "mat_surf"
                td_4.text = str(round(xml_surf_mat, 2)) + " m²"

        ### 2 LISTE DES PROJECTIONS ET DES SURFACES

        row = layout.row()
        row.prop(scene, 'atk_procedure_type', text="Procedure")
        row = layout.row()
        row.prop(scene, 'atk_aerial', text="Aerial view path")
        row = layout.row()
        row.prop(scene, 'atk_elevation', text="Elevation view path")
        row = layout.row()
        row.prop(scene, 'atk_address1', text="Street, Nb")
        row = layout.row()
        row.prop(scene, 'atk_address2', text="PostCode City")
        row = layout.row()
        row.prop(scene, 'atk_therm_col', text="Use thermic colors")
        row = layout.row()
        volume = math.fabs(object_volume(obj))

        # calcul de la surface totale de l'enveloppe

        surf_tot = 0
        for s in FACES:
            surf_tot = surf_tot + s[1]
        row = layout.row()
        row.alignment = 'EXPAND'
        box = row.box()
        col = box.column()
        subrow = col.row(align=True)
        subrow.label(text="Volume of the enveloppe:   " + str(round(volume, 2)) + " m\xb3", icon='VIEW3D')
        subrow.label(text="Surface of the enveloppe:   " + str(round(surf_tot, 2)) + " m\xb2", icon='MESH_GRID')

        xml_volume = tree.find('Project/Volume')
        html_volume = tree_html.find(".//td[@id='general_volume']")

        xml_volume.text = str(round(volume, 2))
        html_volume.text = "Volume total: " + str(round(volume, 2)) + " m³"

        xml_surf_tot = tree.find('Project/Surf_tot')
        html_surf_tot = tree_html.find(".//td[@id='general_surface']")

        xml_surf_tot.text = str(round(surf_tot, 2))
        html_surf_tot.text = "Surface totale: " + str(round(surf_tot, 2)) + " m²"

        ### 2.1 MURS
        xml_wall_projections = tree.find('Project/WallProjections')
        html_wall_projections = tree_html.find(".//table[@id='walls_values']")

        projection_id = 0

        for p in PROJECTIONS:
            faces_proj = []
            mat_proj = []
            surf_proj = 0

            # déterminer les faces de la projection et la surface de la projection
            for g in FACES:
                if g[2] == p and g[4] == faces_types[0]:
                    faces_proj.append(g)
                    surf_proj = surf_proj + g[1]

            if surf_proj != 0:
                row = layout.row()
                row.alignment = 'EXPAND'
                box = row.box()
                col = box.column()
                subrow = col.row(align=True)
                subrow.label(text=p + " Projection          Surface  : " + str(round(surf_proj, 2)) + " m\xb2",
                             icon='CURSOR')
                # on peut refaire le moteur apd ici...
                subrow = col.row(align=True)
                subrow.label(text="" + 75 * "-")
                projection = SubElement(xml_wall_projections, 'WallProjection', Id=str(projection_id),
                                        Orientation=str(p), Surf=str(round(surf_proj, 2)))
                projection_id = projection_id + 1

                for x in faces_proj:
                    if mat_proj.count(str(x[3])) == 0:  # si le matériau de la face n'existe pas encore dans mat_proj
                        mat_proj.append(x[3])  # ajouter le matériau dans mat_proj [@name='a']

                for y in sorted(mat_proj):
                    subrow = col.row(align=True)
                    surf_mat = 0
                    for z in faces_proj:
                        if z[3] == y:
                            surf_mat = surf_mat + z[1]
                    subrow.label(text=5 * ' ' + y + ' : ' + str(round(surf_mat, 2)) + " m\xb2", icon='MOD_BUILD')
                    wallpart = SubElement(projection, 'WallPart', id=str(y), Surf=str(round(surf_mat, 2)))

                if projection_id <= 4:
                    projection_html_1 = SubElement(html_wall_projections[0][1], 'td')
                    projection_html_1_table = SubElement(projection_html_1,
                                                         'table')  # , Orientation=str(p), Surf=str(round(surf_proj,2))
                    projection_html_1_table.attrib["id"] = "walls_projection"
                    tbody = SubElement(projection_html_1_table, 'tbody')
                    caption = SubElement(tbody, 'caption')  # , Orientation=str(p), Surf=str(round(surf_proj,2))
                    caption.text = "Az.: " + str(p) + " - " + str(round(surf_proj, 2)) + " m²"
                    for x in faces_proj:
                        if mat_proj.count(
                                str(x[3])) == 0:  # si le matériau de la face n'existe pas encore dans mat_proj
                            mat_proj.append(x[3])  # ajouter le matériau dans mat_proj [@name='a']
                    for y in sorted(mat_proj):
                        surf_mat = 0
                        for z in faces_proj:
                            if z[3] == y:
                                surf_mat = surf_mat + z[1]
                        tr = SubElement(tbody, 'tr')
                        td_1 = SubElement(tr, 'td')
                        td_1.attrib["class"] = "mat_color"
                        for i in bpy.context.object.material_slots:
                            if i.name[0:4] == y:
                                color = i.material.diffuse_color
                        td_1.attrib["style"] = "color:rgb(" + str(int(color[0] * 255)) + "," + str(
                            int(color[1] * 255)) + "," + str(int(color[2] * 255)) + ")"
                        td_1.text = "\u25A0"
                        td_2 = SubElement(tr, 'td')
                        td_2.attrib["class"] = "mat_index"
                        td_2.text = str(y)
                        td_3 = SubElement(tr, 'td')
                        td_3.attrib["class"] = "mat_surf"
                        td_3.text = str(round(surf_mat, 2)) + " m²"

                if projection_id > 4:
                    projection_html_1 = SubElement(html_wall_projections[0][2], 'td')
                    projection_html_1_table = SubElement(projection_html_1,
                                                         'table')  # , Orientation=str(p), Surf=str(round(surf_proj,2))
                    projection_html_1_table.attrib["id"] = "walls_projection"
                    tbody = SubElement(projection_html_1_table, 'tbody')
                    caption = SubElement(tbody, 'caption')  # , Orientation=str(p), Surf=str(round(surf_proj,2))
                    caption.text = "Az.: " + str(p) + " - " + str(round(surf_proj, 2)) + " m²"
                    for x in faces_proj:
                        if mat_proj.count(
                                str(x[3])) == 0:  # si le matériau de la face n'existe pas encore dans mat_proj
                            mat_proj.append(x[3])  # ajouter le matériau dans mat_proj [@name='a']
                    for y in sorted(mat_proj):
                        surf_mat = 0
                        for z in faces_proj:
                            if z[3] == y:
                                surf_mat = surf_mat + z[1]
                        tr = SubElement(tbody, 'tr')
                        td_1 = SubElement(tr, 'td')
                        td_1.attrib["class"] = "mat_color"
                        for i in bpy.context.object.material_slots:
                            if i.name[0:4] == y:
                                color = i.material.diffuse_color

                        td_1.attrib["style"] = "color:rgb(" + str(int(color[0] * 255)) + "," + str(
                            int(color[1] * 255)) + "," + str(int(color[2] * 255)) + ")"
                        td_1.text = "\u25A0"
                        td_2 = SubElement(tr, 'td')
                        td_2.attrib["class"] = "mat_index"
                        td_2.text = str(y)
                        td_3 = SubElement(tr, 'td')
                        td_3.attrib["class"] = "mat_surf"
                        td_3.text = str(round(surf_mat, 2)) + " m²"

        ### 2.2 SOLS
        xml_floor_projections = tree.find('Project/FloorProjections')
        html_floors_projection = tree_html.find(".//table[@id='floors_projection']")
        row = layout.row()
        row.alignment = 'EXPAND'
        box = row.box()
        col = box.column()
        surf_vert = 0
        faces_vert = []
        mat_vert = []

        for g in FACES:
            if g[4] == faces_types[1]:
                faces_vert.append(g)
                surf_vert = surf_vert + g[6]

        if surf_vert != 0:
            subrow = col.row(align=True)
            subrow.label(text="Floors Projection     Surface : " + str(round(surf_vert, 2)) + " m\xb2", icon="TEXTURE")
            subrow = col.row(align=True)
            subrow.label(text="" + 75 * "-")
            xml_floor_projections.attrib['Surf'] = str(round(surf_vert, 2))  #
            html_floors_projection.attrib['Surf'] = str(round(surf_vert, 2))  #
            caption = tree_html.find(".//table[@id='floors_values']/tbody/caption")
            caption.text = 'Projection Sols: ' + str(round(surf_vert, 2)) + ' m²'

            for x in faces_vert:
                if mat_vert.count(str(x[3])) == 0:
                    mat_vert.append(x[3])

            for y in sorted(mat_vert):
                subrow = col.row(align=True)
                surf_mat_vert = 0
                for z in faces_vert:
                    if z[3] == y:
                        surf_mat_vert = surf_mat_vert + z[6]

                subrow.label(text=5 * ' ' + y + ' : ' + str(round(surf_mat_vert, 2)) + " m\xb2", icon="ASSET_MANAGER")
                floorpart = SubElement(xml_floor_projections, 'FloorPart', Id=str(y), Surf=str(round(surf_mat_vert, 2)))

                tr = SubElement(html_floors_projection[0], 'tr')
                td_1 = SubElement(tr, 'td')
                td_1.attrib["class"] = "mat_color"

                for i in bpy.context.object.material_slots:
                    if i.name[0:4] == y:
                        color = i.material.diffuse_color
                td_1.attrib["style"] = "color:rgb(" + str(int(color[0] * 255)) + "," + str(
                    int(color[1] * 255)) + "," + str(int(color[2] * 255)) + ")"
                td_1.text = "\u25A0"
                td_2 = SubElement(tr, 'td')
                td_2.attrib["class"] = "mat_index"
                td_2.text = str(y)
                td_3 = SubElement(tr, 'td')
                td_3.attrib["class"] = "mat_surf"
                td_3.text = str(round(surf_mat_vert, 2)) + " m²"

        ### 2.3 TOITURE

        xml_roof_projections = tree.find('Project/RoofProjections')
        html_roofs_projection = tree_html.find(".//table[@id='roofs_projection']")
        row = layout.row()
        row.alignment = 'EXPAND'
        box = row.box()
        col = box.column()
        surf_roof = 0
        surf_proj_roof = 0
        faces_roof = []
        mat_roof = []

        for g in FACES:
            if g[4] == faces_types[2]:
                faces_roof.append(g)
                surf_roof = surf_roof + g[1]
                surf_proj_roof = surf_proj_roof + g[6]

        if surf_roof != 0:
            subrow = col.row(align=True)
            subrow.label(text="Roofs Projection     Surface : " + str(round(surf_proj_roof, 2)) + " m\xb2",
                         icon="LINCURVE")
            subrow = col.row(align=True)
            subrow.label(text="" + 75 * "-")
            xml_roof_projections.attrib['Surf'] = str(round(surf_proj_roof, 2))  #
            html_roofs_projection.attrib['Surf'] = str(round(surf_proj_roof, 2))  #
            caption = tree_html.find(".//table[@id='roofs_values']/tbody/caption")
            caption.text = 'Projection Toitures: ' + str(round(surf_proj_roof, 2)) + ' m²'

            for x in faces_roof:
                if mat_roof.count(str(x[3])) == 0:
                    mat_roof.append(x[3])
            for y in sorted(mat_roof):
                subrow = col.row(align=True)
                surf_mat_roof = 0
                surf_proj_mat_roof = 0
                roof_angle = 0
                roof_orientation = ''

                for z in faces_roof:
                    if z[3] == y:
                        surf_mat_roof = surf_mat_roof + z[1]
                        surf_proj_mat_roof = surf_proj_mat_roof + z[6]
                        roof_angle = z[5]
                        roof_orientation = z[2]

                subrow.label(text=y + ' : ' + str(round(surf_mat_roof, 2)) + " m\xb2", icon="MOD_ARRAY")
                subrow.label(text='Proj. : ' + str(roof_orientation))
                subrow.label(text='Angle : ' + str(round(math.fabs(math.degrees(roof_angle)), 1)) + " \xb0")
                subrow.label(text='Proj. surf. : ' + str(round(surf_proj_mat_roof, 2)) + " m\xb2")
                roofpart = SubElement(
                    xml_roof_projections,
                    'RoofPart',
                    Angle=str(round(math.fabs(math.degrees(roof_angle)), 1)),
                    Id=str(y),
                    Orientation=str(roof_orientation),
                    Surf=str(round(surf_mat_roof, 2)),
                    SurfProj=str(round(surf_proj_mat_roof, 2))
                )

                tr = SubElement(html_roofs_projection[0], 'tr')
                td_1 = SubElement(tr, 'td')
                td_1.attrib["class"] = "mat_color"
                for i in bpy.context.object.material_slots:
                    if i.name[0:4] == y:
                        color = i.material.diffuse_color
                td_1.attrib["style"] = "color:rgb(" + str(int(color[0] * 255)) + "," + str(
                    int(color[1] * 255)) + "," + str(int(color[2] * 255)) + ")"
                td_1.text = "\u25A0"
                td_2 = SubElement(tr, 'td')
                td_2.attrib["class"] = "mat_index"
                td_2.text = str(y)
                td_3 = SubElement(tr, 'td')
                td_3.attrib["class"] = "mat_surf_brute"
                td_3.text = str(round(surf_mat_roof, 2)) + " m²"
                td_4 = SubElement(tr, 'td')
                td_4.attrib["class"] = "mat_angle"
                td_4.text = str(round(math.fabs(math.degrees(roof_angle)), 1)) + " °"
                td_5 = SubElement(tr, 'td')
                td_5.attrib["class"] = "mat_orient"
                td_5.text = str(roof_orientation)
                td_6 = SubElement(tr, 'td')
                td_6.attrib["class"] = "mat_surf_proj"
                td_6.text = str(round(surf_proj_mat_roof, 2)) + " m²"

        tree.write(temp_file, encoding="UTF-8")
        tree_html.write(temp_file_html, encoding="UTF-8")

        # Resume surfaces par materiau
        row = layout.row()
        row.alignment = 'EXPAND'
        box = row.box()
        col = box.column()
        subrow = col.row(align=True)
        subrow.label(text="Walls", icon="MOD_BUILD")
        for i in bpy.context.object.material_slots:
            xml_surf_mat = 0

            for j in FACES:
                if i.name[0:4] == j[3]:
                    xml_surf_mat = xml_surf_mat + j[1]

            if i.name[0] == 'M' or i.name[0] == 'W':
                subrow = col.row(align=True)
                subrow.label(text=i.name[0:4] + "  " + i.name[5:] + " : ")
                subrow.label(text=str(round(xml_surf_mat, 2)) + " m\xb2")

        col = box.column()
        subrow = col.row(align=True)
        col.label(text="Floors", icon="TEXTURE")
        for i in bpy.context.object.material_slots:
            xml_surf_mat = 0

            for j in FACES:
                if i.name[0:4] == j[3]:
                    xml_surf_mat = xml_surf_mat + j[1]

            if i.name[0] == 'S' or i.name[0] == 'F':
                subrow = col.row(align=True)
                subrow.label(text=i.name[0:4] + "  " + i.name[5:] + " : ")
                subrow.label(text=str(round(xml_surf_mat, 2)) + " m\xb2")

        col = box.column()
        subrow = col.row(align=True)
        col.label(text="Roofs", icon="LINCURVE")
        for i in bpy.context.object.material_slots:
            xml_surf_mat = 0

            for j in FACES:
                if i.name[0:4] == j[3]:
                    xml_surf_mat = xml_surf_mat + j[1]

            if i.name[0] == 'T' or i.name[0] == 'R':
                subrow = col.row(align=True)
                subrow.label(text=i.name[0:4] + "  " + i.name[5:] + " : ")
                subrow.label(text=str(round(xml_surf_mat, 2)) + " m\xb2")

        # buttons & credits

        row = layout.row()
        row.operator("export.xml", text="Save")
        row.operator("export.html", text="Export to pdf...")

        row = layout.row()
        dirname = os.path.expanduser(
            '~') + '\.blender\ArToKi\labels'  #### Only line to change for lite version for windows

        if bpy.data.images.find('ArToKi.png') == -1:
            img_A_Plus = bpy.data.images.load(os.path.join(dirname, 'ArToKi.png'))
            # TODO: Uncomment use_alpha, if useful.
            # img_A_Plus.use_alpha = True
            img_A_Plus.user_clear()  # Won't get saved into .blend files
        icon_ArToKi = self.layout.icon(bpy.data.images['ArToKi.png'])
        row.label(text="ArToKi - Energy by tmaes" + 60 * " " + "info@tmaes.be", icon_value=icon_ArToKi)

