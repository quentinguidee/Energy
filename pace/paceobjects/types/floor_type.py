from ..pace_object import PaceObject


class FloorType(PaceObject):
    template_filename = 'templates/types/floortype.xml'
    path = './building/skin/constructionElements'

    def __init__(self, code: str, name: str):
        self.code = code
        self.name = name

    @property
    def replace_queries(self) -> dict:
        return {
            'reference': {
                'value': self.code
            },
            'shortDescription': {
                'value': self.name
            },
            'MORE': {
                './building/skin/floors': {
                    'com.hemmis.mrw.pace.model.skin.Floor': {
                        'reference': 'CURRENT_ID'
                    }
                }
            }
        }
