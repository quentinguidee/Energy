from ..pace_object import PaceObject


class Floor(PaceObject):
    template_filename = None
    path = None

    def __init__(self, surface: float):
        self.surface = surface

    @property
    def replace_queries(self) -> dict:
        return {
            'MORE': {
                './building/skin/floorPlane/grossSurface': {
                    'INITIAL': {
                        'class': 'java.math.BigDecimal',
                        'value': self.surface
                    }
                }
            }
        }
