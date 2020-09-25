from enum import Enum


class MaterialType(Enum):
    FreeAir = ('Free air', 0)
    SemiStaticAir = ('Semi Static air', 1)
    StaticAir = ('Static air', 2)
    Masonry = ('Masonry', 3)
    Wood = ('Wood', 4)
    Insulation = ('Insulation', 5)

    def get_name(self) -> str:
        return self.value[0]

    def get_blender_tuple(self):
        v = self.value[0]
        return v, v, v, self.value[1]

    @staticmethod
    def as_blender_enum():
        blender_enum = []
        for material in MaterialType:
            blender_enum.append(material.get_blender_tuple())

        return blender_enum
