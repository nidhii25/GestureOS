import time


class VictoryHold:
    """
    Requires the Victory gesture to remain visible
    for a specified duration before triggering.

    After triggering, it will not trigger again until
    the Victory gesture disappears.
    """

    def __init__(self, hold_time: float = 2.0):
        self.hold_time = hold_time

        self.start_time = None
        self.triggered = False

    def update(self, is_victory: bool):
        # Victory disappeared → reset and re-arm
        if not is_victory:
            self.start_time = None
            self.triggered = False
            return False

        # Already triggered while this Victory is held
        if self.triggered:
            return False

        # Start timing
        if self.start_time is None:
            self.start_time = time.monotonic()
            return False

        # Check hold duration
        elapsed = time.monotonic() - self.start_time

        if elapsed >= self.hold_time:
            self.triggered = True
            return True

        return False

    def reset(self):
        self.start_time = None
        self.triggered = False