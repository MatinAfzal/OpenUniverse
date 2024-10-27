from .Mesh import *
from .Settings2 import *


class Axes(Mesh):
    """
    Represents the 3D axes of the world (X, Y, Z) as a mesh with customizable colors.

    Parameters:
        location (tuple): The coordinates where the axes will be positioned in the 3D space.
        shader (str): The shader to be applied to the axes mesh.

    Notes:
        - The axes are rendered with predefined vertices and colors defined in the `Settings2` module.
        - Debugging information is printed if the `ESP` variable is set to True.
    """

    def __init__(self, location, shader) -> None:
        if ESP:
            print("Loading Axes...")
        vertices = WORLD_AXES_VERTICES
        colors = WORLD_AXES_COLORS
        draw_type = WORLD_AXES_DRAWTYPE

        super().__init__(vertices, vertex_colors=colors, draw_type=draw_type, translation=location, material=shader)
