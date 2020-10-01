from energyreport.classes.orientation import Orientation

from .pace_object import PaceObject


class Roof(PaceObject):
    template_filename = 'templates/roofplane.xml'
    path = './building/skin/roofPlanes/INITIAL'

    def __init__(self, name: str, orientation: Orientation, angle: float, width: float, height: float):
        self.name = name
        self.orientation = orientation
        self.angle = angle
        self.width = width
        self.height = height

    @property
    def replace_queries(self):
        return {
            'shortDescription': {
                'value': self.name
            },
            'orientation/INITIAL': {
                'class': 'com.hemmis.mrw.pace.model.enums.Orientation',
                'value': self.orientation.name
            },
            'slope/INITIAL': {
                'class': 'java.math.BigDecimal',
                'value': self.angle
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
