from enum import Enum


class Orientation(Enum):
    S = (-191.25, -168.75)
    SSW = (-168.75, -146.25)
    SW = (-146.25, -123.75)
    WSW = (-123.75, -101.25)
    W = (-101.25, -78.75)
    WNW = (-78.75, -56.25)
    NW = (-56.25, -33.75)
    NNW = (-33.75, -11.25)
    N = (-11.25, 11.25)
    NNE = (-11.25, 33.75)
    NE = (33.75, 56.25)
    ENE = (56.25, 78.75)
    E = (78.75, 101.25)
    ESE = (101.25, 123.75)
    SE = (123.75, 146.25)
    SSE = (146.25, 168.75)

    @staticmethod
    def get_direction(angle_proj: float) -> 'Orientation':
        if 168.75 <= angle_proj < 191.25:
            return Orientation.S

        for direction in Orientation:
            if direction.value[0] <= angle_proj < direction.value[1]:
                return direction
