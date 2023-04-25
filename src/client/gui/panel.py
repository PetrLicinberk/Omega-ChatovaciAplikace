from enum import IntEnum
from PyQt6 import QtWidgets

class Panel(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

    def reset(self):
        raise NotImplementedError

class Panels(IntEnum):
    '''
    Enum of all panel ids.
    '''
    LOGIN = 0
    REGISTER = 1
    MAIN = 2
    FINDUSER = 3
    INVITES = 4
    MY_PROFILE = 5
    VIEW_PROFILE = 6
    EDIT_PROFILE = 7