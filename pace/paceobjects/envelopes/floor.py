from ..pace_object import PaceObject


class Floor(PaceObject):
    template_filename = None
    path = None

    def __init__(self, height: float, width: float):
        self.height = height
        self.width = width

    @property
    def replace_queries(self) -> dict:
        return {
            'MORE': {
                './building/skin/floorPlane/height': {
                    'INITIAL': {
                        'class': 'java.math.BigDecimal',
                        'value': self.height
                    }
                },
                './building/skin/floorPlane/width': {
                    'INITIAL': {
                        'class': 'java.math.BigDecimal',
                        'value': self.width
                    }
                }
            }
        }
