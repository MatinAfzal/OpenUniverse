from .Mesh import *
from .Utils import *
from .Settings2 import *


class LoadObject(Mesh):
    """
    Loads a 3D mesh from an OBJ file and initializes it for rendering.

    This class is responsible for reading mesh data from an OBJ file, including
    vertices, texture coordinates, and normals. It formats this data and sets up
    the mesh for rendering within the graphics environment.

    Attributes:
        draw_type (int): The OpenGL draw type (e.g., GL_TRIANGLES).
        location (pygame.Vector3): The position of the object in 3D space.
        rotation (Rotation): The initial rotation of the object.
        scale (pygame.Vector3): The scaling factors for the object in 3D.
        move_rotation (Rotation): The rotation applied during movement.
        move_translate (pygame.Vector3): The translation applied during movement.
        move_scale (pygame.Vector3): The scaling applied during movement.
        material (optional): The material used for rendering the object.
        memory_save (bool): Flag to save memory usage (default is False).
        memory_save_chunk (bool): Flag to save memory in chunks (default is False).
        distance_range (float): The distance range for visibility (default is 12).
        esp_off (bool): Flag to disable ESP output (default is False).

    Parameters:
        filename (str): The path to the OBJ file to be loaded.
        image_file (str): The texture image file associated with the mesh.
        draw_type (int): The OpenGL draw type for rendering the mesh (default is GL_TRIANGLES).
        location (pygame.Vector3): Initial position of the object in 3D space (default is (0, 0, 0)).
        rotation (Rotation): Initial rotation of the object (default is identity rotation).
        scale (pygame.Vector3): Initial scaling of the object (default is (1, 1, 1)).
        move_rotation (Rotation): Rotation applied during object movement (default is identity).
        move_translate (pygame.Vector3): Translation applied during object movement (default is (0, 0, 0)).
        move_scale (pygame.Vector3): Scaling applied during object movement (default is (1, 1, 1)).
        material (optional): Material used for rendering (default is None).
        memory_save (bool): Whether to save memory during loading (default is False).
        memory_save_chunk (bool): Whether to save memory in chunks (default is False).
        distance_range (float): Distance range for rendering (default is 12).
        esp_off (bool): Flag to disable debug print statements (default is False).

    Methods:
        load_drawing(filename) -> tuple:
            Reads the OBJ file and extracts vertices, triangles, UVs, and normals.

    Notes:
        - Ensure the specified OBJ file is correctly formatted to prevent reading errors.
        - The class inherits from `Mesh`, and all relevant parameters are passed to the
          superclass for initialization.
        - If `ESP` is enabled and `esp_off` is not set, loading messages will be printed.
    """
    def __init__(self, filename, image_file, draw_type=GL_TRIANGLES,
                 location=pygame.Vector3(0, 0, 0),
                 rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 scale=pygame.Vector3(1, 1, 1),
                 move_rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 move_translate=pygame.Vector3(0, 0, 0),
                 move_scale=pygame.Vector3(1, 1, 1),
                 material=None,
                 memory_save=False,
                 memory_save_chunk=False,
                 distance_range=12,
                 esp_off=False
                 ):

        if ESP and not esp_off:
            print("Loading Objects...")
        
        # Mesh sections
        coordinates, triangles, uvs, uvs_ind, normals, normal_ind = self.load_drawing(filename)
        vertices = format_vertices(coordinates, triangles)
        vertex_normals = format_vertices(normals, normal_ind)
        vertex_uvs = format_vertices(uvs, uvs_ind)
        colors = []
        
        for i in range(len(vertices)):
            colors.append(1)
            colors.append(1)
            colors.append(1)
            
        super().__init__(vertices,
                         image_file=image_file,
                         vertex_normals=vertex_normals,
                         vertex_uvs=vertex_uvs,
                         vertex_colors=colors,
                         draw_type=draw_type,
                         translation=location,
                         rotation=rotation,
                         scale=scale,
                         move_rotation=move_rotation,
                         move_translate=move_translate,
                         move_scale=move_scale,
                         material=material,
                         memory_save=memory_save,
                         memory_save_chunk=memory_save_chunk,
                         distance_range=distance_range,
                         esp_off=esp_off)

    def load_drawing(self, filename):
        vertices = []
        triangles = []
        normals = []
        normal_ind = []
        uvs = []
        uvs_ind = []
        with open(filename) as fp:
            line = fp.readline()
            while line:
                try:
                    if line[:2] == "v ":
                        vx, vy, vz = [float(value) for value in line[2:].split()]
                        vertices.append((vx, vy, vz))
                    if line[:2] == "vn":
                        vx, vy, vz = [float(value) for value in line[3:].split()]
                        normals.append((vx, vy, vz))
                    if line[:2] == "vt":
                        vx, vy = [float(value) for value in line[3:].split()]
                        uvs.append((vx, vy))
                    if line[:2] == "f ":
                        t1, t2, t3 = [value for value in line[2:].split()]
                        triangles.append([int(value) for value in t1.split('/')][0]-1)
                        triangles.append([int(value) for value in t2.split('/')][0]-1)
                        triangles.append([int(value) for value in t3.split('/')][0]-1)
                        uvs_ind.append([int(value) for value in t1.split('/')][1] - 1)
                        uvs_ind.append([int(value) for value in t2.split('/')][1] - 1)
                        uvs_ind.append([int(value) for value in t3.split('/')][1] - 1)
                        normal_ind.append([int(value) for value in t1.split('/')][2] - 1)
                        normal_ind.append([int(value) for value in t2.split('/')][2] - 1)
                        normal_ind.append([int(value) for value in t3.split('/')][2] - 1)
                except:
                    print("READING OBJ ERROR")
                line = fp.readline()

        return vertices, triangles, uvs, uvs_ind, normals, normal_ind
