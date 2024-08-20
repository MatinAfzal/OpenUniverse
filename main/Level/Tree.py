from Engine2.Utils import format_vertices
from pygame import Vector3


class Tree:
    def __init__(self, position, max_height=4, min_height=0, biome="A", img=None, material=None, shematic=None) -> None:
        """
        Tree generator

        Args:
            position (pcenter_ygame.Vector3): tree center vertex position
            max_height (int): tree maximum height
            min_height (int): tree minimum depth
            biome (str): tree biome
            img (path): texture
            shematic (np.array): tree generation sample
        """

        self.level_name = "tree1"
        self.position = position
        self.max_height = max_height
        self.min_height = min_height
        self.biome = biome
        self.image = img
        self.material = material
        self.texture = img
        self.colors = []
        self.normals = None
        self.leaf_area = [4, 4]
        self.shematic = shematic
        
        self.vertices, self.triangles, uvs, uvs_ind, normals, normals_ind = self.level_maker(self.position)
        self.vertices = format_vertices(self.vertices, self.triangles)
        self.vertex_uvs = format_vertices(uvs, uvs_ind)
        self.normals = format_vertices(normals, normals_ind)
        
        for _ in range(len(self.vertices)):
            self.colors.append(1)
            self.colors.append(1)
            self.colors.append(1)

    def level_maker(self, center):
        """Tree level maker
        
        Args:
            center (pygame.Vector3): chunk center position
        
        Sample:
            [TLU, TRU] \n
            [TLD, TRD] \n
            |        | \n
            [BLU, BRU] \n
            [BLD, BRD] \n
        """

        level_vertices = []
        level_triangles = []
        level_uvs = []
        level_uvs_ind = []
        level_normals = []
        level_normals_ind = []
        separator = 0
        uv_counter = 0
        normal_counter = 0
        normals = [(0.0, 0.0, 1.0), (0.0, 0.0, 1.0), (0.0, 0.0, 1.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0),
                   (0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, -1.0), (0.0, 0.0, -1.0), (0.0, 0.0, -1.0),
                   (0.0, 0.0, -1.0), (0.0, -1.0, 0.0), (0.0, -1.0, 0.0), (0.0, -1.0, 0.0), (0.0, -1.0, 0.0),
                   (1.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 0.0, 0.0), (-1.0, 0.0, 0.0),
                   (-1.0, 0.0, 0.0), (-1.0, 0.0, 0.0), (-1.0, 0.0, 0.0)]

        center_y = int(self.shematic[3][3]) + 1
        
        # Tree base
        for _ in range(0, self.max_height):
            # Top vertices
            TLU = (center.x - 1, center_y, center.z - 1)
            TLD = (center.x - 1, center_y, center.z + 0)
            TRU = (center.x + 0, center_y, center.z - 1)
            TRD = (center.x + 0, center_y, center.z + 0)
            
            # Bottom vertices
            BLU = (center.x - 1, center_y - 1, center.z - 1)
            BLD = (center.x - 1, center_y - 1, center.z + 0)
            BRU = (center.x + 0, center_y - 1, center.z - 1)
            BRD = (center.x + 0, center_y - 1, center.z + 0)
            
            level_vertices.extend([TLU, TLD, TRU, TRD, BLU, BLD, BRU, BRD])
            level_triangles.extend([
                0 + 8 * separator, 1 + 8 * separator, 2 + 8 * separator,  # TRIANGLE 1
                2 + 8 * separator, 1 + 8 * separator, 3 + 8 * separator,  # TRIANGLE 2
                4 + 8 * separator, 5 + 8 * separator, 6 + 8 * separator,  # TRIANGLE 3
                6 + 8 * separator, 5 + 8 * separator, 7 + 8 * separator,  # TRIANGLE 4
                1 + 8 * separator, 5 + 8 * separator, 3 + 8 * separator,  # TRIANGLE 5
                3 + 8 * separator, 5 + 8 * separator, 7 + 8 * separator,  # TRIANGLE 6
                0 + 8 * separator, 4 + 8 * separator, 2 + 8 * separator,  # TRINAGLE 7
                2 + 8 * separator, 4 + 8 * separator, 6 + 8 * separator,  # TRIANGLE 8
                4 + 8 * separator, 0 + 8 * separator, 5 + 8 * separator,  # TRIANGLE 9
                5 + 8 * separator, 0 + 8 * separator, 1 + 8 * separator,  # TRIANGLE 10
                6 + 8 * separator, 2 + 8 * separator, 7 + 8 * separator,  # TRIANGLE 11
                7 + 8 * separator, 2 + 8 * separator, 3 + 8 * separator,  # TRIANGLE 12
            ])
            
            separator += 1
            center_y += 1
            
            # Texture atlas locations
            # atlas_length = 16
            # atlas_height = 16
            # HM_F = 0  # Horizontal Multiplier to first border
            # HM_L = 1  # Horizontal Multiplier to last border
            # VM_F = 8  # Vertical Multiplier to first border
            # VM_L = 9  # Vertical Multiplier to last border
            # BD = 0.0000000099  # border_deficiency
            # ONE = 1 + BD
            atlas_length = 16
            atlas_height = 16
            HM_F = 0  # Horizontal Multiplier to first border
            HM_L = 1  # Horizontal Multiplier to last border
            VM_F = 1  # Vertical Multiplier to first border
            VM_L = 2  # Vertical Multiplier to last border
            BD = 0.0000000099  # border_deficiency
            ONE = 1 + BD
            
            uvs_face = [
            (ONE / atlas_length * HM_F, ONE / atlas_height * VM_F), (ONE / atlas_length * HM_L, ONE / atlas_height * VM_F), (ONE / atlas_length * HM_F, ONE / atlas_height * VM_L),
            (ONE / atlas_length * HM_L, ONE / atlas_height * VM_L), (ONE / atlas_length * HM_F, ONE / atlas_height * VM_F), (ONE / atlas_length * HM_L, ONE / atlas_height * VM_F), 
            (ONE / atlas_length * HM_F, ONE / atlas_height * VM_L), (ONE / atlas_length * HM_L, ONE / atlas_height * VM_L), (ONE / atlas_length * HM_F, ONE / atlas_height * VM_F), 
            (ONE / atlas_length * HM_L, ONE / atlas_height * VM_F), (ONE / atlas_length * HM_F, ONE / atlas_height * VM_L), (ONE / atlas_length * HM_L, ONE / atlas_height * VM_L), 
            (ONE / atlas_length * HM_F, ONE / atlas_height * VM_F), (ONE / atlas_length * HM_L, ONE / atlas_height * VM_F), (ONE / atlas_length * HM_F, ONE / atlas_height * VM_L), 
            (ONE / atlas_length * HM_L, ONE / atlas_height * VM_L), (ONE / atlas_length * HM_F, ONE / atlas_height * VM_F), (ONE / atlas_length * HM_L, ONE / atlas_height * VM_F), 
            (ONE / atlas_length * HM_F, ONE / atlas_height * VM_L), (ONE / atlas_length * HM_L, ONE / atlas_height * VM_L), (ONE / atlas_length * HM_F, ONE / atlas_height * VM_F), 
            (ONE / atlas_length * HM_L, ONE / atlas_height * VM_F), (ONE / atlas_length * HM_F, ONE / atlas_height * VM_L), (ONE / atlas_length * HM_L, ONE / atlas_height * VM_L)
            ]
            
            # UV vertices
            for i in range(24):
                level_uvs.append(uvs_face[i])
            
            # UV triangles
            level_uvs_ind.extend([
                20 + 24 * uv_counter, 21 + 24 * uv_counter, 22 + 24 * uv_counter,  # TRIANGLE 1
                22 + 24 * uv_counter, 21 + 24 * uv_counter, 23 + 24 * uv_counter,  # TRIANGLE 2
                4 + 24 * uv_counter, 5 + 24 * uv_counter, 6 + 24 * uv_counter,  # TRIANGLE 3
                6 + 24 * uv_counter, 5 + 24 * uv_counter, 7 + 24 * uv_counter,  # TRIANGLE 4
                8 + 24 * uv_counter, 9 + 24 * uv_counter, 10 + 24 * uv_counter,  # TRIANGLE 5
                10 + 24 * uv_counter, 9 + 24 * uv_counter, 11 + 24 * uv_counter,  # TRIANGLE 6
                16 + 24 * uv_counter, 17 + 24 * uv_counter, 18 + 24 * uv_counter,  # TRIANGLE 7
                18 + 24 * uv_counter, 17 + 24 * uv_counter, 19 + 24 * uv_counter,  # TRIANGLE 8
                0 + 24 * uv_counter, 1 + 24 * uv_counter, 2 + 24 * uv_counter,  # TRIANGLE 9
                2 + 24 * uv_counter, 1 + 24 * uv_counter, 3 + 24 * uv_counter,  # TRIANGLE 10
                12 + 24 * uv_counter, 13 + 24 * uv_counter, 14 + 24 * uv_counter,  # TRIANGLE 11
                14 + 24 * uv_counter, 13 + 24 * uv_counter, 15 + 24 * uv_counter,  # TRIANGLE 12
            ])
                            
            uv_counter += 1

            # Normals
            for i in range(24):
                level_normals.append(normals[i])

            level_normals_ind.extend([
                0 + 24 * normal_counter, 1 + 24 * normal_counter, 2 + 24 * normal_counter,
                2 + 24 * normal_counter, 1 + 24 * normal_counter, 3 + 24 * normal_counter,
                4 + 24 * normal_counter, 5 + 24 * normal_counter, 6 + 24 * normal_counter,
                6 + 24 * normal_counter, 5 + 24 * normal_counter, 7 + 24 * normal_counter,
                8 + 24 * normal_counter, 9 + 24 * normal_counter, 10 + 24 * normal_counter,
                10 + 24 * normal_counter, 9 + 24 * normal_counter, 11 + 24 * normal_counter,
                12 + 24 * normal_counter, 13 + 24 * normal_counter, 14 + 24 * normal_counter,
                14 + 24 * normal_counter, 13 + 24 * normal_counter, 15 + 24 * normal_counter,
                16 + 24 * normal_counter, 17 + 24 * normal_counter, 18 + 24 * normal_counter,
                18 + 24 * normal_counter, 17 + 24 * normal_counter, 19 + 24 * normal_counter,
                20 + 24 * normal_counter, 21 + 24 * normal_counter, 22 + 24 * normal_counter,
                22 + 24 * normal_counter, 21 + 24 * normal_counter, 23 + 24 * normal_counter
            ])

            normal_counter += 1
        
        # Tree leafs
        # ROWS
        rs = {
            0:(4, 3),
            1:(3, 2),
            2:(2, 1),
            3:(1, 0),
            4:(0, -1),
            5:(-1, -2),
            6:(-2, -3),
            7:(-3, -4)
        }

        # COLUMNS
        cs = {
            0:(4, 3),
            1:(3, 2),
            2:(2, 1),
            3:(1, 0),
            4:(0, -1),
            5:(-1, -2),
            6:(-2, -3),
            7:(-3, -4)
        }

        # TRIANGLES
        tr = {
            1:(0, 1, 2),
            2:(2, 1, 3),
            3:(2, 3, 4),
            4:(4, 3, 5),
            5:(4, 5, 6),
            6:(6, 5, 7),
            7:(6, 7, 0),
            8:(0, 7, 1),
            9:(1, 7, 3),
            10:(3, 7, 5),
            11:(6, 0, 4),
            12:(4, 0, 2)
        }

        self.leaf_position = Vector3(center.x + 1.5, center_y, center.z + 1.5)
        for ROW in range(0, self.leaf_area[0]):
            for COLUMN in range(0, self.leaf_area[1]):
                # Top vertices
                TLU = (self.leaf_position.x - cs.get(COLUMN)[0], self.leaf_position.y, self.leaf_position.z - rs.get(ROW)[0])
                TLD = (self.leaf_position.x - cs.get(COLUMN)[0], self.leaf_position.y, self.leaf_position.z - rs.get(ROW)[1])
                TRU = (self.leaf_position.x - cs.get(COLUMN)[1], self.leaf_position.y, self.leaf_position.z - rs.get(ROW)[0])
                TRD = (self.leaf_position.x - cs.get(COLUMN)[1], self.leaf_position.y, self.leaf_position.z - rs.get(ROW)[1])

                # Bottom vertices
                BLU = (self.leaf_position.x - cs.get(COLUMN)[0], self.leaf_position.y - 1, self.leaf_position.z - rs.get(ROW)[0])
                BLD = (self.leaf_position.x - cs.get(COLUMN)[0], self.leaf_position.y - 1, self.leaf_position.z - rs.get(ROW)[1])
                BRU = (self.leaf_position.x - cs.get(COLUMN)[1], self.leaf_position.y - 1, self.leaf_position.z - rs.get(ROW)[0])
                BRD = (self.leaf_position.x - cs.get(COLUMN)[1], self.leaf_position.y - 1, self.leaf_position.z - rs.get(ROW)[1])

                level_vertices.extend([TLU, TLD, TRU, TRD, BLU, BLD, BRU, BRD])
                level_triangles.extend([
                    0 + 8 * separator, 1 + 8 * separator, 2 + 8 * separator,  # TRIANGLE 1
                    2 + 8 * separator, 1 + 8 * separator, 3 + 8 * separator,  # TRIANGLE 2
                    4 + 8 * separator, 5 + 8 * separator, 6 + 8 * separator,  # TRIANGLE 3
                    6 + 8 * separator, 5 + 8 * separator, 7 + 8 * separator,  # TRIANGLE 4
                    1 + 8 * separator, 5 + 8 * separator, 3 + 8 * separator,  # TRIANGLE 5
                    3 + 8 * separator, 5 + 8 * separator, 7 + 8 * separator,  # TRIANGLE 6
                    0 + 8 * separator, 4 + 8 * separator, 2 + 8 * separator,  # TRIANGLE 7
                    2 + 8 * separator, 4 + 8 * separator, 6 + 8 * separator,  # TRIANGLE 8
                    4 + 8 * separator, 0 + 8 * separator, 5 + 8 * separator,  # TRIANGLE 9
                    5 + 8 * separator, 0 + 8 * separator, 1 + 8 * separator,  # TRIANGLE 10
                    6 + 8 * separator, 2 + 8 * separator, 7 + 8 * separator,  # TRIANGLE 11
                    7 + 8 * separator, 2 + 8 * separator, 3 + 8 * separator,  # TRIANGLE 12
                ])

                separator += 1

                # Texture atlas locations
                # atlas_length = 16
                # atlas_height = 16
                # HM_F = 10  # Horizontal Multiplier to first border
                # HM_L = 11  # Horizontal Multiplier to last border
                # VM_F = 15  # Vertical Multiplier to first border
                # VM_L = 16  # Vertical Multiplier to last border
                # BD = 0.0000000099  # border_deficiency
                # ONE = 1 + BD
                atlas_length = 16
                atlas_height = 16
                HM_F = 0  # Horizontal Multiplier to first border
                HM_L = 1  # Horizontal Multiplier to last border
                VM_F = 3  # Vertical Multiplier to first border
                VM_L = 4  # Vertical Multiplier to last border
                BD = 0.0000000099  # border_deficiency
                ONE = 1 + BD

                uvs_face = [
                    (ONE / atlas_length * HM_F, ONE / atlas_height * VM_F), (ONE / atlas_length * HM_L, ONE / atlas_height * VM_F), (ONE / atlas_length * HM_F, ONE / atlas_height * VM_L),
                    (ONE / atlas_length * HM_L, ONE / atlas_height * VM_L), (ONE / atlas_length * HM_F, ONE / atlas_height * VM_F), (ONE / atlas_length * HM_L, ONE / atlas_height * VM_F),
                    (ONE / atlas_length * HM_F, ONE / atlas_height * VM_L), (ONE / atlas_length * HM_L, ONE / atlas_height * VM_L), (ONE / atlas_length * HM_F, ONE / atlas_height * VM_F),
                    (ONE / atlas_length * HM_L, ONE / atlas_height * VM_F), (ONE / atlas_length * HM_F, ONE / atlas_height * VM_L), (ONE / atlas_length * HM_L, ONE / atlas_height * VM_L),
                    (ONE / atlas_length * HM_F, ONE / atlas_height * VM_F), (ONE / atlas_length * HM_L, ONE / atlas_height * VM_F), (ONE / atlas_length * HM_F, ONE / atlas_height * VM_L),
                    (ONE / atlas_length * HM_L, ONE / atlas_height * VM_L), (ONE / atlas_length * HM_F, ONE / atlas_height * VM_F), (ONE / atlas_length * HM_L, ONE / atlas_height * VM_F),
                    (ONE / atlas_length * HM_F, ONE / atlas_height * VM_L), (ONE / atlas_length * HM_L, ONE / atlas_height * VM_L), (ONE / atlas_length * HM_F, ONE / atlas_height * VM_F),
                    (ONE / atlas_length * HM_L, ONE / atlas_height * VM_F), (ONE / atlas_length * HM_F, ONE / atlas_height * VM_L), (ONE / atlas_length * HM_L, ONE / atlas_height * VM_L)
                ]

                # UV vertices
                level_uvs.append(uvs_face[0])
                level_uvs.append(uvs_face[1])
                level_uvs.append(uvs_face[2])
                level_uvs.append(uvs_face[3])
                level_uvs.append(uvs_face[4])
                level_uvs.append(uvs_face[5])
                level_uvs.append(uvs_face[6])
                level_uvs.append(uvs_face[7])
                level_uvs.append(uvs_face[8])
                level_uvs.append(uvs_face[9])
                level_uvs.append(uvs_face[10])
                level_uvs.append(uvs_face[11])
                level_uvs.append(uvs_face[12])
                level_uvs.append(uvs_face[13])
                level_uvs.append(uvs_face[14])
                level_uvs.append(uvs_face[15])
                level_uvs.append(uvs_face[16])
                level_uvs.append(uvs_face[17])
                level_uvs.append(uvs_face[18])
                level_uvs.append(uvs_face[19])
                level_uvs.append(uvs_face[20])
                level_uvs.append(uvs_face[21])
                level_uvs.append(uvs_face[22])
                level_uvs.append(uvs_face[23])

                # UV triangles
                level_uvs_ind.extend([
                    20 + 24 * uv_counter, 21 + 24 * uv_counter, 22 + 24 * uv_counter,  # TRIANGLE 1
                    22 + 24 * uv_counter, 21 + 24 * uv_counter, 23 + 24 * uv_counter,  # TRIANGLE 2
                    4 + 24 * uv_counter, 5 + 24 * uv_counter, 6 + 24 * uv_counter,  # TRIANGLE 3
                    6 + 24 * uv_counter, 5 + 24 * uv_counter, 7 + 24 * uv_counter,  # TRIANGLE 4
                    8 + 24 * uv_counter, 9 + 24 * uv_counter, 10 + 24 * uv_counter,  # TRIANGLE 5
                    10 + 24 * uv_counter, 9 + 24 * uv_counter, 11 + 24 * uv_counter,  # TRIANGLE 6
                    16 + 24 * uv_counter, 17 + 24 * uv_counter, 18 + 24 * uv_counter,  # TRIANGLE 7
                    18 + 24 * uv_counter, 17 + 24 * uv_counter, 19 + 24 * uv_counter,  # TRIANGLE 8
                    0 + 24 * uv_counter, 1 + 24 * uv_counter, 2 + 24 * uv_counter,  # TRIANGLE 9
                    2 + 24 * uv_counter, 1 + 24 * uv_counter, 3 + 24 * uv_counter,  # TRIANGLE 10
                    12 + 24 * uv_counter, 13 + 24 * uv_counter, 14 + 24 * uv_counter,  # TRIANGLE 11
                    14 + 24 * uv_counter, 13 + 24 * uv_counter, 15 + 24 * uv_counter,  # TRIANGLE 12
                ])

                uv_counter += 1

                # Normals
                for i in range(24):
                    level_normals.append(normals[i])

                level_normals_ind.extend([
                    0 + 24 * normal_counter, 1 + 24 * normal_counter, 2 + 24 * normal_counter,
                    2 + 24 * normal_counter, 1 + 24 * normal_counter, 3 + 24 * normal_counter,
                    4 + 24 * normal_counter, 5 + 24 * normal_counter, 6 + 24 * normal_counter,
                    6 + 24 * normal_counter, 5 + 24 * normal_counter, 7 + 24 * normal_counter,
                    8 + 24 * normal_counter, 9 + 24 * normal_counter, 10 + 24 * normal_counter,
                    10 + 24 * normal_counter, 9 + 24 * normal_counter, 11 + 24 * normal_counter,
                    12 + 24 * normal_counter, 13 + 24 * normal_counter, 14 + 24 * normal_counter,
                    14 + 24 * normal_counter, 13 + 24 * normal_counter, 15 + 24 * normal_counter,
                    16 + 24 * normal_counter, 17 + 24 * normal_counter, 18 + 24 * normal_counter,
                    18 + 24 * normal_counter, 17 + 24 * normal_counter, 19 + 24 * normal_counter,
                    20 + 24 * normal_counter, 21 + 24 * normal_counter, 22 + 24 * normal_counter,
                    22 + 24 * normal_counter, 21 + 24 * normal_counter, 23 + 24 * normal_counter
                ])

                normal_counter += 1

        return level_vertices, level_triangles, level_uvs, level_uvs_ind, level_normals, level_normals_ind
