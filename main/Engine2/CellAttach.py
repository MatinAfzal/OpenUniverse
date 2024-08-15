import threading
from .Mesh import *
from .Settings2 import *


class CellAttach:
    """
    Attach multiple draw cells together
    - Avoiding draw loops!
    - One line draw (world.draw()) !
    """

    def __init__(self, cells: list[object], draw_type=GL_TRIANGLES, shader=None, image=None) -> None:
        if ESP:
            print("Attaching Cells...")

        self.level_name = cells[0].level_name
        self.image = image
        self.cells = cells
        
        self.world_formatted_vertices = []  # world vertices formatted in triangle order
        self.world_formatted_uvs = []
        self.world_formatted_normals = []
        self.world_shader = shader
        self.world = None
        self.world_draw_type = draw_type
        self.colors = []
        self.call_time = 0

        # Multiprocessing (6 seconds in 30x30)
        t1 = threading.Thread(target=self.attach_vertices)
        t2 = threading.Thread(target=self.attach_uvs)
        t3 = threading.Thread(target=self.attach_normals)

        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()

        # Linear processing  (12 seconds in 30x30)
        # self.attach_vertices()
        # self.attach_uvs()
        # self.attach_normals()

        self.load_world()  # IMPORTANT!

    def attach_vertices(self):
        cells = self.cells
        if len(cells) < 2:
            print("\n\nERROR: NO ENOUGH CELLS TO ATTACH!\n\n")
            return 0
            
        self.world_formatted_vertices = np.concatenate((cells[0].vertices, cells[1].vertices))
        
        for instance in cells[2:]:
            self.world_formatted_vertices = np.concatenate((self.world_formatted_vertices, instance.vertices))

    def attach_uvs(self):
        cells = self.cells
        if len(cells) < 2:
            print("ERROR: NO ENOUGH CELLS TO ATTACH!")
            return 0

        self.world_formatted_uvs = np.concatenate((cells[0].vertex_uvs, cells[1].vertex_uvs))
        
        for instance in cells[2:]:
            self.world_formatted_uvs = np.concatenate((self.world_formatted_uvs, instance.vertex_uvs))

    def attach_normals(self):
        cells = self.cells
        if len(cells) < 2:
            print("ERROR: NO ENOUGH CELLS TO ATTACH!")
            return 0

        self.world_formatted_normals = np.concatenate((cells[0].normals, cells[1].normals))

        for instance in cells[2:]:
            self.world_formatted_normals = np.concatenate((self.world_formatted_normals, instance.normals))
                
    def load_world(self):
        for _ in range(len(self.world_formatted_vertices * 3)):
            self.colors.append(CHUNK_COLOR_R)
            self.colors.append(CHUNK_COLOR_G)
            self.colors.append(CHUNK_COLOR_B)

        if self.level_name == "tree1":
            self.world = Mesh(
                vertices=self.world_formatted_vertices,
                imagefile=self.image,
                material=self.world_shader,
                draw_type=self.world_draw_type,
                vertex_colors=self.colors,
                vertex_uvs=self.world_formatted_uvs,
                vertex_normals=self.world_formatted_normals
            )
        else:
            self.world = Mesh(
                vertices=self.world_formatted_vertices,
                imagefile=self.image,
                material=self.world_shader,
                draw_type=self.world_draw_type,
                vertex_colors=self.colors,
                vertex_uvs=self.world_formatted_uvs,
                vertex_normals=self.world_formatted_normals
            )
