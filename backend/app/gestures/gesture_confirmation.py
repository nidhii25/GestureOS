class GestureConfirmation:
    """
    Confirms a gesture only after it has remained
    consistently detected for a number of frames.
    """

    def __init__(self, required_frames: int = 5):
        self.required_frames = required_frames
        self.current_frames = 0
        self.confirmed = False

    def update(self, detected: bool):
        if detected:
            self.current_frames += 1

            if self.current_frames >= self.required_frames:
                self.confirmed = True

        else:
            self.current_frames = 0
            self.confirmed = False

        return self.confirmed

    def reset(self):
        self.current_frames = 0
        self.confirmed = False