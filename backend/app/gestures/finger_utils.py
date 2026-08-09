from app.vision.geometry import angle_between_points
from app.vision.landmark_indices import (
    INDEX_MCP,
    INDEX_PIP,
    INDEX_DIP,
    MIDDLE_MCP,
    MIDDLE_PIP,
    MIDDLE_DIP,
    RING_MCP,
    RING_PIP,
    RING_DIP,
    PINKY_MCP,
    PINKY_PIP,
    PINKY_DIP,
)

def is_finger_extended(landmarks, mcp, pip, dip):
    angle = angle_between_points(
        landmarks[mcp],
        landmarks[pip],
        landmarks[dip],
    )

    return angle > 2.7

def is_index_extended(landmarks):
    return is_finger_extended(
        landmarks,
        INDEX_MCP,
        INDEX_PIP,
        INDEX_DIP,
    )


def is_middle_extended(landmarks):
    return is_finger_extended(
        landmarks,
        MIDDLE_MCP,
        MIDDLE_PIP,
        MIDDLE_DIP,
    )


def is_ring_extended(landmarks):
    return is_finger_extended(
        landmarks,
        RING_MCP,
        RING_PIP,
        RING_DIP,
    )


def is_pinky_extended(landmarks):
    return is_finger_extended(
        landmarks,
        PINKY_MCP,
        PINKY_PIP,
        PINKY_DIP,
    )

def is_open_palm(landmarks):
    return (
        is_index_extended(landmarks)
        and is_middle_extended(landmarks)
        and is_ring_extended(landmarks)
        and is_pinky_extended(landmarks)
    )