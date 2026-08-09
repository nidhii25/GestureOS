import mediapipe as mp
import cv2

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandDetectionService:
    """
    Detects hands and their landmarks from OpenCV frames.
    """

    def __init__(self, model_path: str):
        self.model_path = model_path
        self.landmarker = None

    def initialize(self):
        base_options = python.BaseOptions(
            model_asset_path=self.model_path
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=2
        )

        self.landmarker = vision.HandLandmarker.create_from_options(
            options
        )

    def detect(self, frame):
        if self.landmarker is None:
            raise RuntimeError(
                "HandDetectionService is not initialized."
            )

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        result = self.landmarker.detect(mp_image)

        return result

    def close(self):
        if self.landmarker is not None:
            self.landmarker.close()
            self.landmarker = None