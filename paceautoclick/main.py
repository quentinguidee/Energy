from time import sleep

import pyautogui

from classes.face_type import FaceType
from energyreport.classes.orientation import Orientation
from paceautoclick.classes.face import Face
from paceautoclick.classes.plane import Plane
from paceautoclick.classes.plane_instance import PlaneInstance

top_left_x = 1920 + 24
top_left_y = 52

top_right_x = pyautogui.size().width - 24
top_right_y = top_left_y

menu_bar_height = 24

toolbar_height = 28
toolbar_item_width = 28

toolbar_create_x = top_left_x + toolbar_item_width * (7 / 2)
toolbar_create_y = top_left_y + menu_bar_height + toolbar_height / 2

pyautogui.PAUSE = 0.15


def fix_numerics(string: str):
    l = list(string)
    for i in range(len(l)):
        if l[i].isnumeric():
            l[i] = 'num' + l[i]
    return l


def create_file():
    pyautogui.moveTo(toolbar_create_x, toolbar_create_y)
    pyautogui.click()
    pyautogui.typewrite(['tab', 'down', 'down', 'enter', 'enter'])
    sleep(1.5)


class Certificate:
    @staticmethod
    def fold():
        LeftBar.fold(1, 0)


class LeftBar:
    start_x = top_left_x + 8
    start_y = top_left_y + menu_bar_height + toolbar_height

    item_height = 15
    item_tab = 24

    @staticmethod
    def select(element_index: int, tab: int):
        pyautogui.moveTo(
            LeftBar.start_x + LeftBar.item_tab * tab + 20,
            LeftBar.start_y + LeftBar.item_height * element_index
        )
        pyautogui.click()

    @staticmethod
    def fold(element_index: int, tab: int):
        pyautogui.moveTo(
            LeftBar.start_x + LeftBar.item_tab * tab,
            LeftBar.start_y + LeftBar.item_height * element_index
        )
        pyautogui.click()


class Type:
    @staticmethod
    def fold_all():
        LeftBar.fold(3, 1)

    @staticmethod
    def get_left_bar_element_index(face_type: FaceType):
        if face_type == FaceType.ROOF:
            return 4
        elif face_type == FaceType.WALL:
            return 5
        else:
            return 6

    @staticmethod
    def fold(face_type: FaceType):
        LeftBar.fold(Type.get_left_bar_element_index(face_type), 2)

    @staticmethod
    def create(code: str, name: str, face_type: FaceType, it: int):
        if face_type == FaceType.ROOF:
            pyautogui.hotkey('ctrl', 't')
        elif face_type == FaceType.WALL:
            pyautogui.hotkey('ctrl', 'm')
        else:
            pyautogui.hotkey('ctrl', 'p')

        if it == 0:
            sleep(0.2)
        else:
            pyautogui.typewrite(['tab'])

        pyautogui.typewrite(['tab'] * 2)
        pyautogui.typewrite(['right'] * 4)
        pyautogui.typewrite(['backspace'] * 4)
        sleep(0.2)
        pyautogui.typewrite(fix_numerics(code))
        pyautogui.typewrite(['tab'])
        pyautogui.typewrite(fix_numerics(name))

    @staticmethod
    def create_all(types: [Face], face_type: FaceType):
        it = 0
        for _type in types:
            Type.create(_type.code, _type.name, face_type, it)
            it += 1


class Envelope:
    @staticmethod
    def fold_all():
        LeftBar.fold(4, 1)

    @staticmethod
    def fold(face_type: FaceType):
        LeftBar.fold(Envelope.get_left_bar_element_index(face_type), 2)

    @staticmethod
    def get_left_bar_element_index(face_type: FaceType):
        if face_type == FaceType.ROOF:
            return 5
        elif face_type == FaceType.WALL:
            return 6
        else:
            return 7

    @classmethod
    def create(cls, plane: Plane, face_type: FaceType, it: int):
        if face_type == FaceType.ROOF:
            pyautogui.hotkey('ctrl', 'd')
        elif face_type == FaceType.WALL:
            pyautogui.hotkey('ctrl', 'f')

        if face_type == FaceType.FLOOR:
            Type.fold_all()
            Envelope.fold(FaceType.ROOF)
            Envelope.fold(FaceType.WALL)
            LeftBar.select(Envelope.get_left_bar_element_index(face_type), 2)
            sleep(1.5)
            pyautogui.moveTo(top_left_x + 663, top_left_y + 134)
            pyautogui.click()
            pyautogui.typewrite(fix_numerics(str(plane.surface)))
            pyautogui.typewrite(['enter'])

        else:
            if it == 0:
                sleep(0.2)
            else:
                pyautogui.typewrite(['tab'])

            pyautogui.typewrite(['tab'] * 2)
            pyautogui.typewrite(['right'] * 15)
            pyautogui.typewrite(['backspace'] * 15)
            sleep(0.2)
            pyautogui.typewrite(fix_numerics(plane.name))
            pyautogui.typewrite(['tab'])
            pyautogui.typewrite(['down'] * (list(Orientation).index(plane.orientation) + 2))
            pyautogui.typewrite(['enter'])
            pyautogui.moveTo(top_left_x + 663, top_left_y + 228)
            pyautogui.click()
            pyautogui.typewrite(fix_numerics(str(plane.surface)))
            pyautogui.typewrite(['enter'])

    @staticmethod
    def create_instance(plane_instance: PlaneInstance, face_type: FaceType, it: int):
        if face_type == FaceType.ROOF:
            pyautogui.hotkey('ctrl', 'shift', 't')
        elif face_type == FaceType.WALL:
            pyautogui.hotkey('ctrl', 'shift', 'm')
        else:
            pyautogui.hotkey('ctrl', 'shift', 'p')

        if it == 0:
            sleep(0.2)
        else:
            pyautogui.typewrite(['tab'])

        pyautogui.typewrite(['tab'] * 2)
        pyautogui.typewrite(['right'] * 15)
        pyautogui.typewrite(['backspace'] * 15)
        sleep(0.2)
        pyautogui.typewrite(fix_numerics(plane_instance.name))
        pyautogui.typewrite(['tab'])
        pyautogui.typewrite(['down'] * (plane_instance.face.i + 2))
        pyautogui.typewrite(['enter'])

        if face_type == FaceType.FLOOR:
            pyautogui.moveTo(top_left_x + 663, top_left_y + 228)
        else:
            pyautogui.moveTo(top_left_x + 663, top_left_y + 248)

        pyautogui.click()
        pyautogui.typewrite(fix_numerics(str(plane_instance.surface)))
        pyautogui.typewrite(['enter'])

    @staticmethod
    def create_all(planes: [Plane], face_type: FaceType):
        i = 0
        for plane in planes:
            Envelope.create(plane, face_type, i)
            j = 0
            for plane_instance in plane.plane_instances:
                Envelope.create_instance(plane_instance, face_type, j)
                j += 1

            i += 1


create_file()

wall_1 = Face(0, 'M-01', 'Mur type 1')
wall_2 = Face(1, 'M-02', 'Mur type 2')
Type.create_all([wall_1, wall_2], FaceType.WALL)

roof_1 = Face(0, 'R-01', 'Roof type 1')
Type.create_all([roof_1], FaceType.ROOF)

floor_1 = Face(0, 'F-01', 'Floor type 1')
Type.create_all([floor_1], FaceType.FLOOR)

Envelope.create_all(
    [
        Plane('Wall 1', Orientation.NE, 3, [
            PlaneInstance('Instance 1', wall_1, 6),
            PlaneInstance('Instance 2', wall_2, 6)
        ]),
        Plane('Wall 2', Orientation.S, 4, [
            PlaneInstance('Instance 3', wall_2, 10)
        ]),
    ],
    FaceType.WALL
)

Envelope.create_all(
    [
        Plane('Roof 1', Orientation.NE, 3, [
            PlaneInstance('Instance 1', roof_1, 6),
            PlaneInstance('Instance 2', roof_1, 6)
        ]),
        Plane('Wall 2', Orientation.S, 4, [
            PlaneInstance('Instance 3', roof_1, 10)
        ]),
    ],
    FaceType.ROOF
)

Envelope.create_all(
    [
        Plane('Floor', Orientation.NE, 3, [
            PlaneInstance('Instance 1', floor_1, 6),
            PlaneInstance('Instance 2', floor_1, 6)
        ]),
    ],
    FaceType.FLOOR
)
