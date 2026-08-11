from app.vision.landmark_indices import (
    WRIST,
    INDEX_MCP,
    MIDDLE_MCP,
    RING_MCP,
    PINKY_MCP,
)


class PalmTracker:
    """
    Calculates the center position of the palm
    from hand landmarks.
    """

    def get_palm_center(self, landmarks):
        points = [
            landmarks[WRIST],
            landmarks[INDEX_MCP],
            landmarks[MIDDLE_MCP],
            landmarks[RING_MCP],
            landmarks[PINKY_MCP],
        ]

        center_x = sum(point.x for point in points) / len(points)
        center_y = sum(point.y for point in points) / len(points)

        return center_x, center_y