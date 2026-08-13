class PalmMovement:
    """
    Converts palm movement into smooth relative cursor movement.
    """

    def __init__(
        self,
        sensitivity: float = 2200.0,
        deadzone: float = 0.002,
        smoothing: float = 0.35,
    ):
        self.sensitivity = sensitivity
        self.deadzone = deadzone
        self.smoothing = smoothing

        self.reference_x = None
        self.reference_y = None

        self.smoothed_x = None
        self.smoothed_y = None

    def update(self, x: float, y: float):
        """
        Calculate smooth relative cursor movement
        from palm movement.
        """

        # First frame
        if self.reference_x is None:
            self.reference_x = x
            self.reference_y = y

            self.smoothed_x = x
            self.smoothed_y = y

            return 0, 0

        # Smooth the palm position
        self.smoothed_x += (
            x - self.smoothed_x
        ) * self.smoothing

        self.smoothed_y += (
            y - self.smoothed_y
        ) * self.smoothing

        # Calculate movement from the smoothed position
        delta_x = self.smoothed_x - self.reference_x
        delta_y = self.smoothed_y - self.reference_y

        # Ignore tiny movements caused by landmark jitter
        if (
            abs(delta_x) < self.deadzone
            and abs(delta_y) < self.deadzone
        ):
            return 0, 0

        movement_x = -delta_x * self.sensitivity
        movement_y = delta_y * self.sensitivity

        # Update reference
        self.reference_x = self.smoothed_x
        self.reference_y = self.smoothed_y

        return movement_x, movement_y

    def reset(self):
        """
        Forget the current palm reference.

        The actual cursor position is not changed.
        """

        self.reference_x = None
        self.reference_y = None

        self.smoothed_x = None
        self.smoothed_y = None