from ..pace_object import PaceObject


class WallType(PaceObject):
    template_filename = 'templates/types/walltype.xml'
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
                './building/skin/walls': {
                    'com.hemmis.mrw.pace.model.skin.Wall': {
                        'reference': 'CURRENT_ID'
                    }
                }
            }
        }
