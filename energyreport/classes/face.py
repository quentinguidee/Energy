from .orientation import Orientation
from ...classes.face_type import FaceType


class Face:
    def __init__(self, index: int, area: float, orientation: Orientation, material: str, face_type: FaceType,
                 angle: float, projection_area: float, material_name: str):
        self.index: int = index
        self.area: float = area
        self.orientation: Orientation = orientation
        self.material: str = material
        self.type: FaceType = face_type
        self.angle: float = angle
        self.projection_area: float = projection_area
        self.material_name: str = material_name
