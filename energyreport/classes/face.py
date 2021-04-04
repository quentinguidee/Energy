from dataclasses import dataclass

from .orientation import Orientation
from ...classes.face_type import FaceType


@dataclass
class Face:
    index: int
    area: float
    orientation: Orientation
    material: str
    type: FaceType
    angle: float
    projection_area: float
    material_name: str
