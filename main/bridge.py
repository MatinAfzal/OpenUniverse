from Engine2.Screen import *
from Engine2.LoadObject import *
from Engine2.Light import *
from Engine2.Material import *
from Engine2.Axes import *
from Engine2.RenderDistance import *
from Engine2.CellAttach import *
from Engine2.Settings2 import *
from Level.ChunkAttach import *
from Level.TreeAttach import *
from Level.Chunk2 import *
from pygame import mixer
from time import sleep

class MultiShaders(Screen):
    
    def __init__(self):
        print("Starting Engine...")
        super().__init__(SCREEN_POS_X, SCREEN_POS_Y, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.plane = None
        self.cube = None
        self.light = None
        self.axes = None
        self.obj_cube = None
        self.img_cube = None
        self.mat = None
        self.seed = 0


    def initialise(self):
        # Variables
        print("Loading Variables...")
        
        # Switching draw types
        self.draw_types = [GL_POINTS, GL_LINES, GL_TRIANGLES]
        self.v_counter = 0
        
        # Switching Cull Face
        self.c_counter = 0
        
        # Switching World axes status
        self.x_counter = 1
        
        # Loads
        print("Loading Files...")
        
        # Shaders
        texturevert = r"texturedvert.vs"
        texturefrag = r"texturedfrag.vs"
        vertexcolvert = r"vertexcolvert.vs"
        vertexcolfrag = r"vertexcolfrag.vs"
        
        # imgs
        self.img_treebase = r"tree_base.png"
        self.img_grass = r"grass.png"
        self.img_texture = r"texture.png"
        self.img_dirt = r"dirt.jpg"
        self.img_icu = r"ICU.png"
        
        # objects
        self.obj_cube = r"cube.obj"
        self.obj_donut = r"donut.obj"
        self.obj_granny = r"granny.obj"
        
        # musics
        self.music_c14 = r"COPY RIGHT!"
        
        # Inits
        print("Loading Inits...")
        # mixer.music.load(self.music_c14)
        # mixer.music.play()
        
        # Shaders
        print("Loading Shaders...")
        self.mat = Material(texturevert, texturefrag)
        axesmat = Material(vertexcolvert, vertexcolfrag)

        # Entity
        print("Loading Entitis...")
        self.axes = Axes(pygame.Vector3(0, 0, 0), axesmat) 
        self.light = Light(pygame.Vector3(0, 0, 0), pygame.Vector3(1, 1, 1), 0)        
        # self.donut = LoadObject(self.obj_donut, self.img_dirt, material=self.mat, location=pygame.Vector3(16, 5, 16))
        self.camera = Camera(self.screen_width, self.screen_height)
        # self.human = LoadObject(self.obj_granny, imagefile=self.img_grass, draw_type=GL_TRIANGLES, material=self.mat, scale=pygame.Vector3(0.02, 0.02, 0.02), location=pygame.Vector3(26, 5, 41))
        self.cube0 = LoadObject(self.obj_cube, imagefile=self.img_icu, draw_type=GL_TRIANGLES, material=self.mat, location=pygame.Vector3(80, 20, 80), scale=pygame.Vector3(8, 8, 8))
          
        # Object Attachs
        self.terrain = ChunkAttach(number=20)
        self.trees = TreeAttach(number=20)
        
        # Cell Attaches
        self.world = CellAttach(self.terrain.terrain, shader=self.mat, image=self.img_texture, chunk=False)
        self.forest = CellAttach(self.trees.forest, shader=self.mat, image=self.img_texture)
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def camera_init(self):
        pass
    
    def display(self):
        # glClearColor(0.5, 0.5 ,0.5, 0.5) # Middle gray
        glClearColor(0.58, 0.85 ,0.94, 0.5) # Sky blue
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        #####
        keys = pygame.key.get_pressed()
        if keys[pygame.K_v]:
            if self.v_counter >= 3:
                self.v_counter = 0
            self.world.world_draw_type = self.draw_types[self.v_counter]
            self.forest.world_draw_type = self.draw_types[self.v_counter]
            print("Draw Type switched...")
            self.world.load_world()
            self.forest.load_world()
            self.v_counter += 1
            sleep(0.3)
            
        if keys[pygame.K_c]:
            if self.c_counter > 1:
                self.c_counter = 0
            
            if self.c_counter == 0:
                print("Cull Face enabled...")
                glEnable(GL_CULL_FACE)
            else:
                print("Cull Face disabled...")
                glDisable(GL_CULL_FACE)
            
            self.c_counter += 1
            sleep(0.3)
            
        if keys[pygame.K_x]:
            self.x_counter += 1
            if self.x_counter > 1:
                self.x_counter = 0
                
            if self.x_counter == 0:
                print("World Center axes enabled...")
            else:
                print("World Center axes disabled...")
            
            sleep(0.3)
        #####
        
        glPointSize(10)
        if self.x_counter == 0:
            self.axes.draw(self.camera, self.light)
        
        #self.world.cell_attachment_update(pygame.Vector3(self.camera.transformation[0, 3], 0, self.camera.transformation[2, 3]))
        self.world.world.draw(self.camera, self.light)
        self.forest.world.draw(self.camera, self.light)
        self.cube0.draw(self.camera, self.light)
        # self.donut.draw(self.camera, self.light)
        # self.human.draw(self.camera, self.light)
        
        self.light.position = pygame.Vector3(self.camera.transformation[0, 3], self.camera.transformation[1, 3], self.camera.transformation[2, 3])
        self.light.update(self.mat.program_id) 
               
        self.light.position = pygame.Vector3(self.camera.transformation[0, 3]+1000, self.camera.transformation[1, 3], self.camera.transformation[2, 3]+1000)
        self.light.update(self.mat.program_id)
        
if __name__ == "__main__":
    MultiShaders().mainloop()
    print("Mainloop Ends...")
    print("\n\n\n")