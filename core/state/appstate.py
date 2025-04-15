from enum import Enum,auto

class APPSTATE(Enum):
    MAIN_MENU = auto()
    OPTIONS_MENU = auto()
    GAME_ACTIVE = auto()
    QUIT = auto()