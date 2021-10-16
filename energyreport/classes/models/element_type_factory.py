from .element_type import ElementType

from ...classes.models.floor_type import FloorType
from ...classes.models.wall_type import WallType
from ...classes.models.roof_type import RoofType
from ....utils.face_type import FaceType


class ElementTypeFactory:
    @staticmethod
    def serialize(face_type: FaceType, label: str, description: str) -> ElementType:
        if face_type == FaceType.WALL:
            return WallType(label, description)
        elif face_type == FaceType.FLOOR:
            return FloorType(label, description)
        elif face_type == FaceType.ROOF:
            return RoofType(label, description)
