from app.vision.geometry import distance
from app.vision.landmark_indices import THUMB_TIP, INDEX_TIP


class PinchDetector:
    """
    Detects a stable pinch between the thumb and index finger.
    """

    def __init__(
        self,
        pinch_threshold: float = 0.045,
        release_threshold: float = 0.060,
    ):
        self.pinch_threshold = pinch_threshold
        self.release_threshold = release_threshold

        self.is_pinching = False

    def update(self, landmarks):
        thumb = landmarks[THUMB_TIP]
        index = landmarks[INDEX_TIP]

        pinch_distance = distance(
            thumb,
            index,
        )

        if not self.is_pinching:
            if pinch_distance < self.pinch_threshold:
                self.is_pinching = True

        else:
            if pinch_distance > self.release_threshold:
                self.is_pinching = False

        return self.is_pinching

    def reset(self):
        self.is_pinching = False