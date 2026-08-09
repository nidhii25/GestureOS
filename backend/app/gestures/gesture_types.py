from enum import Enum, auto


class GestureType(Enum):
    NONE = auto()
    INDEX_POINT = auto()
    LEFT_CLICK = auto()
    RIGHT_CLICK = auto()
    PINCH = auto()
    OPEN_PALM = auto()
    FIST = auto()
    SWIPE_LEFT = auto()
    SWIPE_RIGHT = auto()