import cv2
from app.core.state.app_state import AppState

class CameraService:
    def __init__(self, app_state: AppState):
        self.app_state = app_state
        self.camera = None

    def start_camera(self):
        if self.camera is not None:
            return {
                "success": True,
                "message": "Camera is already running."
            }
        camera_index = self.app_state.camera.camera_index
        self.camera = cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            self.camera = None
            return {
                "success": False,
                "message": f"Failed to open camera."
            }
        self.app_state.camera.is_active = True

        return {
            "success": True,
            "message": "Camera started successfully."
        }

    
    def read_frame(self):
        if self.camera is None:
            return False, None

        success, frame = self.camera.read()

        if not success:
            return False, None

        return True, frame

    def stop_camera(self):
        if self.camera is None:
            return {
                "success": False,
                "message": "Camera is not running."
            }
        self.camera.release()
        self.camera = None
        self.app_state.camera.is_active = False

        return {
            "success": True,
            "message": "Camera stopped successfully."
        }