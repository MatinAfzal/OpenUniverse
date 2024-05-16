import pygame

from Engine2.Screen import *
from Engine2.LoadObject import *
from Engine2.Light import *
from Engine2.Material import *
from Engine2.Axes import *
from Engine2.CellAttach import *
from Engine2.Settings2 import *
from Level.ChunkAttach import *
from Level.TreeAttach import *
from Level.Chunk2 import *
from pygame import mixer
from time import sleep
from datetime import datetime

class MultiShaders(Screen):
    
    def __init__(self):
        print("Starting Engine...")
        start = datetime.now()
        print("Starting at:" + str(start.now()))

        super().__init__(SCREEN_POS_X, SCREEN_POS_Y, SCREEN_WIDTH, SCREEN_HEIGHT)

        self.plane = None
        self.cube = None
        self.light = None
        self.axes = None
        self.obj_cube = None
        self.img_cube = None
        self.mat = None
        self.draw_types = None
        self.v_counter = None
        self.c_counter = None
        self.x_counter = None

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
        texturevert = r"shaders\texturedvert.vs"
        texturefrag = r"shaders/texturedfrag.vs"
        vertexcolvert = r"shaders/vertexcolvert.vs"
        vertexcolfrag = r"shaders/vertexcolfrag.vs"
        
        # imgs
        self.img_texture = r"images\texture.png"
        self.img_icu = r"images\ICU.png"
        
        # objects
        self.obj_cube = r"models\cube.obj"
        self.obj_donut = r"models\donut.obj"
        self.obj_granny = r"models\granny.obj"

        
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
        self.light_pos = pygame.Vector3(20, 30, 20)
        self.lightbolb_pos = pygame.Vector3(self.light_pos.x, self.light_pos.y + 5, self.light_pos.z)
        self.light = Light(self.light_pos, pygame.Vector3(1, 1, 1), 0)
        # self.donut = LoadObject(self.obj_donut, self.img_cube, material=self.mat, location=pygame.Vector3(16, 5, 16))
        self.camera = Camera(self.screen_width, self.screen_height)
        # self.human = LoadObject(self.obj_granny, imagefile=self.img_grass, draw_type=GL_TRIANGLES, material=self.mat, scale=pygame.Vector3(0.02, 0.02, 0.02), location=pygame.Vector3(26, 5, 41))
        self.cube0 = LoadObject(self.obj_cube, imagefile=self.img_icu, draw_type=GL_TRIANGLES, material=self.mat, location=self.lightbolb_pos, scale=pygame.Vector3(8, 8, 8))

        # Object Attachs
        self.terrain = ChunkAttach(number=7)
        self.trees = TreeAttach(number=7)
        
        # Cell Attaches
        cell_start = datetime.now()
        print("Cell Attach started at:" + str(cell_start.now()))

        self.world = CellAttach(self.terrain.terrain, shader=self.mat, image=self.img_texture, chunk=False)
        self.forest = CellAttach(self.trees.forest, shader=self.mat, image=self.img_texture)

        cell_end = datetime.now()
        print("Cell Attach ended at:" + str(cell_end.now()))
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glLight

        # light = [self.light_pos.x, self.light_pos.y, self.light_pos.z, 0.0]
        # glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0, 0, -1])

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

        # self.light.position = pygame.Vector3(self.light_pos.x, self.light_pos.y, self.light_pos.z)
        # self.light.update(self.mat.program_id)

        # self.light.position = pygame.Vector3(-self.light_pos.x, self.light_pos.y, -self.light_pos.z)
        # self.light.update(self.mat.program_id)
        
if __name__ == "__main__":
    MultiShaders().mainloop()
    print("Mainloop Ends...")
    end = datetime.now()
    print("Ended at:" + str(end.now()))
    print("\n\n\n")