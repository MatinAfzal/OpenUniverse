from .Chunk import *
from pygame import Vector3
from .Shematic import Shematic
import numpy as np


class ChunkAttach:
    """
    Attach chunks togther !
    - Making Trrains !
    """
    
    def __init__(self, startX=0, startY=0, startZ=0, number=4) -> None:
        print("Attaching Chunks...")
        self.terrain = []
        self.sx = startX
        self.sy = startY
        self.sz = startZ
        self.number = number
        self.endx = number * 8
        self.endz = number * 8
        self._deufalt_shematic = np.ones(shape=(8,8,1)) * 8
        self.shematic = Shematic(number)
        self.sample = self.shematic.locate(0, 0)
        
        self.load_terrain()
          
          
    def load_terrain(self):
        print("Building Chunks (Multiple Level.Chunk Callings)...")
        # self.shematic.graph() # Showing perlin noise 100x100 grid.
        sample = self.shematic.locate(0, 0)
        for x in range(self.sx, self.endx, 8):
            for z in range(self.sz, self.endz, 8):
                self.terrain.append(Chunk(Vector3(x, 0, z), shematic=self.shematic.locate(x, z), debug=False, test_sample=(self.sample, 0, 0)))