from energyreport.classes.orientation import Orientation
from paceautoclick.classes.plane_instance import PlaneInstance


class Plane:
    def __init__(self, name: str, orientation: Orientation, surface: float, plane_instances: [PlaneInstance]):
        self.name = name
        self.orientation = orientation
        self.surface = surface
        self.plane_instances = plane_instances
