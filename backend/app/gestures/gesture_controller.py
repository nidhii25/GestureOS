from app.core.state.app_state import AppState
from app.gestures.gesture_types import GestureType
from app.core.state.tracking_state import TrackingStatus

class GestureController:
    """
    Handles actions triggered by confirmed gestures.
    """

    def __init__(self, app_state: AppState):
        self.app_state = app_state

    def handle(self, gesture: GestureType):
        """
        Handle a confirmed gesture.
        """

        if gesture == GestureType.OPEN_PALM:
            return self._toggle_tracking()

        return {
            "success": False,
            "message": "No action mapped to this gesture."
        }

    def _toggle_tracking(self):
        """
        Toggle tracking between ACTIVE and IDLE.
        """

        if self.app_state.tracking.status == TrackingStatus.ACTIVE:
            self.app_state.tracking.idle()

            return {
                "success": True,
                "message": "Tracking switched to idle mode."
            }

        self.app_state.tracking.start()

        return {
            "success": True,
            "message": "Tracking started successfully."
        }