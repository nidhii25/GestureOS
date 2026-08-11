import time

from app.gestures.gesture_types import GestureType


class GestureHold:
    """
    Detects when a gesture has been continuously held
    for a specified duration.
    """

    def __init__(self, hold_time: float = 1.0):
        self.hold_time = hold_time
        self.current_gesture = GestureType.NONE
        self.start_time = None
        self.triggered = False

    def update(self, gesture: GestureType) -> bool:
        """
        Update the current gesture.

        Returns True once when the gesture has been
        held for the required duration.
        """

        # No gesture detected.
        if gesture == GestureType.NONE:
            self.reset()
            return False

        # A new gesture has started.
        if gesture != self.current_gesture:
            self.current_gesture = gesture
            self.start_time = time.monotonic()
            self.triggered = False
            return False

        # Gesture is still being held.
        if self.start_time is None:
            self.start_time = time.monotonic()
            return False

        elapsed_time = time.monotonic() - self.start_time

        # Trigger only once for this hold.
        if elapsed_time >= self.hold_time and not self.triggered:
            self.triggered = True
            return True

        return False

    def reset(self):
        """
        Reset the hold detector.
        """

        self.current_gesture = GestureType.NONE
        self.start_time = None
        self.triggered = False