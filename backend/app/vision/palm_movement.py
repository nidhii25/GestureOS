class PalmMovement:
    """
    Converts palm movement into relative cursor movement.
    """

    def __init__(
        self,
        sensitivity: float = 2200.0,
        deadzone: float = 0.003,
    ):
        self.sensitivity = sensitivity
        self.deadzone = deadzone

        self.reference_x = None
        self.reference_y = None

    def update(self, x: float, y: float):
        """
        Calculate relative cursor movement from palm movement.
        """

        if self.reference_x is None:
            self.reference_x = x
            self.reference_y = y

            return 0, 0

        delta_x = x - self.reference_x
        delta_y = y - self.reference_y

        if (
            abs(delta_x) < self.deadzone
            and abs(delta_y) < self.deadzone
        ):
            return 0, 0

        movement_x = -delta_x * self.sensitivity
        movement_y = delta_y * self.sensitivity

        self.reference_x = x
        self.reference_y = y

        return movement_x, movement_y

    def reset(self):
        """
        Forget the current palm reference.

        The actual cursor position is not changed.
        """

        self.reference_x = None
        self.reference_y = None