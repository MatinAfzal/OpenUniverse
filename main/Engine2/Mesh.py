from .DataHandler import *
from .Uniform import *
from .Transformations import *
from .Texture import *
from .Settings2 import *


class Mesh:
    """
    Mesh Loader for 3D Objects.

    This class is responsible for loading, transforming, and rendering 3D meshes
    using OpenGL. It handles the creation of vertex buffer objects, texture binding,
    and applying transformations to the mesh.

    Attributes:
        position (pygame.Vector3): The translation position of the mesh.
        material (Material): The shader program used for rendering the mesh.
        vertices (list): The vertex data of the mesh.
        vertex_normals (list): The normal vectors for lighting calculations.
        vertex_uvs (list): The texture coordinates for the mesh.
        draw_type (int): The OpenGL draw type (e.g., GL_TRIANGLES).
        memory_save (bool): Flag for saving memory during rendering.
        distance_range (float): The rendering distance range for optimization.
        vao_ref (int): OpenGL reference for the Vertex Array Object.
        transformation_mat (numpy.ndarray): The transformation matrix for the mesh.
        texture (Texture): The texture associated with the mesh, if any.

    Parameters:
        vertices (list): A list of vertex positions.
        image_file (str, optional): Path to the texture image file.
        vertex_normals (list, optional): A list of normal vectors.
        vertex_uvs (list, optional): A list of texture coordinates.
        vertex_colors (list, optional): A list of vertex colors.
        draw_type (int): OpenGL draw type for rendering (default: GL_TRIANGLES).
        translation (pygame.Vector3): Initial translation position (default: (0, 0, 0)).
        rotation (Rotation): Initial rotation parameters (default: no rotation).
        scale (pygame.Vector3): Initial scaling factors (default: (1, 1, 1)).
        move_rotation (Rotation): Rotation to apply during movement.
        move_translate (pygame.Vector3): Translation to apply during movement.
        move_scale (pygame.Vector3): Scaling to apply during movement.
        material (Material, optional): The shader material for rendering.
        memory_save (bool): Flag to indicate memory-saving mode (default: True).
        memory_save_chunk (bool): Chunking for memory-saving (default: False).
        distance_range (float): Distance range for optimization (default: 12).
        esp_off (bool): Flag to disable debug output (default: False).

    Methods:
        draw(camera, light) -> None:
            Renders the mesh using the specified camera and light.

        update(translation, rotation, scale) -> None:
            Updates the transformation matrix of the mesh based on the new parameters.

    Notes:
        - The `draw_force` method is used internally to handle the drawing of the mesh
          with transformations applied.
        - Ensure that the material provided is properly initialized with valid shader programs.
        - The `ESP` variable controls debug print statements for development purposes.
    """
    def __init__(self, vertices,
                 image_file=None,
                 vertex_normals=None,
                 vertex_uvs=None,
                 vertex_colors=None,
                 draw_type=GL_TRIANGLES,
                 translation=pygame.Vector3(0, 0, 0),
                 rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 scale=pygame.Vector3(1, 1, 1),
                 move_rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 move_translate=pygame.Vector3(0, 0, 0),
                 move_scale=pygame.Vector3(1, 1, 1),
                 material=None,
                 memory_save=True,
                 memory_save_chunk=False,
                 distance_range=12,
                 esp_off=False
                 ):

        self.esp_off = esp_off
        if ESP and not esp_off:
            print("Building Mesh...")
        
        self.position = translation
        self.material = material
        self.vertices = vertices
        self.vertex_normals = vertex_normals
        self.vertex_uvs = vertex_uvs
        self.draw_type = draw_type
        self.memory_save = memory_save
        self.memory_save_chunk = memory_save_chunk
        self.distance_range = distance_range
        
        self.vao_ref = glGenVertexArrays(1)
        glBindVertexArray(self.vao_ref)
        
        # Construction of mesh sections if there are any
        if vertices is not None:
            position = DataHandler("vec3", self.vertices)
            position.create_variable(self.material.program_id, "position")
            
        if vertex_colors is not None:
            colors = DataHandler("vec3", vertex_colors)
            colors.create_variable(self.material.program_id, "vertex_color")

        if vertex_normals is not None:
            v_normals = DataHandler("vec3", vertex_normals)
            v_normals.create_variable(self.material.program_id, "vertex_normal")
            
        if vertex_uvs is not None:
            v_uvs = DataHandler("vec2", vertex_uvs)
            v_uvs.create_variable(self.material.program_id, "vertex_uv")
            
        self.transformation_mat = identity_mat()
        self.transformation_mat = rotateA(self.transformation_mat, rotation.angle, rotation.axis)
        self.transformation_mat = translate(self.transformation_mat, translation.x, translation.y, translation.z)
        self.transformation_mat = scale3(self.transformation_mat, scale.x, scale.y, scale.z)
        self.transformation = Uniform("mat4", self.transformation_mat)
        self.transformation.find_variable(self.material.program_id, "model_mat")
        self.move_rotation = move_rotation
        self.move_translate = move_translate
        self.move_scale = move_scale
        self.texture = None
        
        if image_file is not None:
            self.image = Texture(image_file, esp_off=self.esp_off)
            self.texture = Uniform("sampler2D", [self.image.texture_id, 1])

    def draw_force(self, camera, light, draw_type_force=None):
        self.material.use()
        camera.update(self.material.program_id)
        light.update(self.material.program_id)
        
        if self.texture is not None:
            self.texture.find_variable(self.material.program_id, "tex")
            self.texture.load()
        
        self.transformation_mat = rotateA(self.transformation_mat, self.move_rotation.angle, self.move_rotation.axis)
        self.transformation_mat = translate(self.transformation_mat,
                                            self.move_translate.x, self.move_translate.y, self.move_translate.z)
        self.transformation_mat = scale3(
            self.transformation_mat, self.move_scale.x, self.move_scale.y, self.move_scale.z)
        self.transformation = Uniform("mat4", self.transformation_mat)
        self.transformation.find_variable(self.material.program_id, "model_mat")
        self.transformation.load()

        glBindVertexArray(self.vao_ref)
        
        if draw_type_force:
            glDrawArrays(draw_type_force, 0, len(self.vertices))
        glDrawArrays(self.draw_type, 0, len(self.vertices))

    def draw(self, camera, light):
        """
        Drawing mesh
        """

        self.draw_force(camera, light)

    def update(self, translation=pygame.Vector3(0, 0, 0), rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
               scale=pygame.Vector3(1, 1, 1)):
        self.transformation_mat = identity_mat()
        self.transformation_mat = rotateA(self.transformation_mat, rotation.angle, rotation.axis)
        self.transformation_mat = translate(self.transformation_mat, translation.x, translation.y, translation.z)
        self.transformation_mat = scale3(self.transformation_mat, scale.x, scale.y, scale.z)
        self.transformation = Uniform("mat4", self.transformation_mat)
        self.transformation.find_variable(self.material.program_id, "model_mat")
