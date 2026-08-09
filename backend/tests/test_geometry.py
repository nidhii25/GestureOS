from app.vision.landmark_processor import LandmarkPoint
from app.vision.geometry import distance, angle_between_points


point_a = LandmarkPoint(0.0, 0.0, 0.0)
point_b = LandmarkPoint(3.0, 4.0, 0.0)

print("Distance:", distance(point_a, point_b))


point_c = LandmarkPoint(0.0, 0.0, 0.0)
point_d = LandmarkPoint(1.0, 0.0, 0.0)
point_e = LandmarkPoint(1.0, 1.0, 0.0)

print(
    "Angle:",
    angle_between_points(point_c, point_d, point_e)
)