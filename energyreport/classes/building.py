import math

import bmesh
import bpy

from typing import List

from ...functions import face_projection_area

from .face import Face
from .models.element_type import ElementType
from .models.element_type_factory import ElementTypeFactory
from ...utils.face_type import FaceType
from .orientation import Orientation


class Building:
    def populate_faces(self, obj):
        for a in obj.data.polygons:
            angle_proj = round(math.degrees(math.atan2(a.normal[0], a.normal[1])))
            angle_proj_orientation = Orientation.get_direction(angle_proj)
            material_id = obj.material_slots[a.material_index].name[0:1]

            if round(math.atan2(a.normal[1], a.normal[2]), 3) == 0:
                angle_roof = math.atan2(a.normal[0], a.normal[2])
            else:
                hypotenuse = math.sqrt(math.pow(a.normal[0], 2) + math.pow(a.normal[1], 2))
                angle_roof = math.atan2(hypotenuse, a.normal[2])

            face = Face(
                index=a.index,
                area=a.area,
                orientation=angle_proj_orientation,
                material=bpy.context.object.material_slots[a.material_index].name[0:4],
                type=FaceType.get_face_type(material_id),
                angle=angle_roof,
                projection_area=face_projection_area(a, obj),
                material_name=bpy.context.object.material_slots[a.material_index].name[5:],
            )

            self.faces.append(face)

    def __init__(self, obj):
        self.obj = obj
        self.faces: List[Face] = []
        self.populate_faces(obj)
        self.element_types: List[ElementType] = []
        self.populate_element_types()

    def populate_element_types(self):
        for material in bpy.context.object.material_slots:
            face_type = FaceType.get_face_type(material.name[0])
            element_type = ElementTypeFactory.serialize(face_type, material.name[0:4], material.name[5:])
            self.element_types.append(element_type)

    def get_faces(self, face_type: FaceType) -> List[Face]:
        return [face for face in self.faces if face.type == face_type]

    def eval_volume(self):
        """
        Calculate the volume of the mesh object.
        """
        if self.obj and self.obj.type == 'MESH' and self.obj.data:
            # New volume method for bmesh 2015 corrected 2017
            bm = bmesh.new()
            # could also use from_mesh() if you don't care about deformation etc.
            bm.from_object(self.obj, bpy.context.evaluated_depsgraph_get())
            bmesh.ops.triangulate(bm, faces=bm.faces)
            return math.fabs(bm.calc_volume())

    def eval_area(self):
        """
        Calculate the area of the mesh object.
        """
        return sum([face.area for face in self.faces])
