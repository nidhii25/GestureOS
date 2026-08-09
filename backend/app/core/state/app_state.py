from .application_state import ApplicationState
from .tracking_state import TrackingState
from .camera_state import CameraState
from .voice_state import VoiceState
from .gesture_state import GestureState
from .permission_state import PermissionState

class AppState:
    def __init__(self):
        self.application = ApplicationState()
        self.tracking = TrackingState()
        self.permission = PermissionState()
        self.camera = CameraState()
        self.voice = VoiceState()
        self.gesture = GestureState()
        


app_state = AppState()