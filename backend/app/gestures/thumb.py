from app.vision.landmark_indices import (
    THUMB_TIP,
    THUMB_IP,
    THUMB_MCP,
    WRIST,
    INDEX_MCP,
    MIDDLE_MCP,
    RING_MCP,
    PINKY_MCP,
)
from app.gestures.finger_utils import (
    is_index_extended,
    is_middle_extended,
    is_ring_extended,
    is_pinky_extended,
)

def get_palm_center(landmarks):
    points = [
        landmarks[WRIST],
        landmarks[INDEX_MCP],
        landmarks[MIDDLE_MCP],
        landmarks[RING_MCP],
        landmarks[PINKY_MCP],
    ]

    x = sum(point.x for point in points) / len(points)
    y = sum(point.y for point in points) / len(points)
    z = sum(point.z for point in points) / len(points)

    return x, y, z


def distance_3d(point1, point2):
    return (
        (point2.x - point1.x) ** 2
        + (point2.y - point1.y) ** 2
        + (point2.z - point1.z) ** 2
    ) ** 0.5


def is_thumb_extended(landmarks):
    """
    Detect whether the thumb is extended away from the palm.
    """

    palm_x, palm_y, palm_z = get_palm_center(landmarks)

    thumb_tip = landmarks[THUMB_TIP]
    thumb_ip = landmarks[THUMB_IP]
    thumb_mcp = landmarks[THUMB_MCP]

    palm_distance = (
        (thumb_tip.x - palm_x) ** 2
        + (thumb_tip.y - palm_y) ** 2
        + (thumb_tip.z - palm_z) ** 2
    ) ** 0.5

    thumb_length = (
        distance_3d(thumb_mcp, thumb_ip)
        + distance_3d(thumb_ip, thumb_tip)
    )

    return palm_distance > thumb_length * 1.05


def is_left_thumb(landmarks, handedness):
    return (
        handedness.lower() == "left"
        and is_thumb_extended(landmarks)
        and not is_index_extended(landmarks)
        and not is_middle_extended(landmarks)
        and not is_ring_extended(landmarks)
        and not is_pinky_extended(landmarks)
    )


def is_right_thumb(landmarks, handedness):
    return (
        handedness.lower() == "right"
        and is_thumb_extended(landmarks)
        and not is_index_extended(landmarks)
        and not is_middle_extended(landmarks)
        and not is_ring_extended(landmarks)
        and not is_pinky_extended(landmarks)
    )