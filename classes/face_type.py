from enum import Enum


class FaceType(Enum):
    WALL = (0, 'Walls', 'MOD_BUILD', ['M', 'W'], 'wall')
    FLOOR = (1, 'Floors', 'TEXTURE', ['S', 'F'], 'floor')
    ROOF = (2, 'Roofs', 'LINCURVE', ['T', 'R'], 'roof')

    def get_id(self):
        return self.value[0]

    def get_name(self):
        return self.value[1]

    def get_icon(self):
        return self.value[2]

    def get_letters(self):
        return self.value[3]

    def get_pacetools_id(self):
        return self.value[4]

    @staticmethod
    def get_face_type(letter: str) -> 'FaceType':
        for face_type in FaceType:
            if letter in face_type.get_letters():
                return face_type
