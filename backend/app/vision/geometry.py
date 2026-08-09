from math import sqrt, acos


def distance(point1, point2):
    return sqrt(
        (point2.x - point1.x) ** 2
        + (point2.y - point1.y) ** 2
        + (point2.z - point1.z) ** 2
    )


def angle_between_points(point1, point2, point3):
    vector1 = (
        point1.x - point2.x,
        point1.y - point2.y,
        point1.z - point2.z,
    )

    vector2 = (
        point3.x - point2.x,
        point3.y - point2.y,
        point3.z - point2.z,
    )

    dot_product = (
        vector1[0] * vector2[0]
        + vector1[1] * vector2[1]
        + vector1[2] * vector2[2]
    )

    magnitude1 = sqrt(
        vector1[0] ** 2
        + vector1[1] ** 2
        + vector1[2] ** 2
    )

    magnitude2 = sqrt(
        vector2[0] ** 2
        + vector2[1] ** 2
        + vector2[2] ** 2
    )

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    cosine_angle = dot_product / (magnitude1 * magnitude2)

    # Prevent floating-point errors from producing
    # values slightly outside the valid acos range.
    cosine_angle = max(-1.0, min(1.0, cosine_angle))

    return acos(cosine_angle)