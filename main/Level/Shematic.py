import numpy as np
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise


class Shematic:
    def __init__(self, chunks) -> None:
        self.x_max = 8
        self.y_max = 1
        self.z_max = 8
        self.repeat = self.x_max * self.y_max * self.z_max
        self.chunks = chunks
        self.width = self.chunks * 8
        self.height = self.chunks * 8
        # self.terrain_shematic = self.terrain_maker() * 20
        self.terrain_shematic = self.load_gen()
    
    def terrain_maker(self):
        noise = PerlinNoise(octaves=4, seed=100)
        zpix, xpix = self.height, self.width
        terrain = np.zeros(shape=(self.height, self.width))
        
        for z in range(zpix):
            for x in range(xpix):       
                    noise_value = noise([z/zpix, x/xpix])
                    terrain[z][x] = noise_value
          
        return terrain.copy()
    
    def gen_save(self):
        noise = PerlinNoise(octaves=35, seed=100)
        zpix, xpix = 400, 400
        terrain = np.zeros(shape=(800, 800))
        
        for z in range(zpix):
            for x in range(xpix):       
                    noise_value = noise([z/zpix, x/xpix])
                    terrain[z][x] = noise_value * 20
                    
        np.savetxt("world.txt", terrain)
        
    def load_gen(self):
        return np.loadtxt(r"Saves\world.txt")
    
    def locate(self, x, z):
        result = self.terrain_shematic[x:x+8, z:z+8]
        return result
    
    def graph(self):
        plt.imshow(self.terrain_shematic[0:100, 0:100], cmap="gray")
        plt.show()
        
# if __name__ == "__main__":
#     sh = Shematic(4)
#     sh.gen_save()
