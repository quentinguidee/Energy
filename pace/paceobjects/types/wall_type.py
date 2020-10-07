from ..pace_object import PaceObject


class WallType(PaceObject):

    @property
    def template_filename(self):
        if self.is_in_wall_instance:
            return None
        else:
            return 'templates/types/walltype.xml'

    @property
    def path(self):
        if self.is_in_wall_instance:
            return None
            # return './building/skin/constructionElements/com.hemmis.mrw.pace.model.skin.Wall[@id="' + str(self.wall_instance.wall.wall_instance.wall_type.id) + '"]/wallInstances/INITIAL/com.hemmis.mrw.pace.model.skin.WallInstance/plane/wallInstances/INITIAL/com.hemmis.mrw.pace.model.skin.WallInstance[@id="' + str(self.wall_instance.id) + '"]/INITIAL'
        else:
            return './building/skin/constructionElements'

    def __init__(self, code: str, name: str):
        self.is_in_wall_instance = False
        self.is_already_registered = False
        self.registered_in_wall_instance: 'WallInstance' = None
        self.wall_instance: 'WallInstance' = None
        self.code = code
        self.name = name

    @property
    def replace_queries(self) -> dict:
        if self.is_in_wall_instance:
            if self.is_already_registered:
                return {
                    'MORE': {
                        './building/skin/constructionElements/com.hemmis.mrw.pace.model.skin.Wall[@id="' + str(self.wall_instance.wall.wall_instance.wall_type.id) + '"]/wallInstances/INITIAL/com.hemmis.mrw.pace.model.skin.WallInstance[@id="' + str(self.wall_instance.wall.wall_instance.id) + '"]/plane/wallInstances/INITIAL/com.hemmis.mrw.pace.model.skin.WallInstance[@id="' + str(
                            self.wall_instance.id) + '"]/opaqueElement': {
                            'INITIAL': {
                                'class': 'com.hemmis.mrw.pace.model.skin.Wall',
                                'reference': self.registered_in_wall_instance.id + 18
                            },
                        },
                        # './building/skin/walls': {
                        #     'com.hemmis.mrw.pace.model.skin.Wall': {
                        #         'reference': self.registered_in_wall_instance.id + 18
                        #     }
                        # }
                    }
                }
            else:
                self.is_already_registered = True
                return {
                    'MORE': {
                        './building/skin/constructionElements/com.hemmis.mrw.pace.model.skin.Wall[@id="' + str(self.wall_instance.wall.wall_instance.wall_type.id) + '"]/wallInstances/INITIAL/com.hemmis.mrw.pace.model.skin.WallInstance[@id="' + str(self.wall_instance.wall.wall_instance.id) + '"]/plane/wallInstances/INITIAL/com.hemmis.mrw.pace.model.skin.WallInstance[@id="' + str(
                            self.wall_instance.id) + '"]/opaqueElement/INITIAL': {
                            'reference': {
                                'value': self.code
                            },
                            'shortDescription': {
                                'value': self.name
                            }
                        },
                        './building/skin/walls': {
                            'com.hemmis.mrw.pace.model.skin.Wall': {
                                'reference': self.wall_instance.id + 18
                            }
                        }
                    }
                }
        else:
            self.is_already_registered = True
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

    # def is_already_registered(self):
    #     return self.wall_instance is not None and self.wall_instance is self.registered_in_wall_instance

    def inside_wall_instance(self, wall_instance: 'WallInstance') -> 'WallType':
        self.is_in_wall_instance = True
        self.wall_instance = wall_instance
        if self.id is None:
            self.registered_in_wall_instance = wall_instance
        return self
