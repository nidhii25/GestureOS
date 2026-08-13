class EdgeTrigger:
    """
    Detects the transition from False -> True.

    Returns True only once when the gesture becomes active.
    """

    def __init__(self):
        self.previous_state = False

    def update(self, current_state: bool):
        triggered = current_state and not self.previous_state

        self.previous_state = current_state

        return triggered

    def reset(self):
        self.previous_state = False