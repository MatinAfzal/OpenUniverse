import numpy as np
from math import radians, cos, sin


class Rotation:
    """Represents a rotation defined by an angle and an axis."""

    def __init__(self, angle, axis):
        self.angle = angle
        self.axis = axis


def identity_mat() -> np.ndarray:
    """Creates a 4x4 identity matrix."""
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]], np.float32)


def translate_mat(x, y, z) -> np.ndarray:
    """Creates a translation matrix for the specified x, y, and z offsets."""
    return np.array([[1, 0, 0, x],
                     [0, 1, 0, y],
                     [0, 0, 1, z],
                     [0, 0, 0, 1]], np.float32)


def scale_mat(s) -> np.ndarray:
    """Creates a uniform scaling matrix with the specified scale factor."""
    return np.array([[s, 0, 0, 0],
                     [0, s, 0, 0],
                     [0, 0, s, 0],
                     [0, 0, 0, 1]], np.float32)


def scale_mat3(sx, sy, sz) -> np.ndarray:
    """Creates a scaling matrix with different scale factors for each axis."""
    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]], np.float32)


def rotate_x_mat(angle) -> np.ndarray:
    """Creates a rotation matrix for a rotation around the x-axis."""
    c = cos(radians(angle))
    s = sin(radians(angle))
    return np.array([[1, 0, 0, 0],
                     [0, c, -s, 0],
                     [0, s, c, 0],
                     [0, 0, 0, 1]], np.float32)


def rotate_y_mat(angle) -> np.ndarray:
    """Creates a rotation matrix for a rotation around the y-axis."""
    c = cos(radians(angle))
    s = sin(radians(angle))
    return np.array([[c, 0, s, 0],
                     [0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [0, 0, 0, 1]], np.float32)


def rotate_z_mat(angle) -> np.ndarray:
    """Creates a rotation matrix for a rotation around the z-axis."""
    c = cos(radians(angle))
    s = sin(radians(angle))
    return np.array([[c, -s, 0, 0],
                     [s, c, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]], np.float32)


def rotate_axis(angle, axis) -> np.ndarray:
    """Creates a rotation matrix for a rotation around an arbitrary axis."""
    c = cos(radians(angle))
    s = sin(radians(angle))
    axis = axis.normalize()  # Assuming `axis` has a normalize method
    ux2 = axis.x * axis.x
    uy2 = axis.y * axis.y
    uz2 = axis.z * axis.z
    return np.array(
        [[c + (1 - c) * ux2, (1 - c) * axis.y * axis.x - s * axis.z, (1 - c) * axis.z * axis.x + s * axis.y, 0],
         [(1 - c) * axis.y * axis.x + s * axis.z, c + (1 - c) * uy2, (1 - c) * axis.z * axis.y - s * axis.x, 0],
         [(1 - c) * axis.x * axis.z - s * axis.y, (1 - c) * axis.y * axis.z + s * axis.x, c + (1 - c) * uz2, 0],
         [0, 0, 0, 1]], np.float32)


def translate(matrix, x, y, z):
    """Applies translation to the given matrix by x, y, and z."""
    trans = translate_mat(x, y, z)
    return matrix @ trans


def scale(matrix, s):
    """Applies uniform scaling to the given matrix."""
    sc = scale_mat(s)
    return matrix @ sc


def scale3(matrix, x, y, z):
    """Applies scaling with different factors to the given matrix."""
    sc = scale_mat3(x, y, z)
    return matrix @ sc


def rotate(matrix, angle, axis, local=True):
    """Applies rotation to the given matrix around the specified axis."""
    rot = identity_mat()
    if axis == "X":
        rot = rotate_x_mat(angle)
    elif axis == "Y":
        rot = rotate_y_mat(angle)
    elif axis == "Z":
        rot = rotate_z_mat(angle)

    return matrix @ rot if local else rot @ matrix


def rotateA(matrix, angle, axis, local=True):
    """Applies rotation to the given matrix around an arbitrary axis."""
    rot = rotate_axis(angle, axis)
    return matrix @ rot if local else rot @ matrix
