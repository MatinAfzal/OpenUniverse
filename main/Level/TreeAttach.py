import random
from main.Level.Tree import *
from pygame import Vector3
from main.Level.Shematic import Shematic


class TreeAttach:
    """
    Attach Trees together !
    - Making Forests !
    """
    
    def __init__(self, startX=0, startY=0, startZ=0, numberx=1, numberz= 1, shader=None, texture=None) -> None:
        print("Attaching Trees...")
        self.forest = []
        self.shader = shader
        self.texture = texture
        self.sx = startX
        self.sy = startY
        self.sz = startZ
        self.end = numberx * 8 + 1
        self.end = numberz * 8 + 1
        self.shematic = Shematic(numberx)
        
        random.seed(100)
        self.load_forest()
        
    
    def load_forest(self):
        print("Building Trees (Multiple Level.Trees Callings)...")
        for x in range(self.sx, self.end, 8):
            for z in range(self.sz, self.end, 8):
                y = int(self.shematic.locate(x, z)[3][3])
                if y <= 0 or y >= 15:
                    continue
                else:
                    if random.randint(0, 2) in [0, 1]:
                        self.forest.append(Tree(Vector3(x, 0, z), shematic=self.shematic.locate(x, z)))
