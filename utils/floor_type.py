from .element_type import ElementType
from .face_type import FaceType


class FloorType(ElementType):
    def __init__(self, label: str, description: str):
        super(FloorType, self).__init__(
            face_type=FaceType.FLOOR,
            label=label,
            description=description,
            environment='GROUND',
            subtype=''
        )
