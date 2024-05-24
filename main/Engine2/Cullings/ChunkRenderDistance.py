import numpy as np

class ChunkRenderDistance:
    def __init__(self, renderdistance=1) -> None:
        self.render_distance = renderdistance # Chunks
        self.maximum_distance = 500
        self.block_distance = self.render_distance * 8 # Blocks
        
        self.load_map = None
        self.init_map()
        
        # self.player_location = [int(round(self.maximum_distance / 2)), int(round(self.maximum_distance / 2))]
        self.player_location = [0, 0]
        self.player_identifier = 5 # Player identifier
        
    def first_load(self):
        self.load_map[self.player_location[0]][self.player_location[1]] = self.player_identifier # initilaise player on chunk map
        
        # Render Cross One
        self.load_map[self.player_location[0]:self.player_location[0]+self.block_distance, self.player_location[1]:self.player_location[1]+self.block_distance] = 1 # BR
        self.load_map[self.player_location[0]-self.block_distance:self.player_location[0], self.player_location[1]-self.block_distance:self.player_location[1]] = 1 # TL
        
        
        # Render Cross Two
        self.load_map[self.player_location[0]:self.player_location[0]+self.block_distance, self.player_location[1]-self.block_distance:self.player_location[1]] = 1 # BL
        self.load_map[self.player_location[0]-self.block_distance:self.player_location[0], self.player_location[1]:self.player_location[1]+self.block_distance] = 1 # TR

    def init_map(self):
        self.load_map = np.zeros(shape=(self.maximum_distance, self.maximum_distance), dtype=np.uint8)
      
    def update_load_map(self, direction):
        """ updating new load map based on player direction.

        Args:
            direction (tuple): player new direction
            
        Sample:
            (X, Y, Z, W): X Croos One, Y Cross One, Z Cross Two, W Cross Two
            (1, 0, 0, 0): Positive move on X Croos One
            (0, 0, -1, 0): Negative move on Z Cross Two
        """
        
        triger = 0 # Stay
        try:
            triger = 1
            positive = direction.index(1)
        except:
            triger = 2
            negative = direction.index(-1)
            
        # Positive move
        if triger == 1:
            self.init_map()
            
            # Cross One X & Y
            if positive == 0: # X Croos One (Right Column Move)
                self.player_location[1] += 1
                self.first_load()
            
            elif positive == 1: # Y Croos One (Up Row Move)
                self.player_location[0] -= 1
                self.first_load()
                
            # Cross Two Z & W
            elif positive == 2: # Z Cross Two (Right up column and row move)
                self.player_location[0] -= 1
                self.player_location[1] += 1
                self.first_load()
            
            elif positive == 3: # W Cross Two (Left up column and row move)
                self.player_location[0] -= 1
                self.player_location[1] -= 1
                self.first_load()
        
        # Negative Move
        elif triger == 2:
            self.init_map()
            # Cross One X & Y
            if negative == 0: # -X Cross One (Left Column Move)
                self.player_location[1] -= 1
                self.first_load()
            
            elif negative == 1: # -Y Cross One (Down Row Move)
                self.player_location[0] += 1
                self.first_load()

            # Cross Two Z & W
            elif negative == 2: # -Z Cross Two (Down left row and column move)
                self.player_location[0] += 1
                self.player_location[1] -= 1
                self.first_load()
            
            elif negative == 3: # -W Cross Two (Down right row and column move)
                self.player_location[0] += 1
                self.player_location[1] += 1
                self.first_load()
        
        else:
            pass
                
# if __name__ == "__main__":
#     map = ChunkRenderDistance()
#     map.first_load()
#     print(map.load_map)
#     print("\n\n\n\n")
#     map.update_load_map(direction=(0, 0, 0, -1))

#     print(map.load_map)
    