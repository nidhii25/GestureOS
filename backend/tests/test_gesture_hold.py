import time

from app.gestures.gesture_hold import GestureHold
from app.gestures.gesture_types import GestureType


hold = GestureHold(hold_time=1.0)


print("First update:")
print(hold.update(GestureType.OPEN_PALM))

time.sleep(0.5)

print("After 0.5 seconds:")
print(hold.update(GestureType.OPEN_PALM))

time.sleep(0.6)

print("After another 0.6 seconds:")
print(hold.update(GestureType.OPEN_PALM))

print("Still holding:")
print(hold.update(GestureType.OPEN_PALM))

print("Gesture released:")
print(hold.update(GestureType.NONE))

print("New gesture:")
print(hold.update(GestureType.OPEN_PALM))