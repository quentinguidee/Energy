from .element_type import ElementType

from .floor_type import FloorType
from .wall_type import WallType
from .roof_type import RoofType
from .face_type import FaceType


class ElementTypeFactory:
    @staticmethod
    def serialize(face_type: FaceType, label: str, description: str) -> ElementType:
        if face_type == FaceType.WALL:
            return WallType(label, description)
        elif face_type == FaceType.FLOOR:
            return FloorType(label, description)
        elif face_type == FaceType.ROOF:
            return RoofType(label, description)
