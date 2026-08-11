import time

from app.controllers.mouse_controller import MouseController


mouse = MouseController()

print("Move right...")
mouse.move_relative(200, 0)

time.sleep(1)

print("Move left...")
mouse.move_relative(-200, 0)

time.sleep(1)

print("Move down...")
mouse.move_relative(0, 200)

time.sleep(1)

print("Move up...")
mouse.move_relative(0, -200)

print("Mouse controller test complete.")