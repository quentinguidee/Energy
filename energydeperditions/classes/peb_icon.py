import os
from enum import Enum

import bpy
from ... import info


class PEBIcon(Enum):
    APP = "A_Plus_Plus"
    AP = "A_Plus"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"

    def get_path(self):
        directory = os.path.expanduser('~') + info.INSTALL_PATH + '/labels'
        return os.path.join(directory, self.value + ".png")

    def load(self):
        if bpy.data.images.find(self.value + ".png") == -1:
            img = bpy.data.images.load(self.get_path())
            img.user_clear()  # Won't get saved into .blend files

    def get_icon(self, layout):
        self.load()
        return layout.icon(bpy.data.images[self.value + ".png"])
