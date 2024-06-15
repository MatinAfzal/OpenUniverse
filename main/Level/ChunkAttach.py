from pygame import Vector3
from main.Level.Chunk import *
from main.Level.Shematic import Shematic
from main.Engine2.Settings2 import *

class ChunkAttach:
    """
    Attach chunks together !
    - Making Trains !
    """

    def __init__(self, startX=0, startY=0, startZ=0, numberx=1, numberz=1, shader=None, texture=None) -> None:
        if ESP:
            print("Attaching Chunks...")
        self.terrain = []
        self.shader = shader
        self.texture = texture
        self.sx = startX
        self.sy = startY
        self.sz = startZ
        self.endx = numberx * 8 + 1
        self.endz = numberz * 8 + 1
        self.shematic = Shematic(numberx)
        self.sample = self.shematic.locate(0, 0)
        
        self.load_terrain()

    def load_terrain(self):
        if ESP:
            print("Building Chunks (Multiple Level.Chunk Callings)...")
        for x in range(self.sx, self.endx, 8):
            for z in range(self.sz, self.endz, 8):
                self.terrain.append(Chunk(Vector3(x, 0, z), shematic=self.shematic.locate(x, z), material=self.shader,
                                          img=self.texture))
