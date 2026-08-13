class ScrollMode:
    """
    Manages whether scroll mode is active.
    """

    def __init__(self):
        self.active = False

    def toggle(self):
        self.active = not self.active
        return self.active

    def reset(self):
        self.active = False