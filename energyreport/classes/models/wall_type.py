from .element_type import ElementType

from ....classes.face_type import FaceType


class WallType(ElementType):
    def __init__(self, label: str, description: str):
        super(WallType, self).__init__(
            face_type=FaceType.WALL,
            label=label,
            description=description,
            environment='OPEN_AIR',
            subtype='FULL'
        )
