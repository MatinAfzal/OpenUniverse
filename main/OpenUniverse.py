import threading
import pygame.mouse
from OpenGL.GL import *
from Engine2.Screen import *
from Engine2.LoadObject import *
from Engine2.Light import *
from Engine2.Material import *
from Engine2.Axes import *
from Engine2.CellAttach import *
from Level.ObjectAttach import *
from Engine2.Cullings.DistanceCulling import *
from Level.Shematic import *
from Level.Chunk import *
from Level.ManualChunkGen import *
from Level.ObjectBuilder import *
from time import sleep
from datetime import datetime
from time import time


class MultiShaders(Screen):

    def __init__(self):
        print("---------------------------------------------------------------------")
        print(BANNER)
        print("Project repo: https://github.com/MatinAfzal/OpenUniverse")
        if ESP:
            print("Starting Engine...")
        else:
            print("ESP (ENGINE_STATUS_PRINT) IS OFF!")

        start = datetime.now()
        print("Starting at:" + str(start.now()))

        print("""
    OpenUniverse Control Guide:
        movement: w - a - s - d
        yaw & pitch: mouse
        world main axes: x  (0.3 second interrupt)
        face culling: c     (0.3 second interrupt)
        view mode: v        (GL_POINTS, GL_LINES, GL_TRIANGLES) (0.3 second interrupt)
        camera info: z      (1 second interrupt)
        light control: l    (Pause, Grab, PLace, Continue) (0.3 second interrupt)
        memory info: m      (1 second interrupt)
        live debugger: F3   (UNAVAILABLE V1.2.3-beta)
        builder mode: b     (0.3 second interrupt)
            - Change block: MouseRightClick
            - Place Block: MouseLeftClick
            - Distance: MouseScroll
        """)

        if ESP:
            print("---Begin of ENGINE_STATUS_PRINT (ESP) logs---")

        # img
        self.img_texture = r"Textures\texture.png"
        self.img_atlas2 = r"Textures\OpenUniverseAtlas-1.png"
        self.img_icu = r"Textures\ICU.png"
        self.img_sun = r"Textures\sun.jpeg"
        self.img_cactus = r"Textures\cactus.png"
        self.image_matin = r"Images\matin_afzal.jpg"
        self.image_monalisa = r"Images\mona_lisa.jpg"
        self.image_dinner = r"Images\the_last_dinner.jpg"

        self.image_makima1 = r"Images\makima1.jpg"
        self.image_makima2 = r"Images\makima2.jpg"
        self.image_kishibe = r"Images\kishibe.jpg"
        self.image_berserk = r"Images\berserk.jpg"
        self.image_luffy = r"Images\luffy.jpg"
        self.image_cicada = r"Images\cicada.jpg"
        self.image_world = r"Images\world.jpg"
        self.image_kishibe2 = r"Images\kishibe2.jpg"
        self.image_kishibe3 = r"Images\kishibe3.jpg"
        self.image_kishibe4 = r"Images\kishibe4.jpg"
        self.image_shanks = r"Images\shanks.jpg"
        self.image_makima10 = r"Images\makima10.jpg"
        self.image_makima11 = r"Images\makima11.jpg"
        self.image_makima12 = r"Images\makima12.jpg"

        super().__init__(SCREEN_POS_X, SCREEN_POS_Y, SCREEN_WIDTH, SCREEN_HEIGHT)

        self.light = None
        self.axes = None
        self.mat = None
        self.seed = 0

        # Switching draw types
        self.draw_types = [GL_POINTS, GL_LINES, GL_TRIANGLES]
        self.v_counter = 0

        # Switching Cull Face
        self.c_counter = 0

        # Switching World axes status
        self.x_counter = 1

        # Moving sun
        self.s_counter = 0

        # Builder mode
        self.b_counter = 0

        self.f3_counter = 0

        # Loads
        if ESP:
            print("Loading Files...")

        # objects
        self.obj_cube = r"Models\cube.obj"
        self.obj_donut = r"Models\donut.obj"

        # Shaders
        texturevert = r"Shaders/texturedvert.vs"
        texturefrag = r"Shaders/texturedfrag.vs"
        vertexcolvert = r"Shaders/vertexcolvert.vs"
        vertexcolfrag = r"Shaders/vertexcolfrag.vs"

        # Shaders
        if ESP:
            print("Loading Shaders...")
        self.mat = Material(texturevert, texturefrag)
        axesmat = Material(vertexcolvert, vertexcolfrag)

        # Entity
        if ESP:
            print("Loading Entities...")
        self.axes = Axes(pygame.Vector3(0, 0, 0), axesmat)
        self.light_pos = pygame.Vector3(INITIAL_LIGHT_POS_X, INITIAL_LIGHT_POS_Y, INITIAL_LIGHT_POS_Z)
        self.light = Light(self.light_pos, pygame.Vector3(1, 1, 1), 0)
        self.camera = Camera(self.screen_width, self.screen_height)
        self.start_time = int(time())

        # Cell Attaches
        cell_start = datetime.now()
        if ESP:
            print("Cell Attach started at:" + str(cell_start.now()))

    def initialise(self):
        # Variables
        if ESP:
            print("Loading Variables...")

        cell_end = datetime.now()
        if ESP:
            print("Cell Attach ended at:" + str(cell_end.now()))

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def camera_init(self):
        pass

    def display(self):
        if SKY_DYNAMIC:
            glClearColor(self.red, self.green, self.blue, self.alpha)  # Sky night
        else:
            glClearColor(0.58, 0.85, 0.94, 0.5)  # Sky blue

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # #####################RENDER#######################
        self.axes.draw(self.camera, self.light)
        # #####################RENDER#######################

        keys = pygame.key.get_pressed()
        if keys[pygame.K_v]:
            if self.v_counter >= 3:
                self.v_counter = 0
            try:
                pass
                if ESP:
                    print("Draw Type switched...")
            except:
                pass
            try:
                pass
            except:
                pass
            self.v_counter += 1
            sleep(0.3)

        if keys[pygame.K_c]:
            if self.c_counter > 1:
                self.c_counter = 0

            if self.c_counter == 0:
                if ESP:
                    print("Cull Face enabled...")
                glEnable(GL_CULL_FACE)

            else:
                if ESP:
                    print("Cull Face disabled...")
                glDisable(GL_CULL_FACE)

            self.c_counter += 1
            sleep(0.3)

        if keys[pygame.K_x]:
            self.x_counter += 1
            if self.x_counter > 1:
                self.x_counter = 0

            if self.x_counter == 0:
                if ESP:
                    print("World Center axes enabled...")
            else:
                if ESP:
                    print("World Center axes disabled...")

            sleep(0.3)

        if keys[pygame.K_l]:
            if self.s_counter >= 3:
                self.s_counter = 0
            else:
                self.s_counter += 1

            sleep(0.3)

        if keys[pygame.K_b]:
            if self.b_counter >= 1:
                self.b_counter = 0
                self.object_build_status = False
                if ESP:
                    print("Builder mode disabled...")
            else:
                self.b_counter += 1
                self.camera.camera_distance = -10
                if ESP:
                    print("World Center axes enabled...")

            sleep(0.3)

        if keys[pygame.K_F3]:
            if self.f3_counter >= 1:
                self.f3_counter = 0
                if ESP:
                    print("Debugger mode disabled...")
            else:
                self.f3_counter += 1
                if ESP:
                    print("Debugger mode enabled...")

            sleep(0.3)


if __name__ == "__main__":
    MultiShaders().mainloop()
    if ESP:
        print("Mainloop Ends...")
    if ESP:
        print("---End of ENGINE_STATUS_PRINT (ESP) logs---")
    end = datetime.now()
    print("Ended at:" + str(end.now()))
    print("---------------------------------------------------------------------")
    print("\n\n")
