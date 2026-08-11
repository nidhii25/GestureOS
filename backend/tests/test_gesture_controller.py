from app.core.state.app_state import AppState
from app.core.state.tracking_state import TrackingStatus
from app.gestures.gesture_controller import GestureController
from app.gestures.gesture_types import GestureType


app_state = AppState()
controller = GestureController(app_state)


print("Initial state:")
print(app_state.tracking.status)


print("\nFirst OPEN_PALM:")
print(controller.handle(GestureType.OPEN_PALM))
print(app_state.tracking.status)


print("\nSecond OPEN_PALM:")
print(controller.handle(GestureType.OPEN_PALM))
print(app_state.tracking.status)


print("\nUnknown gesture:")
print(controller.handle(GestureType.NONE))