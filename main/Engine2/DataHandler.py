import numpy as np
from OpenGL.GL import *


class DataHandler:
    """
    Handles OpenGL buffer creation and data loading for vertex attributes.

    This class simplifies the process of creating OpenGL buffer objects for storing
    vertex data (such as positions, normals, or texture coordinates). It manages
    data loading into GPU memory and sets up the vertex attribute pointers for
    rendering.

    Attributes:
        data_type (str): The type of data being handled, e.g., "vec2" for 2D vectors
                         or "vec3" for 3D vectors.
        data (list or np.ndarray): The data to be stored in the OpenGL buffer,
                                   typically a list or NumPy array of floats.
        buffer_ref (int): The OpenGL buffer ID generated for this data.

    Parameters:
        data_type (str): The type of vertex attribute data (e.g., "vec2", "vec3").
        data (list or np.ndarray): The actual vertex data to be stored in the buffer.

    Methods:
        load() -> None:
            Binds the buffer and loads the vertex data into GPU memory.

        create_variable(program_id, variable_name) -> None:
            Sets up the vertex attribute pointer for the specified variable in the
            given shader program.

    Notes:
        - This class relies on the PyOpenGL library for OpenGL function calls.
        - The data should be structured correctly based on the specified `data_type`
          to ensure proper rendering.
        - Make sure to use the appropriate shader program ID when calling
          `create_variable`.
    """
    def __init__(self, data_type, data):
        self.data_type = data_type
        self.data = data
        self.buffer_ref = glGenBuffers(1)
        self.load()

    def load(self):
        data = np.array(self.data, np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_ref)
        glBufferData(GL_ARRAY_BUFFER, data.ravel(), GL_STATIC_DRAW)

    def create_variable(self, program_id, variable_name):
        variable_id = glGetAttribLocation(program_id, variable_name)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer_ref)
        if self.data_type == "vec3":
            glVertexAttribPointer(variable_id, 3, GL_FLOAT, False, 0, None)
        elif self.data_type == "vec2":
            glVertexAttribPointer(variable_id, 2, GL_FLOAT, False, 0, None)

        glEnableVertexAttribArray(variable_id)
