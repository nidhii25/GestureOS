from app.vision.landmark_processor import LandmarkPoint, LandmarkProcessor


class FakeLandmark:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


processor = LandmarkProcessor()

fake_landmarks = [
    FakeLandmark(0.1, 0.2, 0.3),
    FakeLandmark(0.4, 0.5, 0.6),
]

result = processor.process_hand(fake_landmarks)

print("Number of landmarks:", len(result))
print("First landmark:", result[0])
print("Second landmark:", result[1])