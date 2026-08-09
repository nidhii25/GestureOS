from app.gestures.gesture_types import GestureType
from app.gestures.finger_utils import is_open_palm

class GestureRecognizer:
    """
    Converts processed hand landmarks into recognized gestures.
    """

    def recognize(self, landmarks):
        if is_open_palm(landmarks):
            return GestureType.OPEN_PALM

        return GestureType.NONE