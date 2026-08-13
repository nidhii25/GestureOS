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
    def left_click(self):
        pyautogui.click(button="left")
    def right_click(self):
        pyautogui.click(button="right")

    def mouse_down(self, button="left"):
        pyautogui.mouseDown(button=button)


    def mouse_up(self, button="left"):
        pyautogui.mouseUp(button=button)

    def scroll(self, amount):
        pyautogui.scroll(amount)

    def double_click(self):
        pyautogui.doubleClick()