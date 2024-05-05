import pygame
from math import *
from .Settings2 import *


# NEAR = settings.camera_near_plane
# FAR = settings.camera_far_plane
# # CHUNK_SIZE = 4
# # H_CHUNK_SIZE = CHUNK_SIZE // 2
# H_CHUNK_SIZE = 8
# # CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
# # CHUNK_VOL = CHUNK_AREA * CHUNK_SIZE
# CHUNK_SPHERE_RADIUS = H_CHUNK_SIZE * sqrt(3)
# FOV_DEG = 50
# V_FOV = radians(FOV_DEG)
# WIN_RES = pygame.Vector2(1000, 800)
# ASPECT_RATIO = WIN_RES.x / WIN_RES.y
# H_FOV = 2 * atan(tan(V_FOV * 0.5) * ASPECT_RATIO)  # horizontal FOV

def is_on_distance(camera, obj_pos, chunk=True, distance=10):
    # """Checks if object in camera distance

    # Args:
    #     cam_trans_matrix (np.ndarray): camera transformation matrix
    #     obj_pos (pygame.Vector3): object position x, y, z
    #     distance (int): chunks [distance * 8]. Defaults to 10.

    # Returns:
    #     bool: True if in range
    # """
    
    # diff = sqrt(
    #         (camera.transformation[0, 3] - obj_pos[0])**2 +
    #         (camera.transformation[1, 3] - obj_pos[1])**2 +
    #         (camera.transformation[2, 3] - obj_pos[2])**2
    #     )
    
    # if chunk:
    #     if diff < distance * 8:
    #         return True
    #     return False
    
    # if diff < distance * 8:
    #     return True
    # return False
    return True


def is_on_forward(camera, object):
    # camera_forward = pygame.math.Vector3(0, 0, 1)
    # camera_forward.x = camera.transformation[0, 2]
    # camera_forward.y = camera.transformation[1, 2]
    # camera_forward.z = camera.transformation[2, 2]
    # camera_forward.normalize()
    
    # # # x
    # # if round(forward.x) == object.transformation_mat[0, 2]:
    # #     return True
    
    # # # # z
    # # # if round(forward.z) == object.transformation_mat[2, 2]:
    # # #    return True

    # # # y
    # # if round(forward.y) == object.transformation_mat[1, 2]:
    # #     return True
    
    # # else:
    # #     return False
    # # print(round(forward.x), round(forward.y), round(forward.z))
    # # return True
    # sphere_vec = object.position - pygame.Vector3(camera.transformation[0, 3], camera.transformation[1, 3],
    #                                               camera.transformation[2, 3])
    
    # # # outside the NEAR and FAR planes?
    # sz = pygame.Vector3.dot(sphere_vec, camera_forward)
    # # if not (NEAR - CHUNK_SPHERE_RADIUS <= sz <= FAR + CHUNK_SPHERE_RADIUS):
    # #     return False
    # factor_y = 1.0 / cos(half_y := V_FOV * 0.5)
    # tan_y = tan(half_y)

    # factor_x = 1.0 / cos(half_x := H_FOV * 0.5)
    # tan_x = tan(half_x)
    # camera_right = pygame.Vector3.normalize(pygame.Vector3.cross(camera_forward, pygame.Vector3(0, 1, 0)))
    # camera_up = pygame.Vector3.normalize(pygame.Vector3.cross(camera_right, camera_forward))
    # sx = pygame.Vector3.dot(sphere_vec, camera_right)
    # dist = factor_x * CHUNK_SPHERE_RADIUS + sz * tan_x
    # if not (-dist <= sx <= dist):
    #     return False
    
    # # outside the TOP and BOTTOM planes?
    # sy = pygame.Vector3.dot(sphere_vec, camera_up)
    # dist = factor_y * CHUNK_SPHERE_RADIUS + sz * tan_y
    # if not (-dist <= sy <= dist):
    #     return False
    
    # return True
    return True