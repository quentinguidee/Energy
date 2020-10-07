from paceautoclick.classes.face import Face


class PlaneInstance:
    def __init__(self, name: str, face: Face, surface: float):
        self.name = name
        self.face = face
        self.surface = surface
