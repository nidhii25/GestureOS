from app.gestures.pinch import is_pinching


class Point:
    def __init__(self, x, y, z=0.0):
        self.x = x
        self.y = y
        self.z = z


landmarks = [
    Point(0.0, 0.0, 0.0)
    for _ in range(21)
]


# Thumb tip = landmark 4
landmarks[4] = Point(0.50, 0.50, 0.0)

# Index tip = landmark 8
landmarks[8] = Point(0.51, 0.51, 0.0)


print("Pinch:", is_pinching(landmarks))


# Move index finger away
landmarks[8] = Point(0.80, 0.80, 0.0)

print(
    "Pinch after moving index away:",
    is_pinching(landmarks)
)