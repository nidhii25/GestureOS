from app.core.state.app_state import AppState
from app.core.state.tracking_state import TrackingStatus
from app.core.state.permission_state import PermissionStatus


class TrackingService:
    """
    Handles all tracking-related business logic.
    """

    def __init__(self, app_state: AppState):
        self.app_state = app_state

    def start_tracking(self) -> dict:

        if not self.app_state.application.is_running:
            return {
                "success": False,
                "message": "Application is not running."
            }

        if (
            self.app_state.permission.camera_permission
            != PermissionStatus.GRANTED
        ):
            return {
                "success": False,
                "message": "Camera permission is required."
            }

        if (
            self.app_state.tracking.status
            == TrackingStatus.ACTIVE
        ):
            return {
                "success": True,
                "message": "Tracking is already active."
            }

        self.app_state.tracking.start()

        return {
            "success": True,
            "message": "Tracking started successfully."
        }

    def idle_tracking(self) -> dict:

        self.app_state.tracking.idle()

        return {
            "success": True,
            "message": "Tracking switched to idle mode."
        }

    def reset_tracking(self) -> dict:

        self.app_state.tracking.reset()

        return {
            "success": True,
            "message": "Tracking reset successfully."
        }