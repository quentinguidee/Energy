from ..pace_object import PaceObject


class RoofType(PaceObject):
    template_filename = 'templates/types/rooftype.xml'
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
                './building/skin/roofs': {
                    'com.hemmis.mrw.pace.model.skin.Roof': {
                        'reference': 'CURRENT_ID'
                    }
                }
            }
        }
