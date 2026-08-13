class ContinuousScroll:
    """
    Produces a constant scroll amount while a
    scroll direction is active.
    """

    def __init__(self, speed: int = 3):
        self.speed = speed

    def get_amount(self, direction):
        if direction == "UP":
            return self.speed

        if direction == "DOWN":
            return -self.speed

        return 0