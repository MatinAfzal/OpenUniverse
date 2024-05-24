# This file creates the x, y, z mesh axes of the world in different colors
from .Mesh import *
from .Settings2 import *


class Axes(Mesh):
    """
    World mesh axes x, y, z
    """
    def __init__(self, location, material) -> None:
        print("Loading Axes...")
        vertices = WORLD_AXES_VERTICES
        colors = WORLD_AXES_COLORS
        draw_type = WORLD_AXES_DRAWTYPE
        
        super().__init__(vertices, vertex_colors=colors, draw_type=draw_type, translation=location, material=material)
