import os
import bpy

from enum import Enum

from .files import get_path


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
        directory = get_path("labels")
        return os.path.join(directory, self.value + ".png")

    def load(self):
        if bpy.data.images.find(self.value + ".png") == -1:
            img = bpy.data.images.load(self.get_path())
            img.user_clear()  # Won't get saved into .blend files

    def get_icon(self, layout):
        self.load()
        return layout.icon(bpy.data.images[self.value + ".png"])
