import time


class DoubleClickHold:
    """
    Requires the H008 pinky gesture to remain stable
    for a short duration before triggering.

    Once triggered, it cannot trigger again until
    the pinky gesture disappears.
    """

    def __init__(self, hold_time: float = 0.6):
        self.hold_time = hold_time

        self.start_time = None
        self.triggered = False

    def update(self, active: bool):

        if not active:
            self.start_time = None
            self.triggered = False
            return False

        if self.triggered:
            return False

        if self.start_time is None:
            self.start_time = time.monotonic()
            return False

        elapsed = time.monotonic() - self.start_time

        if elapsed >= self.hold_time:
            self.triggered = True
            return True

        return False

    def reset(self):
        self.start_time = None
        self.triggered = False