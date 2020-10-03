from enum import Enum


class MaterialType(Enum):
    FREE_AIR = ('Free air', 0)
    SEMI_STATIC_AIR = ('Semi Static air', 1)
    STATIC_AIR = ('Static air', 2)
    MASONRY = ('Masonry', 3)
    WOOD = ('Wood', 4)
    INSULATION = ('Insulation', 5)

    def get_name(self) -> str:
        return self.value[0]

    def get_id(self) -> int:
        return self.value[1]

    def as_blender_tuple(self):
        name = self.get_name()
        return name, name, name, self.get_id()

    @staticmethod
    def as_blender_enum():
        blender_enum = []
        for material in MaterialType:
            blender_enum.append(material.as_blender_tuple())

        return blender_enum

    @staticmethod
    def get_type_of(material_type_name: str) -> 'MaterialType':
        for material in MaterialType:
            if material_type_name in material.get_name():
                return material
