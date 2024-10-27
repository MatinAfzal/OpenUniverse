from .Utils import *


class Material:
    """
    Represents a shader program for rendering materials in the graphics environment.

    This class encapsulates the creation of a shader program using vertex and fragment
    shaders, allowing for the application of various rendering techniques and effects
    to 3D objects.

    Attributes:
        program_id (int): The OpenGL identifier for the shader program.

    Parameters:
        vertex_shader (str): The path to the vertex shader source file.
        fragment_shader (str): The path to the fragment shader source file.

    Methods:
        use() -> None:
            Activates the shader program for rendering.

    Notes:
        - The `create_program` function is expected to compile the provided shaders and link them
          into a program.
        - Ensure that the shader files are correctly formatted and contain valid GLSL code.
        - The `ESP` variable controls debug print statements for development purposes.
    """
    def __init__(self, vertex_shader, fragment_shader):
        if ESP:
            print("creating Program...")
        self.program_id = create_program(open(vertex_shader).read(), open(fragment_shader).read())

    def use(self):
        glUseProgram(self.program_id)
