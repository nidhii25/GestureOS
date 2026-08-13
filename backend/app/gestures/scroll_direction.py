from app.gestures.finger_utils import (
    is_index_extended,
    is_middle_extended,
    is_ring_extended,
    is_pinky_extended,
)


def get_scroll_direction(landmarks):
    """
    Determine scroll direction from the index finger.

    Returns:
        "UP"
        "DOWN"
        None
    """

    # Index must be extended
    if not is_index_extended(landmarks):
        return None

    # Other fingers must be folded
    if is_middle_extended(landmarks):
        return None

    if is_ring_extended(landmarks):
        return None

    if is_pinky_extended(landmarks):
        return None

    index = landmarks[8]
    wrist = landmarks[0]

    # MediaPipe Y increases downward.
    #
    # Index above wrist → UP
    # Index below wrist  → DOWN

    if index.y < wrist.y:
        return "UP"

    if index.y > wrist.y:
        return "DOWN"

    return None