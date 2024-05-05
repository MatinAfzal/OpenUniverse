import numpy as np
from Engine2.Mesh import *
from Engine2.Settings2 import *
from Engine2.Cullings.ChunkRenderDistance import *

class CellAttach:
    """
    Attach multiple draw cells togther
    - Avoiding draw loops!
    - One line draw (world.draw()) !
    """
    
    def __init__(self, cells: list[object], draw_type=GL_TRIANGLES, shader=None, image=None, chunk=False) -> None:
        print("Attaching Cells...")
        self.image = image
        self.cells = cells
        
        if chunk:
            self.td_cells = np.reshape(cells, newshape=(30, 30))
        
        self.world_formated_vertices = [] # world vertices formated in triangle order
        self.world_formated_uvs = [] 
        self.world_shader = shader
        self.world = None
        self.world_draw_type = draw_type
        self.colors = []
        self.call_time = 0
        
        self.render_distance = 40 # Chunks
        self.load_map = ChunkRenderDistance(renderdistance=self.render_distance)
        self.load_map.first_load()
        
        if not chunk:
            self.attach_vertices(self.cells)
            self.attach_uvs(self.cells)
            self.load_world()
        
    
    def attach_vertices(self, cells):
        if len(cells) < 2:
            print("\n\nERROR: NO ENOUGH CELLS TO ATTACH!\n\n")
            return 0
            
        self.world_formated_vertices = np.concatenate((cells[0].vertices, cells[1].vertices))
        
        for object in cells[2:]:
            if self.load_map.load_map[int(object.position.x)][int(object.position.z)] == 1:
                self.world_formated_vertices = np.concatenate((self.world_formated_vertices, object.vertices))
            else:
                pass       
        
        
    def attach_uvs(self, cells):
        if len(cells) < 2:
            print("ERROR: NO ENOUGH CELLS TO ATTACH!")
            return 0
            
        self.world_formated_uvs = np.concatenate((cells[0].vertex_uvs, cells[1].vertex_uvs))
        
        for object in cells[2:]:
            if self.load_map.load_map[int(object.position.x)][int(object.position.z)] == 1:
                self.world_formated_uvs = np.concatenate((self.world_formated_uvs, object.vertex_uvs))
            else:
                pass

#############################################################################################################################################################
    # def cell_attachment_update(self, camera_position):
    #     flag = False
    #     if self.call_time == 0:
    #         self.attach_vertices(np.ravel(self.td_cells[self.load_map.player_location[0]:self.load_map.player_location[0]+2, self.load_map.player_location[1]:self.load_map.player_location[1]+2]))
    #         self.attach_uvs(np.ravel(self.td_cells[self.load_map.player_location[0]:self.load_map.player_location[0]+2, self.load_map.player_location[1]:self.load_map.player_location[1]+2]))
    #         self.load_world()
            
    #         self.call_time += 1
    #     elif camera_position.x < 0 or camera_position.z < 0:
    #         pass
    #     elif (camera_position.x < 8 and camera_position.x >= 0) or (camera_position.y < 8 and camera_position.y >= 0): # First Chunk - below 8 
    #         current_cunk = pygame.Vector3(0, 0, 0)
    #         flag = True
    #     elif abs(self.load_map.player_location[0] - int(camera_position.x / 8)) > 0 or abs(self.load_map.player_location[1] - int(camera_position.z / 8)) > 0:
    #         flag = True
    #     else:
    #         current_cunk = pygame.Vector3(int(camera_position.x) / 8, 0, int(camera_position.z) / 8)
    #         flag = True
        
    #     if flag == True:
    #         if abs(abs(self.load_map.player_location[0]) - abs(camera_position.x)) > 8 * self.render_distance or abs(abs(self.load_map.player_location[1]) - abs(camera_position.z)) > 8 * self.render_distance:
    #             self.load_map.player_location[0] = int(camera_position.x / 8)
    #             self.load_map.player_location[1] = int(camera_position.z / 8)
                
    #             self.load_map.init_map()
    #             self.load_map.first_load()
                
    #             self.world_formated_vertices = []
    #             self.world_formated_uvs = []
    #             self.colors = []
                
    #             self.attach_vertices(np.ravel(self.td_cells[self.load_map.player_location[0]-self.render_distance:self.load_map.player_location[0]+self.render_distance, self.load_map.player_location[1]-self.render_distance:self.load_map.player_location[1]+self.render_distance]))
    #             self.attach_uvs(np.ravel(self.td_cells[self.load_map.player_location[0]-self.render_distance:self.load_map.player_location[0]+self.render_distance, self.load_map.player_location[1]-self.render_distance:self.load_map.player_location[1]+self.render_distance]))
                
    #             self.load_world()
    #             self.call_time += 1
#############################################################################################################################################################
                
    def load_world(self):
        for _ in range(len(self.world_formated_vertices * 3)):
            self.colors.append(CHUNK_COLOR_R)
            self.colors.append(CHUNK_COLOR_G)
            self.colors.append(CHUNK_COLOR_B)
            
        self.world = Mesh(vertices=self.world_formated_vertices,
                     imagefile=self.image,
                     material=self.world_shader,
                     draw_type=self.world_draw_type,
                     vertex_colors=self.colors,
                     vertex_uvs=self.world_formated_uvs)