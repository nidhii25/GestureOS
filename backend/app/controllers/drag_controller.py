class DragController:
    """
    Controls mouse drag state.

    Pinch starts the drag.
    Pinch release ends the drag.
    """

    def __init__(self, mouse_controller):
        self.mouse_controller = mouse_controller
        self.dragging = False

    def start_drag(self):
        if self.dragging:
            return False

        self.mouse_controller.mouse_down(button="left")
        self.dragging = True

        return True

    def stop_drag(self):
        if not self.dragging:
            return False

        self.mouse_controller.mouse_up(button="left")
        self.dragging = False

        return True

    def reset(self):
        if self.dragging:
            self.mouse_controller.mouse_up(
                button="left"
            )

        self.dragging = False