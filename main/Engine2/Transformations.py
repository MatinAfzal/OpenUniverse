# This file performs matrix transformations (translating, rotating, scaling)
# Reduced code duplication: The scale_mat function has been modified to handle scaling with one or three parameters. 
# Additionally, the apply_transform function was created to eliminate code repetition when combining matrices (local and global).
# Improved readability: Function and variable names have been simplified and made more logical, and parts of the code have been 
# refactored into more general and reusable functions.
# Better efficiency: np.eye is used for generating the identity matrix, which is more efficient and faster than manually creating the matrix.

import numpy as np
from math import cos, sin, radians

class Rotation:
    "Rotation angle & axis"
    def __init__(self, angle, axis):
        self.angle = angle
        self.axis = axis

def identity_mat() -> np.ndarray:
    return np.eye(4, dtype=np.float32)

def translate_mat(x, y, z) -> np.ndarray:
    mat = identity_mat()
    mat[:3, 3] = [x, y, z]
    return mat

def scale_mat(sx, sy=None, sz=None) -> np.ndarray:
    if sy is None: sy = sx
    if sz is None: sz = sx
    return np.diag([sx, sy, sz, 1]).astype(np.float32)

def rotate_x_mat(angle) -> np.ndarray:
    c, s = cos(radians(angle)), sin(radians(angle))
    return np.array([[1, 0, 0, 0],
                     [0, c, -s, 0],
                     [0, s, c, 0],
                     [0, 0, 0, 1]], np.float32)

def rotate_y_mat(angle) -> np.ndarray:
    c, s = cos(radians(angle)), sin(radians(angle))
    return np.array([[c, 0, s, 0],
                     [0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [0, 0, 0, 1]], np.float32)

def rotate_z_mat(angle) -> np.ndarray:
    c, s = cos(radians(angle)), sin(radians(angle))
    return np.array([[c, -s, 0, 0],
                     [s, c, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]], np.float32)

def rotate_axis_mat(angle, axis) -> np.ndarray:
    c, s = cos(radians(angle)), sin(radians(angle))
    axis = axis.normalize()
    ux, uy, uz = axis.x, axis.y, axis.z
    return np.array([[c + (1-c)*ux*ux, (1-c)*ux*uy - s*uz, (1-c)*ux*uz + s*uy, 0],
                     [(1-c)*uy*ux + s*uz, c + (1-c)*uy*uy, (1-c)*uy*uz - s*ux, 0],
                     [(1-c)*uz*ux - s*uy, (1-c)*uz*uy + s*ux, c + (1-c)*uz*uz, 0],
                     [0, 0, 0, 1]], np.float32)

def apply_transform(matrix, transform, local=True):
    return matrix @ transform if local else transform @ matrix

def translate(matrix, x, y, z):
    return apply_transform(matrix, translate_mat(x, y, z))

def scale(matrix, sx, sy=None, sz=None):
    return apply_transform(matrix, scale_mat(sx, sy, sz))

def rotate(matrix, angle, axis, local=True):
    if axis == "X":
        return apply_transform(matrix, rotate_x_mat(angle), local)
    elif axis == "Y":
        return apply_transform(matrix, rotate_y_mat(angle), local)
    elif axis == "Z":
        return apply_transform(matrix, rotate_z_mat(angle), local)

def rotateA(matrix, angle, axis, local=True):
    return apply_transform(matrix, rotate_axis_mat(angle, axis), local)
