from dataclasses import dataclass


@dataclass
class LandmarkPoint:
    """
    Represents a single hand landmark.
    """

    x: float
    y: float
    z: float

class LandmarkProcessor:
    """
    Converts MediaPipe hand landmarks into application-friendly data.
    """

    def process_hand(self, hand_landmarks):
        return [
            LandmarkPoint(
                x=landmark.x,
                y=landmark.y,
                z=landmark.z
            )
            for landmark in hand_landmarks
        ]