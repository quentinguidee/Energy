from .element_type import ElementType

from ....utils.face_type import FaceType


class RoofType(ElementType):
    def __init__(self, label: str, description: str):
        super(RoofType, self).__init__(
            face_type=FaceType.ROOF,
            label=label,
            description=description,
            environment='OPEN_AIR',
            subtype='INCLINED'
        )
