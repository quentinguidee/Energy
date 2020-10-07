from ..envelopes.wall import Wall
from ..types.wall_type import WallType
from ..pace_object import PaceObject


class WallInstance(PaceObject):
    wall_type: WallType
    wall: Wall
    upcoming_wall_type: WallType

    @property
    def template_filename(self) -> str:
        if self.is_in_wall_type:
            return 'templates/instances/wallinstance.xml'
        elif self.is_in_wall:
            if self.upcoming_wall_type.is_already_registered:
                return 'templates/instances/wallinstancesecondemptywalltype.xml'
            else:
                return 'templates/instances/wallinstancesecond.xml'

    @property
    def path(self):
        if self.is_in_wall_type:
            return './building/skin/constructionElements/com.hemmis.mrw.pace.model.skin.Wall[@id="' + str(self.wall_type.id) + '"]/wallInstances/INITIAL'
        elif self.is_in_wall:
            return './building/skin/constructionElements/com.hemmis.mrw.pace.model.skin.Wall[@id="' + str(self.wall.wall_instance.wall_type.id) + '"]/wallInstances/INITIAL/com.hemmis.mrw.pace.model.skin.WallInstance[@id="' + str(self.wall.wall_instance.id) + '"]/plane/wallInstances/INITIAL'

    def __init__(self, name: str, surface: float):
        self.is_in_wall_type = False
        self.is_in_wall = False
        self.name = name
        self.surface = surface

    @property
    def replace_queries(self) -> dict:
        wall_instance_reference = {
            'com.hemmis.mrw.pace.model.skin.WallInstance': {
                'reference': 'CURRENT_ID'
            }
        }

        if self.is_in_wall_type:
            return {
                'shortDescription': {
                    'value': self.name
                },
                'opaqueElement/INITIAL': {
                    'reference': self.wall_type.id
                },
                'MORE': {
                    './building/skin/wallPlanes/INITIAL': {
                        'com.hemmis.mrw.pace.model.skin.WallPlane': {
                            'reference': 'CURRENT_ID+15'
                        }
                    },
                    './building/skin/constructionElements/com.hemmis.mrw.pace.model.skin.Wall[@id="' + str(self.wall_type.id) + '"]/wallInstances/SECOND': wall_instance_reference,
                    './building/skin/opaqueInstances/INITIAL': wall_instance_reference,
                    './building/skin/opaqueInstances/SECOND': wall_instance_reference
                }
            }
        elif self.is_in_wall:
            return {
                'shortDescription': {
                    'value': self.name
                },
                'plane': {
                    'reference': self.wall.wall_instance.id + 15
                },
                'MORE': {
                    './building/skin/constructionElements/com.hemmis.mrw.pace.model.skin.Wall[@id="' + str(self.wall.wall_instance.wall_type.id) + '"]/wallInstances/INITIAL': wall_instance_reference,
                    './building/skin/constructionElements/com.hemmis.mrw.pace.model.skin.Wall[@id="' + str(self.wall.wall_instance.wall_type.id) + '"]/wallInstances/SECOND': wall_instance_reference,
                    './building/skin/opaqueInstances/INITIAL': wall_instance_reference,
                    './building/skin/opaqueInstances/SECOND': wall_instance_reference
                }
            }

    def inside_wall_type(self, wall_type: WallType) -> 'WallInstance':
        self.is_in_wall_type = True
        self.wall_type = wall_type
        return self

    def inside_wall(self, wall: Wall, upcoming_wall_type: WallType) -> 'WallInstance':
        self.is_in_wall = True
        self.wall = wall
        self.upcoming_wall_type = upcoming_wall_type
        return self
