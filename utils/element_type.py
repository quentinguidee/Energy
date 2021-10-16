from .face_type import FaceType


class ElementType:
    def __init__(self, face_type: FaceType, label: str, description: str, environment: str, subtype: str):
        self.face_type: FaceType = face_type
        self.label: str = label
        self.description: str = description
        self.environment: str = environment
        self.subtype: str = subtype

    def get_pacetools_type(self) -> str:
        return self.face_type.get_pacetools_type()
