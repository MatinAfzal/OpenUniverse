import numpy as np
import threading
from Engine2.Utils import format_vertices
from Engine2.Mesh import Mesh
from Engine2.Settings2 import *


class Chunk(Mesh):
    def __init__(self, biome="jungle", position=None, max_height=10, min_depth=-10, shematic=None, img=None,
                 material=None, is_image=False) -> None:
        """
        Chunk generator

        Args:
            biome (str): chunk type ["jungle", "desert", "snow"]
            position (pygame.Vector3): chunk center vertex position
            max_height (int): chunk maximum height
            min_depth (int): chunk minimum depth
            shematic (np.array): chunk generation sample
            img (path): texture
            material (): if material -> for loop gen

        info:
            jungle: texture
            desert: texture
            snow: texture
            superflat: texture
            image: atlas 2
            dirty: atlas 1
        """

        self.known_biomes = ["jungle", "desert", "snow", "superflat", "image", "dirty"]
        self.biome = biome
        self.chunk_center = position  # for distance culling
        self.level_name = "chunk"
        self.material = material
        self.texture = img
        self.position = position
        self.chunk_id = f"{self.position.x}:{self.position.y}:{self.position.z}:{self.biome}:{VERSION}"
        self.load_status = True
        self.index_key = 0
        if material:
            self.shematic = np.round(shematic).astype(int)
        else:
            self.shematic = shematic
        self.shematic_shape = shematic.shape
        self.image = img
        self.vertices = None
        self.lines = None
        self.triangles = None
        self.colors = []
        self.translation = self.position
        self.max = max_height
        self.min = -min_depth
        self.height = self.max + (self.min * -1)
        self.left = 8
        self.right = 8
        self.area = self.left * self.right * self.height
        self.uvs_face = []
        self.blocks = 0
        
        # Texture atlas locations
        self.atlas_length = 15.9999991
        self.atlas_height = 15.9999991
        self.HM_F = 0  # Horizontal Multiplier to first border
        self.HM_L = 1  # Horizontal Multiplier to last border
        self.VM_F = 0  # Vertical Multiplier to first border
        self.VM_L = 1  # Vertical Multiplier to last border
        self.BD = 0.0000099  # border_deficiency
        self.ONE = 1 - self.BD

        if self.biome in self.known_biomes:
            self.vertices, self.triangles, uvs, uvs_ind, normals, normals_ind = self.level_maker(self.position)
        else:
            if ESP:
                print("Biome not found!")

        # Linear processing (3 seconds in 30x30, Multiprocessing is 4 seconds)
        self.vertices = format_vertices(self.vertices, self.triangles)
        self.vertex_uvs = format_vertices(uvs, uvs_ind)
        self.normals = format_vertices(normals, normals_ind)

        if self.material:
            for _ in range(len(self.vertices * 3)):
                self.colors.append(CHUNK_COLOR_R)
                self.colors.append(CHUNK_COLOR_G)
                self.colors.append(CHUNK_COLOR_B)

            super().__init__(
                vertices=self.vertices,
                imagefile=self.texture,
                vertex_normals=self.normals,
                vertex_uvs=self.vertex_uvs,
                vertex_colors=self.colors,
                material=self.material,
                esp_off=True
            )

    def level_maker(self, center):
        """
        Chunk level maker
        
        Args:
            center (pygame.Vector3): chunk center position

        Sample:
               a   b   c   d   e   f   g   h    \n
            0 [a0, b0, c0, d0, e0, f0, g0, h0]  \n
            1 [a1, b1, c1, d1, e1, f1, g1, h1]  \n
            2 [a2, b2, c2, d2, e2, f2, g2, h2]  \n
            3 [a3, b3, c3, d3, e3, f3, g3, h3]  \n
            4 [a4, b4, c4, d4, e4, f4, g4, h4]  \n
            5 [a5, b5, c5, d5, e5, f5, g5, h5]  \n
            6 [a6, b6, c6, d6, e6, f6, g6, h6]  \n
            7 [a7, b7, c7, d7, e7, f7, g7, h7]  \n
            
        Center:
               d   e   \n
            3 [d3, e3] \n
            4 [d4, e4] \n
            
        Block:
            [TLU, TRU] \n
            [TLD, TRD] \n
            |        | \n
            [BLU, BRU] \n
            [BLD, BRD] \n
            
        Block faces:
            ## U Face [UF] \n
            ## F Face [FF] , B Face [BF], L Face [LF], R Face [RF]\n
            ## D Face [DF] \n
        
        (LENGTH, HEIGHT)
        """
        
        # ROWS
        rs = {
            0: (4, 3),
            1: (3, 2),
            2: (2, 1),
            3: (1, 0),
            4: (0, -1),
            5: (-1, -2),
            6: (-2, -3),
            7: (-3, -4)
        }
        
        # COLUMNS
        cs = {
            0: (4, 3),
            1: (3, 2),
            2: (2, 1),
            3: (1, 0),
            4: (0, -1),
            5: (-1, -2),
            6: (-2, -3),
            7: (-3, -4)
        }
        
        # TRIANGLES
        tr = {
            1: (0, 1, 2),
            2: (2, 1, 3),
            3: (2, 3, 4),
            4: (4, 3, 5),
            5: (4, 5, 6),
            6: (6, 5, 7),
            7: (6, 7, 0),
            8: (0, 7, 1),
            9: (1, 7, 3),
            10: (3, 7, 5),
            11: (6, 0, 4),
            12: (4, 0, 2)
        }
        
        level_vertices = []
        level_triangles = []
        level_uvs = []
        level_uvs_ind = []

        normals = [(0.0, 0.0, 1.0), (0.0, 0.0, 1.0), (0.0, 0.0, 1.0),
                   (0.0, 0.0, 1.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0),
                   (0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, -1.0),
                   (0.0, 0.0, -1.0), (0.0, 0.0, -1.0), (0.0, 0.0, -1.0),
                   (0.0, -1.0, 0.0), (0.0, -1.0, 0.0), (0.0, -1.0, 0.0),
                   (0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (1.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0), (1.0, 0.0, 0.0), (-1.0, 0.0, 0.0),
                   (-1.0, 0.0, 0.0), (-1.0, 0.0, 0.0), (-1.0, 0.0, 0.0)]

        level_normals = []
        level_normals_ind = []
        triangle_counter = 0
        uv_counter = 0
        normal_counter = 0
        dirt = False
        _map = {
            "DIRT_X": (2, 3, 1, 2),  # HF/HL/LF/LL
            "DIRT_Z": (2, 3, 1, 2),
            "DIRT_Y": (2, 3, 0, 1)
        }

        for ROW in range(0, self.shematic_shape[0]):  # Z
            for COLUMN in range(0, self.shematic_shape[1]):  # X
                if self.biome == "superflat":
                    temp = 1
                    n_temp = 0
                elif self.biome == "image":
                    temp = 1
                    n_temp = 0
                    block_map = self.shematic[COLUMN][ROW]
                else:  # Normal terrain
                    temp = int(self.shematic[COLUMN][ROW]) + 1
                    n_temp = temp - WORLD_DEPTH

                for DEPTH in range(n_temp, temp):  # Y
                    self.blocks += 1
                    if DEPTH <= -5:
                        if self.biome == "jungle":  # Jungle sand
                            self.HM_F = 0
                            self.HM_L = 1
                            self.VM_F = 2
                            self.VM_L = 3
                        elif self.biome == "desert":
                            self.HM_F = 0
                            self.HM_L = 1
                            self.VM_F = 2
                            self.VM_L = 3
                        elif self.biome == "snow":  # Snow pure snow
                            self.HM_F = 15
                            self.HM_L = 16
                            self.VM_F = 15
                            self.VM_L = 16
                        elif self.biome == "dirty": # dirty dirt
                            self.HM_F = 3
                            self.HM_L = 4
                            self.VM_F = 6
                            self.VM_L = 7
                    elif -4 <= DEPTH < 0:
                        if self.biome == "jungle":  # Jungle dirt
                            # dirt = True
                            self.HM_F = 0
                            self.HM_L = 1
                            self.VM_F = 1
                            self.VM_L = 2
                        elif self.biome == "desert":
                            self.HM_F = 5
                            self.HM_L = 6
                            self.VM_F = 15
                            self.VM_L = 16
                        elif self.biome == "snow":  # Snow pure snow
                            self.HM_F = 15
                            self.HM_L = 16
                            self.VM_F = 15
                            self.VM_L = 16
                    elif 0 <= DEPTH < 15:
                        if self.biome == "jungle":  # Jungle grass
                            self.HM_F = 9
                            self.HM_L = 10
                            self.VM_F = 15
                            self.VM_L = 16
                        elif self.biome == "desert":
                            self.HM_F = 0
                            self.HM_L = 1
                            self.VM_F = 1
                            self.VM_L = 2
                        elif self.biome == "snow":  # Snow ice
                            self.HM_F = 1
                            self.HM_L = 2
                            self.VM_F = 14
                            self.VM_L = 15
                        elif self.biome == "superflat":  # Jungle grass
                            self.HM_F = 9
                            self.HM_L = 10
                            self.VM_F = 15
                            self.VM_L = 16
                        elif self.biome == "image" and block_map <= 40:  # Black wool in Atlas 2
                            self.HM_F = 3
                            self.HM_L = 4
                            self.VM_F = 13
                            self.VM_L = 14
                        elif self.biome == "image" and 120 >= block_map > 40:  # Dark gray wool in Atlas 2
                            self.HM_F = 8
                            self.HM_L = 9
                            self.VM_F = 13
                            self.VM_L = 14
                        elif self.biome == "image" and 120 < block_map > 200:  # Gray wool in Atlas 2
                            self.HM_F = 10
                            self.HM_L = 11
                            self.VM_F = 13
                            self.VM_L = 14
                        elif self.biome == "image" and block_map <= 255:  # White wool in Atlas 2
                            self.HM_F = 3
                            self.HM_L = 4
                            self.VM_F = 12
                            self.VM_L = 13
                        elif self.biome == "dirty":  # dirty grass
                            self.HM_F = 1
                            self.HM_L = 2
                            self.VM_F = 10
                            self.VM_L = 11
                    elif DEPTH >= 15:
                        if self.biome == "jungle":  # Jungle snow
                            self.HM_F = 0
                            self.HM_L = 1
                            self.VM_F = 14
                            self.VM_L = 15
                    else:
                        print(f"ERROR: Unidentified block detected... ZXY:{ROW}/{COLUMN}/{DEPTH}")

                    # Check for neighbors (Face culling)
                    n_top = False
                    n_bot = False
                    n_front = False
                    n_back = False
                    n_right = False
                    n_left = False
                    lock = True

                    if COLUMN == 7 or COLUMN == 0:
                        # TODO: Chunk edge
                        lock = False
                    if ROW == 7 or ROW == 0:
                        # TODO: Chunk edge
                        lock = False
                    if lock:
                        if temp-1 != DEPTH:
                            n_top = True
                        if self.shematic[COLUMN][ROW] > DEPTH:
                            n_bot = True
                        if self.shematic[COLUMN][ROW - 1] >= DEPTH:
                            n_back = True
                        if self.shematic[COLUMN][ROW + 1] >= DEPTH:
                            n_front = True
                        if self.shematic[COLUMN - 1][ROW] >= DEPTH:
                            n_right = True
                        if self.shematic[COLUMN + 1][ROW] >= DEPTH:
                            n_left = True

                    if n_front and n_back and n_left and n_right and n_top and n_bot:  # It's a hidden block
                        continue

                    available_faces = [n_front, n_back, n_left, n_right, n_top, n_bot]

                    # Top vertices
                    TLU = (center.x - cs.get(COLUMN)[0], DEPTH, center.z - rs.get(ROW)[0])
                    TLD = (center.x - cs.get(COLUMN)[0], DEPTH, center.z - rs.get(ROW)[1])
                    TRU = (center.x - cs.get(COLUMN)[1], DEPTH, center.z - rs.get(ROW)[0])
                    TRD = (center.x - cs.get(COLUMN)[1], DEPTH, center.z - rs.get(ROW)[1])

                    # Bottom vertices
                    BLU = (center.x - cs.get(COLUMN)[0], DEPTH - 1, center.z - rs.get(ROW)[0])
                    BLD = (center.x - cs.get(COLUMN)[0], DEPTH - 1, center.z - rs.get(ROW)[1])
                    BRU = (center.x - cs.get(COLUMN)[1], DEPTH - 1, center.z - rs.get(ROW)[0])
                    BRD = (center.x - cs.get(COLUMN)[1], DEPTH - 1, center.z - rs.get(ROW)[1])

                    # Mesh triangles
                    level_vertices.extend([TLU, TLD, TRU, TRD, BLU, BLD, BRU, BRD])

                    triangle = self.triangle_face_cull(available_faces, triangle_counter)
                    level_triangles.extend(triangle)

                    # UV vertices
                    if dirt:
                        self.update_uvs_face_dirt(_map)
                    else:
                        self.update_uvs_face()

                    for i in range(24):
                        level_uvs.append(self.uvs_face[i])

                    # UV triangles
                    uvs_ind = self.uvs_face_cull(available_faces, uv_counter)
                    level_uvs_ind.extend(uvs_ind)

                    triangle_counter += 1
                    uv_counter += 1
                    dirt = False

                    # Normals
                    for i in range(24):
                        level_normals.append(normals[i])

                    normals_ind = self.normal_face_cull(available_faces, normal_counter)
                    level_normals_ind.extend(normals_ind)

                    normal_counter += 1

        return level_vertices, level_triangles, level_uvs, level_uvs_ind, level_normals, level_normals_ind

    def update_uvs_face(self):
        self.uvs_face = [
            (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L),
            (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F), 
            (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F), 
            (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L), 
            (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L), 
            (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F), 
            (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F), 
            (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L)
        ]

    def update_uvs_face_dirt(self, _map):
        self.uvs_face = [
            (self.ONE / self.atlas_length * _map.get("DIRT_X")[2], self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * _map.get("DIRT_X")[3], self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * _map.get("DIRT_X")[2], self.ONE / self.atlas_height * self.VM_L),  # -X
            (self.ONE / self.atlas_length * _map.get("DIRT_X")[3], self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * _map.get("DIRT_X")[2], self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * _map.get("DIRT_X")[3], self.ONE / self.atlas_height * self.VM_F),  # -X
            (self.ONE / self.atlas_length * _map.get("DIRT_Z")[2], self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * _map.get("DIRT_Z")[3], self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * _map.get("DIRT_Z")[2], self.ONE / self.atlas_height * self.VM_F),  # +Z
            (self.ONE / self.atlas_length * _map.get("DIRT_Z")[3], self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * _map.get("DIRT_Z")[2], self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * _map.get("DIRT_Z")[3], self.ONE / self.atlas_height * self.VM_L),  # +Z
            (self.ONE / self.atlas_length * _map.get("DIRT_X")[2], self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * _map.get("DIRT_X")[3], self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * _map.get("DIRT_X")[2], self.ONE / self.atlas_height * self.VM_L),  # +X
            (self.ONE / self.atlas_length * _map.get("DIRT_X")[3], self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * _map.get("DIRT_X")[2], self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * _map.get("DIRT_X")[3], self.ONE / self.atlas_height * self.VM_F),  # +X
            (self.ONE / self.atlas_length * _map.get("DIRT_Y")[2], self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * _map.get("DIRT_Y")[3], self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * _map.get("DIRT_Y")[2], self.ONE / self.atlas_height * self.VM_F),  # +Y / H -Z
            (self.ONE / self.atlas_length * _map.get("DIRT_Y")[3], self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * _map.get("DIRT_Y")[2], self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * _map.get("DIRT_Y")[3], self.ONE / self.atlas_height * self.VM_L)  # +Y / H -Z
        ]

    @staticmethod
    def triangle_face_cull(available_faces: list, triangle_counter: int):
        """
        front, back, right, left
        """
        temp = []

        if not available_faces[4]:  # top face triangles
            temp.extend(
                [0 + 8 * triangle_counter, 1 + 8 * triangle_counter, 2 + 8 * triangle_counter,  # TOP 1
                 2 + 8 * triangle_counter, 1 + 8 * triangle_counter, 3 + 8 * triangle_counter]  # TOP 2
            )

        if not available_faces[5]:  # bottom face triangles
            temp.extend(
                [4 + 8 * triangle_counter, 5 + 8 * triangle_counter, 6 + 8 * triangle_counter,  # BOT 1
                 6 + 8 * triangle_counter, 5 + 8 * triangle_counter, 7 + 8 * triangle_counter])  # BOT 2

        if not available_faces[0]:  # front face triangles
            temp.extend(
                        [1 + 8 * triangle_counter, 5 + 8 * triangle_counter, 3 + 8 * triangle_counter,
                         3 + 8 * triangle_counter, 5 + 8 * triangle_counter, 7 + 8 * triangle_counter]
            )
        if not available_faces[1]:  # Back face triangles
            temp.extend(
                        [0 + 8 * triangle_counter, 4 + 8 * triangle_counter, 2 + 8 * triangle_counter,
                         2 + 8 * triangle_counter, 4 + 8 * triangle_counter, 6 + 8 * triangle_counter]
            )
        if not available_faces[2]:  # Right face triangles
            temp.extend(
                        [6 + 8 * triangle_counter, 2 + 8 * triangle_counter, 7 + 8 * triangle_counter,
                         7 + 8 * triangle_counter, 2 + 8 * triangle_counter, 3 + 8 * triangle_counter]
            )
        if not available_faces[3]:  # Left face triangles
            temp.extend(
                        [4 + 8 * triangle_counter, 0 + 8 * triangle_counter, 5 + 8 * triangle_counter,
                         5 + 8 * triangle_counter, 0 + 8 * triangle_counter, 1 + 8 * triangle_counter]
            )

        return temp

    @staticmethod
    def uvs_face_cull(available_faces: list, uv_counter: int):
        temp = []

        if not available_faces[4]:  # top face triangles
            temp.extend(
                [20 + 24 * uv_counter, 21 + 24 * uv_counter, 22 + 24 * uv_counter,  # TOP 1
                 22 + 24 * uv_counter, 21 + 24 * uv_counter, 23 + 24 * uv_counter])  # TOP 2

        if not available_faces[5]:  # bottom face triangles
            temp.extend(
                [4 + 24 * uv_counter, 5 + 24 * uv_counter, 6 + 24 * uv_counter,  # BOT 1
                 6 + 24 * uv_counter, 5 + 24 * uv_counter, 7 + 24 * uv_counter])  # BOT 2

        if not available_faces[0]:  # front face triangles
            temp.extend(
                [8 + 24 * uv_counter, 9 + 24 * uv_counter, 10 + 24 * uv_counter,
                 10 + 24 * uv_counter, 9 + 24 * uv_counter, 11 + 24 * uv_counter]
            )
        if not available_faces[1]:  # Back face triangles
            temp.extend(
                [16 + 24 * uv_counter, 17 + 24 * uv_counter, 18 + 24 * uv_counter,
                 18 + 24 * uv_counter, 17 + 24 * uv_counter, 19 + 24 * uv_counter]
            )
        if not available_faces[2]:  # Right face triangles
            temp.extend(
                [12 + 24 * uv_counter, 13 + 24 * uv_counter, 14 + 24 * uv_counter,
                 14 + 24 * uv_counter, 13 + 24 * uv_counter, 15 + 24 * uv_counter]
            )
        if not available_faces[3]:  # Left face triangles
            temp.extend(
                [0 + 24 * uv_counter, 1 + 24 * uv_counter, 2 + 24 * uv_counter,
                 2 + 24 * uv_counter, 1 + 24 * uv_counter, 3 + 24 * uv_counter]
            )

        return temp

    @staticmethod
    def normal_face_cull(available_faces: list, normal_counter: int):
        temp = []

        if not available_faces[4]:  # top face triangles
            temp.extend([0 + 24 * normal_counter, 1 + 24 * normal_counter, 2 + 24 * normal_counter,  # TOP 1
                        2 + 24 * normal_counter, 1 + 24 * normal_counter, 3 + 24 * normal_counter])  # TOP 2

        if not available_faces[5]:  # bottom face triangles
            temp.extend(
                [4 + 24 * normal_counter, 5 + 24 * normal_counter, 6 + 24 * normal_counter,  # BOT 1
                 6 + 24 * normal_counter, 5 + 24 * normal_counter, 7 + 24 * normal_counter])  # BOT 2

        if not available_faces[0]:  # front face triangles
            temp.extend(
                        [8 + 24 * normal_counter, 9 + 24 * normal_counter, 10 + 24 * normal_counter,
                         10 + 24 * normal_counter, 9 + 24 * normal_counter, 11 + 24 * normal_counter]
            )
        if not available_faces[1]:  # Back face triangles
            temp.extend(
                        [12 + 24 * normal_counter, 13 + 24 * normal_counter, 14 + 24 * normal_counter,
                         14 + 24 * normal_counter, 13 + 24 * normal_counter, 15 + 24 * normal_counter]
            )
        if not available_faces[2]:  # Right face triangles
            temp.extend(
                        [20 + 24 * normal_counter, 21 + 24 * normal_counter, 22 + 24 * normal_counter,
                         22 + 24 * normal_counter, 21 + 24 * normal_counter, 23 + 24 * normal_counter]
            )
        if not available_faces[3]:  # Left face triangles
            temp.extend(
                        [16 + 24 * normal_counter, 17 + 24 * normal_counter, 18 + 24 * normal_counter,
                         18 + 24 * normal_counter, 17 + 24 * normal_counter, 19 + 24 * normal_counter]
            )

        return temp
