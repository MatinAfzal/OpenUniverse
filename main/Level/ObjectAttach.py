from random import randint
from pygame import Vector3
from Level.Chunk import *
from Level.Tree import *
from Level.Cactus import *
from Level.Shematic import Shematic
from Engine2.Settings2 import *


class ObjectAttach:
    """
    Attach objects together !
    """

    def __init__(self, object_name="chunk", object_type="", start_x=0, start_y=0, start_z=0, number_x=1, number_z=1,
                 shader=None, texture=None) -> None:
        if ESP:
            print("Attaching Objects...")

        self.known_objects = ["chunk", "tree", "cactus"]
        self.object_name = object_name
        self.object_type = object_type
        self.layer = []
        self.shader = shader
        self.texture = texture
        self.sx = start_x
        self.sy = start_y
        self.sz = start_z
        self.end_x = number_x * 8 + 1
        self.end_z = number_z * 8 + 1
        self.shematic = Shematic(number_x)
        self.sample = self.shematic.locate(0, 0)

        if self.object_name not in self.known_objects:
            if ESP:
                print("A binding method is not specified for this object, use force=True to use default method!")
        if self.object_name == "chunk":
            self.chunk_binding()
        elif self.object_name == "tree":
            self.tree_binding()
        elif object_name == "cactus":
            self.cactus_binding()
        else:
            # Impossible to reach!
            pass

    def chunk_binding(self):
        if ESP:
            print("Building Chunks (Multiple Level.Chunk Callings)...")
        for x in range(self.sx, self.end_x, 8):
            for z in range(self.sz, self.end_z, 8):
                self.layer.append(Chunk(biome=self.object_type, position=Vector3(x, 0, z),
                                        shematic=self.shematic.locate(x, z), material=self.shader, img=self.texture))

    def tree_binding(self):
        if ESP:
            print("Building Trees (Multiple Level.Trees Callings)...")
        for x in range(self.sx, self.end_x, 8):
            for z in range(self.sz, self.end_z, 8):
                y = int(self.shematic.locate(x, z)[3][3])
                if y <= 0 or y >= 15:
                    continue
                else:
                    if randint(0, 2) in [0, 1]:
                        self.layer.append(Tree(Vector3(x, 0, z), shematic=self.shematic.locate(x, z)))

    def cactus_binding(self):
        if ESP:
            print("Building Cactus's (Multiple Leve.Cactus Callings)...")
        for x in range(self.sx, self.end_x, 8):
            for z in range(self.sz, self.end_z, 8):
                y = int(self.shematic.locate(x, z)[3][3])
                if y <= 0 or y >= 15:
                    continue
                else:
                    if randint(0, 2) in [0, 1]:
                        self.layer.append(Cactus(Vector3(x, 0, z), shematic=self.shematic.locate(x, z)))
