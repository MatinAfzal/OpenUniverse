from OpenGL.GL import *


class Uniform:
    """Handles OpenGL uniform variables for shaders."""

    def __init__(self, data_type, data):
        """
        Initializes a Uniform object.

        Parameters:
            data_type (str): The type of the uniform variable (e.g., "vec3", "mat4", "sampler2D").
            data: The data to be stored in the uniform variable.
        """
        self.data_type = data_type
        self.data = data
        self.variable_id = None

    def find_variable(self, program_id, variable_name):
        """
        Retrieves the location of the uniform variable in the shader program.

        Parameters:
            program_id (int): The OpenGL program ID.
            variable_name (str): The name of the uniform variable in the shader.
        """
        self.variable_id = glGetUniformLocation(program_id, variable_name)

    def load(self):
        """Uploads the data to the GPU as a uniform variable."""
        if self.data_type == "vec3":
            glUniform3f(self.variable_id, self.data[0], self.data[1], self.data[2])
        elif self.data_type == "mat4":
            glUniformMatrix4fv(self.variable_id, 1, GL_TRUE, self.data)
        elif self.data_type == "sampler2D":
            texture_obj, texture_unit = self.data
            glActiveTexture(GL_TEXTURE0 + texture_unit)
            glBindTexture(GL_TEXTURE_2D, texture_obj)
            glUniform1i(self.variable_id, texture_unit)
