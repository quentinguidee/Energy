from enum import Enum


class EnvironmentType(Enum):
    OUTSIDE = ('Outside', 0)
    UNPROTECTED_SPACE = ('Unprotected space', 1)
    PROTECTED_SPACE = ('Protected space (no freeze)', 2)
    GROUND = ('Ground', 3)
    HEATED_SPACE = ('Heated space', 4)

    def get_name(self) -> str:
        return self.value[0]

    def as_blender_tuple(self):
        v = self.get_name()
        return v, v, v

    @staticmethod
    def as_blender_enum():
        blender_enum = []
        for environment in EnvironmentType:
            blender_enum.append(environment.as_blender_tuple())

        return blender_enum

    @staticmethod
    def get_type_of(environment_name: str) -> 'EnvironmentType':
        for environment in EnvironmentType:
            if environment_name in environment.get_name():
                return environment
