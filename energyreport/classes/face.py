from .orientation import Orientation
from ...classes.face_type import FaceType


class Face:
    index: int
    area: float
    orientation: Orientation
    material: str  # ex: M-01
    type: FaceType
    angle: float
    projection_area: float
    material_name: str

    def __init__(self, index: int, area: float, orientation: Orientation, material: str, face_type: FaceType,
                 angle: float, projection_area: float, material_name: str):
        self.index = index
        self.area = area
        self.orientation = orientation
        self.material = material
        self.type = face_type
        self.angle = angle
        self.projection_area = projection_area
        self.material_name = material_name
