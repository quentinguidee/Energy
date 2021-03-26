from .building import Building


class Save:
    building: Building = None

    @staticmethod
    def reset():
        Save.building = None
