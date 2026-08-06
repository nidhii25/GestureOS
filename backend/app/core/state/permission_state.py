from dataclasses import dataclass
from enum import Enum, auto


class PermissionStatus(Enum):

    NOT_REQUESTED = auto()
    GRANTED = auto()
    DENIED = auto()


@dataclass
class PermissionState:

    camera_permission: PermissionStatus = PermissionStatus.NOT_REQUESTED
    microphone_permission: PermissionStatus = PermissionStatus.NOT_REQUESTED

    def grant_camera(self):
        self.camera_permission = PermissionStatus.GRANTED

    def revoke_camera(self):
        self.camera_permission = PermissionStatus.DENIED

    def grant_microphone(self):
        self.microphone_permission = PermissionStatus.GRANTED

    def revoke_microphone(self):
        self.microphone_permission = PermissionStatus.DENIED