from app.gestures.finger_utils import (
    is_index_extended,
    is_middle_extended,
    is_ring_extended,
    is_pinky_extended,
)


def is_victory(landmarks):
    """
    Detect a Victory / V sign.

    Index and middle fingers must be extended.
    Ring and pinky fingers must be folded.
    """

    return (
        is_index_extended(landmarks)
        and is_middle_extended(landmarks)
        and not is_ring_extended(landmarks)
        and not is_pinky_extended(landmarks)
    )