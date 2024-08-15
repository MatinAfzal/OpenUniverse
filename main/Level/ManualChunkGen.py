import numpy as np
from perlin_noise import PerlinNoise
from pygame import Vector3
from Level.Chunk import *
from Level.Shematic import Shematic
from Engine2.Settings2 import *


class ManualChunkGen:
    """
    creates chunk manually by coordinates.
    """

    def __init__(self, seed: int = 100, octaves: int = 20, multiplier: int = 20, texture: any = None,
                 material: any = None):

        self.seed = seed
        self.octaves = octaves
        self.world_border = WORLD_BORDER
        self.noise = PerlinNoise(octaves=self.octaves, seed=self.seed)
        self.height_multiplier = multiplier
        self.texture = texture
        self.material = material
        self.shematic = Shematic()

    def generate(self, x: int = 0, z: int = 0, i: int = 0):
        # main_x = x
        # main_z = z
        # shematic = np.zeros(shape=(8, 8))
        # for i in range(8):
        #     for j in range(8):
        #         shematic[i][j] = self.noise.noise([i+z/self.world_border, j+x/self.world_border, ])
        #         * self.height_multiplier
        #
        # shematic = shematic.astype(str).astype(float).astype(int)

        shematic = self.shematic.locate(x, z)

        chunk = Chunk(biome="jungle", position=Vector3(x, 0, z), shematic=shematic, img=self.texture,
                      material=self.material)

        chunk.index_key = i

        return chunk
