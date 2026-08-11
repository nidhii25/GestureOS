from app.gestures.finger_utils import (
    is_index_extended,
    is_middle_extended,
    is_ring_extended,
    is_pinky_extended,
)


def is_index_pointing(landmarks):
    """
    Returns True when the index finger is extended
    and the other four fingers are folded.
    """

    return (
        is_index_extended(landmarks)
        and not is_middle_extended(landmarks)
        and not is_ring_extended(landmarks)
        and not is_pinky_extended(landmarks)
    )