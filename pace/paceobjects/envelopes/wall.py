from energyreport.classes.orientation import Orientation

from ..pace_object import PaceObject


class Wall(PaceObject):
    # template_filename = 'templates/envelopes/wallplane.xml'
    # path = './building/skin/wallPlanes/INITIAL'

    template_filename = None
    path = None

    wall_instance: 'WallInstance'

    def __init__(self, name: str, orientation: Orientation, surface: float):
        self.is_in_wall_instance = False
        self.name = name
        self.orientation = orientation
        self.surface = surface

    @property
    def replace_queries(self) -> dict:
        if self.is_in_wall_instance:
            return {
                'MORE': {
                    './building/skin/constructionElements/com.hemmis.mrw.pace.model.skin.Wall[@id="' + str(self.wall_instance.wall_type.id) + '"]/wallInstances/INITIAL/com.hemmis.mrw.pace.model.skin.WallInstance[@id="' + str(self.wall_instance.id) + '"]/plane': {
                        'shortDescription': {
                            'value': self.name
                        }
                    },
                    './building/skin/constructionElements/com.hemmis.mrw.pace.model.skin.Wall[@id="' + str(self.wall_instance.wall_type.id) + '"]/wallInstances/INITIAL/com.hemmis.mrw.pace.model.skin.WallInstance[@id="' + str(self.wall_instance.id) + '"]/plane/orientation': {
                        'INITIAL': {
                            'class': 'com.hemmis.mrw.pace.model.enums.Orientation',
                            'value': self.orientation.name
                        }
                    },
                    './building/skin/constructionElements/com.hemmis.mrw.pace.model.skin.Wall[@id="' + str(self.wall_instance.wall_type.id) + '"]/wallInstances/INITIAL/com.hemmis.mrw.pace.model.skin.WallInstance[@id="' + str(self.wall_instance.id) + '"]/plane/grossSurface': {
                        'INITIAL': {
                            'class': 'java.math.BigDecimal',
                            'value': self.surface
                        }
                    }
                }
            }

    def inside_wall_instance(self, wall_instance: 'WallInstance') -> 'Wall':
        self.is_in_wall_instance = True
        self.wall_instance = wall_instance
        return self
