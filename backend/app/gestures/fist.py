from app.gestures.finger_utils import (
    is_index_extended,
    is_middle_extended,
    is_ring_extended,
    is_pinky_extended,
)


def is_fist(landmarks):
    """
    Detect a closed fist.

    All four non-thumb fingers must be folded.
    """

    return (
        not is_index_extended(landmarks)
        and not is_middle_extended(landmarks)
        and not is_ring_extended(landmarks)
        and not is_pinky_extended(landmarks)
    )


def is_open_hand(landmarks):
    """
    Detect an open hand.

    All four non-thumb fingers must be extended.
    """

    return (
        is_index_extended(landmarks)
        and is_middle_extended(landmarks)
        and is_ring_extended(landmarks)
        and is_pinky_extended(landmarks)
    )