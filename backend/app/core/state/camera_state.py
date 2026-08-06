from dataclasses import dataclass

@dataclass
class CameraState:
    is_active: bool = False
    camera_index: int = 0
    fps: int = 0
    resolution: tuple[int, int] = (1280, 720)