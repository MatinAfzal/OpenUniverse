import numpy as np
import pygame
from math import sqrt
from Engine2.Settings2 import *


class DistanceCulling:
    def __init__(self, distance=13, camera=None) -> None:
        self.block_distance = distance
        self.chunk_distance = self.block_distance * 8
        self.maximum_distance = 14
        self.player_location = [0, 0]
        self.camera = camera
        self.camera_init_pos = pygame.Vector3(int(self.camera.transformation[0, 3]),
                                              int(self.camera.transformation[1, 3]),
                                              int(self.camera.transformation[2, 3]))

        self.camera_change_val = self.camera_init_pos.copy()

    def chunk_in_distance(self, camera, chunk=None, chunk_x=None, chunk_z=None, chunk_y=None):
        x = camera.transformation[0, 3]
        y = camera.transformation[1, 3]
        z = camera.transformation[2, 3]

        if chunk:
            d = sqrt(((x - chunk.chunk_center.x)**2) + ((y - chunk.chunk_center.y)**2) +
                     ((z - chunk.chunk_center.z)**2))
        elif None not in (chunk_x, chunk_z, chunk_y):
            d = sqrt(((x - chunk_x)**2) + ((y - chunk_y)**2) +
                     ((z - chunk_z)**2))
        else:
            if ESP:
                print("Distance Culling Error: chunk_in_distance object is None!")
            return 0

        if d > self.chunk_distance:
            return False
        return True

    def camera_change_distance(self, camera, distance=8):
        x = int(camera.transformation[0, 3])
        y = int(camera.transformation[1, 3])
        z = int(camera.transformation[2, 3])

        d = abs(sqrt(((x - self.camera_change_val.x) ** 2) + ((y - self.camera_change_val.y) ** 2) +
                     ((z - self.camera_change_val.z) ** 2)))

        if d > distance:
            self.camera_change_val = pygame.Vector3(x, y, z)
            return True
        return False

    def find_new_coordinates(self, unloaded_chunk, new_camera):
        moved_direction = self.direction_calculator(self.camera_init_pos, new_camera)
        new_coord = self.coordinates_calculator(unloaded_chunk, moved_direction)
        return new_coord
        
    def direction_calculator(self, A, B):
        """ calculating movement direction.

        Args:
            A (pygame.Vector3): old location of camera
            B (pygame.Vector3): new loacton of camera (after chunk delete)

        Formola:
            link: [https://math.stackexchange.com/questions/1086104/get-directional-vector-from-point-a-to-point-b]
            the vector pointing in the direction from point A to point B is BA→=OB→−OA→.
        """
        try:
            vector = A - B
            direction_vector = vector.normalize()
            # direction_vector = vector
            direction = None

            # N
            if int(direction_vector.x) == 0 and direction_vector.z < 0:
                direction = "N"

            # S
            elif int(direction_vector.x) == 0 and direction_vector.z > 0:
                direction = "S"

            # E
            elif direction_vector.x > 0 and int(direction_vector.z) == 0:
                direction = "E"

            # W
            elif direction_vector.x < 0 and int(direction_vector.z) == 0:
                direction = "W"

            # NE
            elif direction_vector.x > 0 and direction_vector.z < 0:
                direction = "NE"

            # NW
            elif direction_vector.x < 0 and direction_vector.z < 0:
                direction = "NW"

            # SE
            elif direction_vector.x > 0 and direction_vector.z > 0:
                direction = "SE"

            # SW
            elif direction_vector.x < 0 and direction_vector.z > 0:
                direction = "SW"

            return direction

        except Exception as Error:
            if ESP:
                print("ERROR: direction vector calculating faild...")
                print(Error)

    def coordinates_calculator(self, unloaded_chunk, direction):
        """ calculating the coordinates of new chunk.

        Args:
            direction (str): player new direction

        Sample:
            note! cam: player location
            [NW, N, NE]
            [W, CAM, E]
            [SW, S, SE]
            "N" : North
            "S" : South
            "E" : East
            "W" : West
            "NE" : Northeast
            "NW" : Northwest
            "SE" : Southeast
            "SW" : Southwest
        """
        x = None
        z = None
        coordinates = None
        # if direction == "N":
        #     x = unloaded_chunk.chunk_center.x
        #     z = unloaded_chunk.chunk_center.z - self.chunk_distance - 1
        #
        # elif direction == "S":
        #     x = unloaded_chunk.chunk_center.x
        #     z = unloaded_chunk.chunk_center.z + self.chunk_distance + 1
        #
        # elif direction == "E":
        #     x = unloaded_chunk.chunk_center.x + self.chunk_distance + 1
        #     z = unloaded_chunk.chunk_center.z
        #
        # elif direction == "W":
        #     x = unloaded_chunk.chunk_center.x - self.chunk_distance - 1
        #     z = unloaded_chunk.chunk_center.z
        #
        # elif direction == "NE":
        #     x = unloaded_chunk.chunk_center.x + self.chunk_distance + 1
        #     z = unloaded_chunk.chunk_center.z - self.chunk_distance + 1
        #
        # elif direction == "NW":
        #     x = unloaded_chunk.chunk_center.x - self.chunk_distance - 1
        #     z = unloaded_chunk.chunk_center.z - self.chunk_distance - 1
        #
        # elif direction == "SE":
        #     x = unloaded_chunk.chunk_center.x + self.chunk_distance + 1
        #     z = unloaded_chunk.chunk_center.z + self.chunk_distance + 1
        #
        # elif direction == "SW":
        #     x = unloaded_chunk.chunk_center.x - self.chunk_distance - 1
        #     z = unloaded_chunk.chunk_center.z + self.chunk_distance + 1
        if direction == "N":
            x = unloaded_chunk.chunk_center.x
            z = unloaded_chunk.chunk_center.z + self.chunk_distance

        elif direction == "S":
            x = unloaded_chunk.chunk_center.x
            z = unloaded_chunk.chunk_center.z - self.chunk_distance

        elif direction == "E":
            x = unloaded_chunk.chunk_center.x - self.chunk_distance
            z = unloaded_chunk.chunk_center.z

        elif direction == "W":
            x = unloaded_chunk.chunk_center.x + self.chunk_distance
            z = unloaded_chunk.chunk_center.z

        elif direction == "NE":
            x = unloaded_chunk.chunk_center.x - self.chunk_distance
            z = unloaded_chunk.chunk_center.z + self.chunk_distance

        elif direction == "NW":
            x = unloaded_chunk.chunk_center.x + self.chunk_distance
            z = unloaded_chunk.chunk_center.z + self.chunk_distance

        elif direction == "SE":
            x = unloaded_chunk.chunk_center.x - self.chunk_distance
            z = unloaded_chunk.chunk_center.z - self.chunk_distance

        elif direction == "SW":
            x = unloaded_chunk.chunk_center.x + self.chunk_distance
            z = unloaded_chunk.chunk_center.z - self.chunk_distance

        else:
            coordinates = pygame.Vector3(0, 30, 0)

        if x and z:
            coordinates = pygame.Vector3(x, 0, z)

        return coordinates

# if __name__ == "__main__":
#     temp = DistanceCulling()
#     temp.direction_calculator(pygame.Vector3(3, 0, 7), pygame.Vector3(7, 0, 3))
