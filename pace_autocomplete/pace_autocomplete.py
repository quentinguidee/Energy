from time import sleep

import pyautogui

from ..classes.face_type import FaceType
from ..energyreport.classes.orientation import Orientation
from .classes.face import Face
from .classes.plane import Plane
from .classes.plane_instance import PlaneInstance
from .config import Config

pyautogui.PAUSE = 0.15


def fix_numerics(string: str):
    l = list(string)
    for i in range(len(l)):
        if l[i].isnumeric():
            l[i] = 'num' + l[i]
    return l


def create_file():
    pyautogui.hotkey('ctrl', 'n')
    pyautogui.typewrite(['tab', 'down', 'down', 'enter', 'enter'])
    sleep(1.5)


class Type:
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
    @classmethod
    def create(cls, plane: Plane, face_type: FaceType, it: int):
        if face_type == FaceType.ROOF:
            pyautogui.hotkey('ctrl', 'd')
        elif face_type == FaceType.WALL:
            pyautogui.hotkey('ctrl', 'f')

        if face_type == FaceType.FLOOR:
            # pyautogui.prompt(
            #     text="Encodez manuellement la valeur" + str(
            #         plane.surface) + "dans Enveloppe > Planchers > Surface brute, puis cliquez sur OK.",
            #     title="PACE Autocomplete"
            # )
            # pyautogui.alert(
            #     text="Cliquez sur OK et recliquez sur PACE dans les 3 secondes. Ensuite, ne touchez plus à rien.",
            #     title="PACE Autocomplete"
            # )
            pass

        else:
            if it == 0:
                sleep(0.2)
            else:
                pyautogui.typewrite(['tab'])

            pyautogui.typewrite(['tab'] * 2)
            # pyautogui.typewrite(['right'] * 15)
            # pyautogui.typewrite(['backspace'] * 15)
            # sleep(0.2)
            # pyautogui.typewrite(fix_numerics(plane.name))
            pyautogui.typewrite(['tab'])
            pyautogui.typewrite(['down'] * (list(Orientation).index(plane.orientation) + 2))
            pyautogui.typewrite(['enter'])
            pyautogui.moveTo(Config.area_button_position_x, Config.area_button_position_y)
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
        # pyautogui.typewrite(['right'] * 15)
        # pyautogui.typewrite(['backspace'] * 15)
        # sleep(0.2)
        # pyautogui.typewrite(fix_numerics(plane_instance.name))
        pyautogui.typewrite(['tab'])
        pyautogui.typewrite(['down'] * (plane_instance.face.i + 2))
        pyautogui.typewrite(['enter'])

        if face_type == FaceType.FLOOR:
            pyautogui.moveTo(Config.area_button_position_x, Config.area_button_position_y)
        else:
            pyautogui.moveTo(Config.area_button_position_x, Config.area_button_position_y + 22)

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


def configure():
    """
    Requires Tkinter.
    """
    yes = "Oui"
    no = "Non"

    choice = pyautogui.confirm(
        text="Utiliser les coordonnées (" + str(Config.area_button_position_x) + "," + str(
            Config.area_button_position_y) + ") pour le bouton \"Surface brute\".",
        title="Configuration",
        buttons=[yes, no]
    )

    if choice == no:
        pyautogui.alert(
            text="""
                    - Ouvrez le logiciel PACE
                    - Créez un nouveau document
                    - Créer un toit avec le raccourci CTRL+D
                    """
        )
        while choice == no:
            pyautogui.alert(
                text="""
                        - Vous allez devoir passer la souris sur l'icône à côté de "Surface brute".
                        Quand vous êtes prêt, cliquez sur OK. Vous aurez 3 secondes pour passer la souris dessus. Ne bougez plus.
                        """
            )
            sleep(3)
            Config.area_button_position_x, Config.area_button_position_y = pyautogui.position()
            choice = pyautogui.confirm(
                text="Position retenue: (" + str(Config.area_button_position_x) + "," + str(
                    Config.area_button_position_y) + ")\nSi tout est OK, fermez le fichier PACE (en gardant PACE ouvert) et cliquez sur OUI.",
                buttons=[yes, no]
            )

    pyautogui.alert(
        text="Ouvrez le logiciel PACE, cliquez sur OK et recliquez sur PACE dans les 3 secondes. Ensuite, ne touchez plus à rien.",
        title="PACE Autocomplete"
    )
    sleep(3)


class Save:
    faces = {}

    @staticmethod
    def reset():
        Save.faces = {
            FaceType.WALL.get_name(): [],
            FaceType.ROOF.get_name(): [],
            FaceType.FLOOR.get_name(): [],
        }
        Save.wall_planes = []
        Save.roof_planes = []
        Save.floor_planes = []

    @staticmethod
    def get_face(code: str) -> Face:
        face_type = FaceType.get_face_type(code[0])
        faces = Save.faces[face_type.get_name()]
        for face in faces:
            if face.code == code:
                return face

    wall_planes: [Plane] = []
    roof_planes: [Plane] = []
    floor_planes: [Plane] = []

# def example():
#    configure()
#
#    create_file()
#
#    wall_1 = Face(0, 'M-01', 'Mur type 1')
#    wall_2 = Face(1, 'M-02', 'Mur type 2')
#    Type.create_all([wall_1, wall_2], FaceType.WALL)
#
#    roof_1 = Face(0, 'R-01', 'Roof type 1')
#    Type.create_all([roof_1], FaceType.ROOF)
#
#    floor_1 = Face(0, 'F-01', 'Floor type 1')
#    Type.create_all([floor_1], FaceType.FLOOR)
#
#    Envelope.create_all(
#        [
#            Plane('Wall 1', Orientation.NE, 3, [
#                PlaneInstance('Instance 1', wall_1, 6),
#                PlaneInstance('Instance 2', wall_2, 6)
#            ]),
#            Plane('Wall 2', Orientation.S, 4, [
#                PlaneInstance('Instance 3', wall_2, 10)
#            ]),
#        ],
#        FaceType.WALL
#    )
#
#    Envelope.create_all(
#        [
#            Plane('Roof 1', Orientation.NE, 3, [
#                PlaneInstance('Instance 1', roof_1, 6),
#                PlaneInstance('Instance 2', roof_1, 6)
#            ]),
#            Plane('Wall 2', Orientation.S, 4, [
#                PlaneInstance('Instance 3', roof_1, 10)
#            ]),
#        ],
#        FaceType.ROOF
#    )
#
#    Envelope.create_all(
#        [
#            Plane('Floor', Orientation.NE, 3, [
#                PlaneInstance('Instance 1', floor_1, 6),
#                PlaneInstance('Instance 2', floor_1, 6)
#            ]),
#        ],
#        FaceType.FLOOR
#    )
#
#
# start()
