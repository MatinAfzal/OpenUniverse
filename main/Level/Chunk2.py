from Engine2.Mesh import Mesh
from OpenGL.GL import *
from Engine2.Utils import format_vertices
from Engine2.Settings2 import *
from opensimplex.internals import _noise2, _noise3, _init

class Chunk2(Mesh):
    def __init__(self, position, max_height=10, min_death=-10 , shematic=None, img=None, material=None) -> None:
        """Chunk generator

        Args:
            position (pygame.Vector3): chunk center vertex position
            max_height (int): chunk maximum height
            min_DEATH_A (int): chunk minimum DEATH_A
            biome (str): chunk biome
        """
        
        self.material = material
        self.position = position
        self.shematic = shematic
        # self.shematic_shape = shematic.shape
        # self.image = img
        self.vertices = None
        self.lines = None
        self.triangles = None
        self.colors = []
        self.translation = self.position
        self.max = max_height
        self.min = min_death
        self.height = self.max + (self.min * -1)
        self.left = 8
        self.right = 8
        self.area = self.left * self.right * self.height
        
        # Texture atlas locations
        self.atlas_length = 15.9999991
        self.atlas_height = 15.9999991
        self.HM_F = 0 # Horizontal Multiplier to first border
        self.HM_L = 1 # Horizontal Multiplier to last border
        self.VM_F = 0  # Vertical Multiplier to first border
        self.VM_L = 1 # Vertical Multiplier to last border
        self.BD = 0.0000099 # border_deficiency
        self.ONE = 1 - self.BD
            
        self.vertices, self.triangles , uvs, uvs_ind= self.level_maker(self.position)
        self.vertices = format_vertices(self.vertices, self.triangles)
        
        self.vertex_uvs = format_vertices(uvs, uvs_ind)
        
        for _ in range(len(self.vertices)):
                self.colors.append(CHUNK_COLOR_R)
                self.colors.append(CHUNK_COLOR_G)
                self.colors.append(CHUNK_COLOR_B)
                
        super().__init__(self.vertices,
                 imagefile=img,
                 vertex_normals=None,
                 vertex_uvs=self.vertex_uvs,
                 vertex_colors=self.colors,
                 draw_type=GL_TRIANGLES,
                 material=self.material,
                 memory_save=True,
                 memory_save_chunk=False,
                 distance_range=12
                 )
        
    
    def level_maker(self, center):
        """Chunk level maker
        
        Args:
            position (pygame.Vector3): chunk center position

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
        RS = {
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
        CS = {
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
        TR = {
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
        
        level_vertices = []
        level_triangles = []
        level_uvs = []
        level_uvs_ind = []
        triangle_counter = 0
        uv_counter = 0
        self.perm, self.perm_grad_index3 = _init(seed=100)
        
        for ROW in range(0, 8): # Z
            for COLUMN in range(0, 8): # X
                for DEATH_A in range(self.min, int(_noise2(COLUMN, ROW, perm=self.perm)) * 20): # Y
                    
                    if DEATH_A <= -5: 
                        self.HM_F = 5
                        self.HM_L = 6
                        self.VM_F = 15
                        self.VM_L = 16
                    elif DEATH_A >= -4:
                        self.HM_F = 9
                        self.HM_L = 10
                        self.VM_F = 15
                        self.VM_L = 16
                    else:
                        print(f"ERROR: Unidentified block detected... ZXY:{ROW}/{COLUMN}/{DEATH_A}")
                        
                    uvs_face = [
                        (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L),
                        (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F), 
                        (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F), 
                        (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L), 
                        (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L), 
                        (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F), 
                        (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F), 
                        (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L)
                    ]
                        
                    # Top vertices
                    TLU = (center.x - CS.get(COLUMN)[0], center.y + DEATH_A, center.z - RS.get(ROW)[0])
                    TLD = (center.x - CS.get(COLUMN)[0], center.y + DEATH_A, center.z - RS.get(ROW)[1])
                    TRU = (center.x - CS.get(COLUMN)[1], center.y + DEATH_A, center.z - RS.get(ROW)[0])
                    TRD = (center.x - CS.get(COLUMN)[1], center.y + DEATH_A, center.z - RS.get(ROW)[1])
                    
                    # Bottom vertices
                    BLU = (center.x - CS.get(COLUMN)[0], center.y + DEATH_A - 1, center.z - RS.get(ROW)[0])
                    BLD = (center.x - CS.get(COLUMN)[0], center.y + DEATH_A - 1, center.z - RS.get(ROW)[1])
                    BRU = (center.x - CS.get(COLUMN)[1], center.y + DEATH_A - 1, center.z - RS.get(ROW)[0])
                    BRD = (center.x - CS.get(COLUMN)[1], center.y + DEATH_A - 1, center.z - RS.get(ROW)[1])
                    
                    # Mesh triangles
                    level_vertices.extend([TLU, TLD, TRU, TRD, BLU, BLD, BRU, BRD])
                    level_triangles.extend([
                        0 + 8 * triangle_counter, 1 + 8 * triangle_counter, 2 + 8 * triangle_counter, # TRIANGLE 1
                        2 + 8 * triangle_counter, 1 + 8 * triangle_counter, 3 + 8 * triangle_counter, # TRIANGLE 2
                        4 + 8 * triangle_counter, 5 + 8 * triangle_counter, 6 + 8 * triangle_counter, # TRIANGLE 3
                        6 + 8 * triangle_counter, 5 + 8 * triangle_counter, 7 + 8 * triangle_counter, # TRIANGLE 4
                        1 + 8 * triangle_counter, 5 + 8 * triangle_counter, 3 + 8 * triangle_counter, # TRIANGLE 5
                        3 + 8 * triangle_counter, 5 + 8 * triangle_counter, 7 + 8 * triangle_counter, # TRIANGLE 6
                        0 + 8 * triangle_counter, 4 + 8 * triangle_counter, 2 + 8 * triangle_counter, # TRINAGLE 7
                        2 + 8 * triangle_counter, 4 + 8 * triangle_counter, 6 + 8 * triangle_counter, # TRIANGLE 8
                        4 + 8 * triangle_counter, 0 + 8 * triangle_counter, 5 + 8 * triangle_counter, # TRIANGLE 9
                        5 + 8 * triangle_counter, 0 + 8 * triangle_counter, 1 + 8 * triangle_counter, # TRIANGLE 10
                        6 + 8 * triangle_counter, 2 + 8 * triangle_counter, 7 + 8 * triangle_counter, # TRIANGLE 11
                        7 + 8 * triangle_counter, 2 + 8 * triangle_counter, 3 + 8 * triangle_counter, # TRIANGLE 12
                    ])
                    
                    # UV vertices
                    for i in range(24):
                        level_uvs.append(uvs_face[i])
                        
                    # UV triangles
                    level_uvs_ind.extend([
                        20 + 24 * uv_counter, 21 + 24 * uv_counter, 22 + 24 * uv_counter, # TRIANGLE 1
                        22 + 24 * uv_counter, 21 + 24 * uv_counter, 23 + 24 * uv_counter, # TRIANGLE 2
                        4 + 24 * uv_counter, 5 + 24 * uv_counter, 6 + 24 * uv_counter, # TRIANGLE 3
                        6 + 24 * uv_counter, 5 + 24 * uv_counter, 7 + 24 * uv_counter, # TRIANGLE 4
                        8 + 24 * uv_counter, 9 + 24 * uv_counter, 10 + 24 * uv_counter, # TRIANGLE 5
                        10 + 24 * uv_counter, 9 + 24 * uv_counter, 11 + 24 * uv_counter, # TRIANGLE 6
                        16 + 24 * uv_counter, 17 + 24 * uv_counter, 18 + 24 * uv_counter, # TRIANGLE 7
                        18 + 24 * uv_counter, 17 + 24 * uv_counter, 19 + 24 * uv_counter, # TRIANGLE 8
                        0 + 24 * uv_counter, 1 + 24 * uv_counter, 2 + 24 * uv_counter, # TRIANGLE 9
                        2 + 24 * uv_counter, 1 + 24 * uv_counter, 3 + 24 * uv_counter, # TRIANGLE 10
                        12 + 24 * uv_counter, 13 + 24 * uv_counter, 14 + 24 * uv_counter, # TRIANGLE 11
                        14 + 24 * uv_counter, 13 + 24 * uv_counter, 15 + 24 * uv_counter, # TRIANGLE 12
                    ])
                                
                    triangle_counter += 1
                    uv_counter += 1
        
        return level_vertices, level_triangles, level_uvs, level_uvs_ind