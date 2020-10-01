from energyreport.classes.orientation import Orientation

from .pace_object import PaceObject


class Wall(PaceObject):
    template_filename = 'templates/wallplane.xml'
    path = './building/skin/wallPlanes/INITIAL'

    def __init__(self, name: str, orientation: Orientation, width: float, height: float):
        self.name = name
        self.orientation = orientation
        self.width = width
        self.height = height

    @property
    def replace_queries(self) -> dict:
        return {
            'shortDescription': {
                'value': self.name
            },
            'orientation/INITIAL': {
                'class': 'com.hemmis.mrw.pace.model.enums.Orientation',
                'value': self.orientation.name
            },
            'width/INITIAL': {
                'class': 'java.math.BigDecimal',
                'value': self.width
            },
            'height/INITIAL': {
                'class': 'java.math.BigDecimal',
                'value': self.height
            }
        }
