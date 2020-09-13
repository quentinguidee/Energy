from . import main
import importlib

bl_info = {
    "name": "ArToKi-Energy",
    "author": "Thierry Maes (tmaes)",
    "version": (0, 0, 10),
    "blender": (2, 90, 0),
    "api": 56533,
    "location": "Properties > Material > ArToKi EPB",
    "description": "Explore surface and volumes of building parts.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Material"}


def register():
    main.register()


def unregister():
    main.unregister()


importlib.reload(main)
