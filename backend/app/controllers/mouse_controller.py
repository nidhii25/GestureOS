import pyautogui


class MouseController:
    """
    Controls the Windows mouse cursor.
    """

    def move_cursor(self, x: int, y: int):
        pyautogui.moveTo(x, y)

    def move_relative(self, x: float, y: float):
        pyautogui.moveRel(
            x,
            y,
            duration=0
        )