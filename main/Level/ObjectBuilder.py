import pygame
from OpenGL.GL import GL_TRIANGLES
from Engine2.LoadObject import *
from Engine2.Transformations import Rotation
from Engine2.Settings2 import *


class ObjectBuilder:
    def __init__(self, object_name="block", object_type="crate", translation=pygame.Vector3(0, 0, 0),
                 rotation=Rotation(0, pygame.Vector3(0, 1, 0)), scale=pygame.Vector3(1, 1, 1),
                 shader=None):
        self.know_object_types = ["crate", "wood", "brick", "glass", "tnt", "library", "?", "prison", "metal",
                                  "white_wool", "black_wool", "dark_wool", "gray_wool", "red_wool", "green_wool",
                                  "blue_wool", "yellow_wool", "orange_wool", "pink_wool", "brown_wool"]
        self.know_objects = ["block"]
        self.know_objects_types = []
        self.object_name = object_name  # Later for different objects rater the blocks
        self.object_type = object_type
        self.translation = translation
        self.rotation = rotation
        self.scale = scale
        self.shader = shader
        self.texture = None

        # Instance
        self.object = None

        # Object models
        self.obj_cube = r"Models\cube.obj"

        # Textures
        self.texture_crate = r"Textures\crate.png"
        self.texture_wood = r"Textures\default_aspen_wood.png"
        self.texture_brick = r"Textures\brickwall.jpg"
        self.texture_glass = r"Textures\default_obsidian_glass.png"
        self.texture_tnt = r"Textures\tnt_side.png"
        self.texture_library = r"Textures\default_bookshelf.png"
        self.texture_unknown = r"Textures\unknown_node.png"
        self.texture_prison = r"Textures\doors_trapdoor_steel.png"
        self.texture_metal = r"Textures\xpanes_bar_top.png"

        self.texture_white_wool = r"Textures\wool_white.png"
        self.texture_black_wool = r"Textures\wool_black.png"
        self.texture_dark_wool = r"Textures\wool_dark_gray.png"
        self.texture_gray_wool = r"Textures\wool_dark_gray.png"
        self.texture_red_wool = r"Textures\wool_blue.png"
        self.texture_green_wool = r"Textures\wool_green.png"
        self.texture_dark_green_wool = r"Textures\wool_dark_green.png"
        self.texture_blue_wool = r"Textures\wool_blue.png"
        self.texture_yellow_wool = r"Textures\wool_yellow.png"
        self.texture_orange_wool = r"Textures\wool_orange.png"
        self.texture_pink_wool = r"Textures\wool_pink.png"
        self.texture_brown_wool = r"Textures\wool_brown.png"

        self.object_type_dict = {
            "crate": self.texture_crate,
            "wood": self.texture_wood,
            "brick": self.texture_brick,
            "glass": self.texture_glass,
            "library": self.texture_library,
            "tnt": self.texture_tnt,
            "?": self.texture_unknown,
            "prison": self.texture_prison,
            "metal": self.texture_metal,

            "white_wool": self.texture_white_wool,
            "black_wool": self.texture_black_wool,
            "dark_wool": self.texture_dark_wool,
            "gray_wool": self.texture_gray_wool,
            "red_wool": self.texture_red_wool,
            "green_wool": self.texture_green_wool,
            "dark_green_wool": self.texture_dark_green_wool,
            "blue_wool": self.texture_blue_wool,
            "yellow_wool": self.texture_yellow_wool,
            "orange_wool": self.texture_orange_wool,
            "pink_wool": self.texture_pink_wool,
            "brown_wool": self.texture_brown_wool
        }

        if self.object_type in self.know_object_types:
            self.object = LoadObject(self.obj_cube, imagefile=self.object_type_dict.get(self.object_type),
                                     draw_type=GL_TRIANGLES, material=self.shader, location=self.translation,
                                     scale=self.scale)
        else:
            if ESP:
                print("ERROR: ObjectBuilder object_type is not known!")

    def update(self, translation=pygame.Vector3(0, 0, 0), rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
               scale=pygame.Vector3(1, 1, 1)):

        if self.object is not None:
            self.object.update(translation, rotation, scale)

        else:
            if ESP:
                print("ERROR: ObjectBuilder object not create yet!")
