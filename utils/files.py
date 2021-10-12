import os

from ..info import INSTALL_PATH


def get_path(path: str):
    return os.path.expanduser('~') + INSTALL_PATH + '/' + path
