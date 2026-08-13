from app.gestures.thumb import (
    is_left_thumb,
    is_right_thumb,
)


class Point:
    def __init__(self, x, y, z=0.0):
        self.x = x
        self.y = y
        self.z = z


landmarks = [
    Point(0.0, 0.0, 0.0)
    for _ in range(21)
]


# Thumb landmarks
landmarks[1] = Point(0.30, 0.50, 0.0)  # THUMB_CMC
landmarks[2] = Point(0.35, 0.50, 0.0)  # THUMB_MCP
landmarks[3] = Point(0.45, 0.50, 0.0)  # THUMB_IP
landmarks[4] = Point(0.55, 0.50, 0.0)  # THUMB_TIP


print(
    "Left thumb:",
    is_left_thumb(landmarks, "Left")
)

print(
    "Right thumb:",
    is_right_thumb(landmarks, "Right")
)

print(
    "Left thumb detected as right:",
    is_right_thumb(landmarks, "Left")
)