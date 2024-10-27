import pygame
from .Transformations import *
from .Uniform import *
from .Settings2 import *


class Light:
    """
    Represents a light source in the 3D scene.

    This class manages the position and color of a light source, and updates
    the corresponding shader variables to ensure correct lighting effects in
    the rendered scene.

    Attributes:
        transformation (np.ndarray): The transformation matrix for the light source.
        position (pygame.Vector3): The position of the light in 3D space.
        color (pygame.Vector3): The color of the light, represented as RGB values.
        light_variable (str): The shader variable name for the light's position.
        color_variable (str): The shader variable name for the light's color.

    Parameters:
        position (pygame.Vector3): The initial position of the light source in 3D space (default is (0, 0, 0)).
        color (pygame.Vector3): The color of the light (default is white (1, 1, 1)).
        light_number (int): The index of the light, used for naming the shader variables (default is 0).

    Methods:
        update(program_id) -> None:
            Updates the light's position and color in the shader program specified by program_id.

    Notes:
        - The class assumes that the lighting data in the shader is structured as an array
          where each light's position and color can be indexed using the light_number.
        - Ensure the shader program is active before calling the update method.
    """
    def __init__(self, position=pygame.Vector3(0, 0, 0), color=pygame.Vector3(1, 1, 1), light_number=0):
        if ESP:
            print("Loading light...")
        self.transformation = identity_mat()
        self.position = position
        self.color = color
        self.light_variable = "light_data[" + str(light_number) + "].position"
        self.color_variable = "light_data[" + str(light_number) + "].color"

    def update(self, program_id):
        light_pos = Uniform("vec3", self.position)
        light_pos.find_variable(program_id, self.light_variable)
        light_pos.load()
        color = Uniform("vec3", self.color)
        color.find_variable(program_id, self.color_variable)
        color.load()
