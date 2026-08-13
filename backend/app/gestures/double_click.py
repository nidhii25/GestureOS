from app.gestures.finger_utils import (
    is_index_extended,
    is_middle_extended,
    is_ring_extended,
    is_pinky_extended,
)


def is_double_click_gesture(landmarks):
    """
    Detect H008 double-click gesture.

    Index  -> folded
    Middle -> folded
    Ring   -> folded
    Pinky  -> extended

    Thumb is intentionally ignored.
    """

    return (
        not is_index_extended(landmarks)
        and not is_middle_extended(landmarks)
        and not is_ring_extended(landmarks)
        and is_pinky_extended(landmarks)
    )