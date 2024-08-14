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
        if ESP:
            print("Starting Engine...")
        else:
            print("ESP (ENGINE_STATUS_PRINT) IS OFF!")
        print("Project repo: https://github.com/MatinAfzal/OpenUniverse")

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
        builder mode: b     (0.3 second interrupt)
            - Change block: MouseRightClick
            - Place Block: MouseLeftClick
            - Distance: MouseScroll
        """)

        # Object Attach
        self.trees = None
        self.terrain = None
        self.threading()

        super().__init__(SCREEN_POS_X, SCREEN_POS_Y, SCREEN_WIDTH, SCREEN_HEIGHT)

        self.plane = None
        self.cube = None
        self.light = None
        self.axes = None
        self.obj_cube = None
        self.img_cube = None
        self.mat = None
        self.seed = 0

        # Class init
        self.culling_distance = DistanceCulling(distance=DCD)
        # self.shematic = Shematic(1)

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

        # img
        self.img_texture = r"Textures\texture.png"
        self.img_atlas2 = r"Textures\OpenUniverseAtlas-1.png"
        self.img_icu = r"Textures\ICU.png"
        self.img_sun = r"Textures\sun.jpeg"
        self.img_cactus = r"Textures\cactus.png"
        self.image_matin = r"Images\matin_afzal.jpg"
        self.image_monalisa = r"Images\mona_lisa.jpg"
        self.image_dinner = r"Images\the_last_dinner.jpg"

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
        self.lightbolb_pos = pygame.Vector3(self.light_pos.x, self.light_pos.y + 5, self.light_pos.z)
        self.light = Light(self.light_pos, pygame.Vector3(1, 1, 1), 0)
        self.camera = Camera(self.screen_width, self.screen_height)
        self.camera_pos = self.get_cam_pos()
        self.cube0 = LoadObject(
            self.obj_cube, imagefile=self.img_sun, draw_type=GL_TRIANGLES, material=self.mat,
            location=self.lightbolb_pos, scale=pygame.Vector3(8, 8, 8))
        self.start_time = int(time())

        # Attaching objects before super initial to avoid screen crashes

        # Object Attach
        # self.trees = None
        # self.terrain = None
        # self.threading()
        # self.terrain = ObjectAttach(object_name="chunk", object_type="desert", number_x=10, number_z=10)
        # self.trees = ObjectAttach(object_name="cactus", number_x=10, number_z=10)

        # Cell Attaches
        cell_start = datetime.now()
        if ESP:
            print("Cell Attach started at:" + str(cell_start.now()))
        self.forest = CellAttach(self.trees.layer, shader=self.mat, image=self.img_texture)
        self.world = CellAttach(self.terrain.layer, shader=self.mat, image=self.img_texture)
        # self.world = CellAttach(self.terrain.layer, shader=self.mat, image=self.img_atlas2)

        # self.forest = CellAttach(self.trees.layer, shader=self.mat, image=self.img_cactus)
        # self.chunk = Chunk(biome="jungle", position=Vector3(0, 0, 0), img=self.img_texture, material=self.mat)

        # Sky variables
        self.sky_cycle_lock = False
        self.sun_cycle_lock = False
        self.red = 0.0
        self.green = 0.0
        self.blue = 0.0
        self.alpha = 0.5

        # Object control variables
        self.object_grab = False
        self.build_object = None
        self.distance_reset_lock = False

        # Locks
        self.object_creation_0 = False  # Avoiding memory overflow.

    def threading(self):
        t1 = threading.Thread(target=self.tree_thread_)
        t2 = threading.Thread(target=self.terrain_thread_())

        t1.start()
        t2.start()

        t1.join()
        t2.join()

    def tree_thread_(self):
        self.trees = ObjectAttach(object_name="tree", number_x=TREES, number_z=TREES)

    def terrain_thread_(self):
        self.terrain = ObjectAttach(object_name="chunk", object_type="jungle", number_x=CHUNKS, number_z=CHUNKS)

    def superflat_thread_(self):
        self.terrain = ObjectAttach(object_name="chunk", object_type="superflat", number_x=CHUNKS, number_z=CHUNKS)

    def image_thread_(self):
        self.terrain = ObjectAttach(object_name="image", texture=self.image_matin)

    def get_cam_pos(self):
        return int(self.camera.transformation[0, 3]), int(self.camera.transformation[2, 3])

    def builder_handler(self, block):
        self.build_object = ObjectBuilder(object_type=block, translation=self.camera.target,
                                          shader=self.mat)
        self.object_build_status = True
        self.object_grab = True

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
        # glClearColor(0.5, 0.5 ,0.5, 0.5) # Middle gray
        # glClearColor(0.58, 0.85, 0.94, 0.5)  # Sky blue
        if SKY_DYNAMIC:
            glClearColor(self.red, self.green, self.blue, self.alpha)  # Sky night
        else:
            glClearColor(0.58, 0.85, 0.94, 0.5)  # Sky blue
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #####
        keys = pygame.key.get_pressed()
        if keys[pygame.K_v]:
            if self.v_counter >= 3:
                self.v_counter = 0
            try:
                self.world.world_draw_type = self.draw_types[self.v_counter]
                self.forest.world_draw_type = self.draw_types[self.v_counter]
                if ESP:
                    print("Draw Type switched...")
            except:
                pass
            try:
                self.world.load_world()
                self.forest.load_world()
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

        # #####################RENDER#######################
        glPointSize(10)
        if self.x_counter == 0:
            self.axes.draw(self.camera, self.light)

        try:
            self.world.world.draw(self.camera, self.light)
            self.forest.world.draw(self.camera, self.light)
        except:
            pass

        for build in self.builded_objects:
            try:
                build.object.draw(self.camera, self.light)
            except:
                continue

        self.cube0.draw(self.camera, self.light)

        # #####################RENDER#######################

        # #####################SUN&SKY######################

        now = int(time())
        current_time = self.start_time - now

        if current_time % 1 == 0 and SKY_DYNAMIC:
            if self.green >= 1 and self.blue >= 1:
                self.sky_cycle_lock = True

            if not self.sky_cycle_lock:
                self.red = 0
                self.green += SKY_SPEED
                self.blue += SKY_SPEED

            if self.sky_cycle_lock:
                self.red = 0
                self.green -= SKY_SPEED
                self.blue -= SKY_SPEED

                if self.green <= 0 and self.blue <= 0:
                    self.sky_cycle_lock = False

        if current_time % 1 == 0 and self.s_counter == 0 and SUN_STATUS:  # Move
            if self.light_pos.y < 120 and self.light_pos.x < 300 and not self.sun_cycle_lock:
                self.light_pos.y += SUN_SPEED_Y
            elif self.light_pos.y >= 120 and self.light_pos.x < 300 and not self.sun_cycle_lock:
                self.light_pos.x += SUN_SPEED_X
            elif self.light_pos.y >= 118 and self.light_pos.x >= 298 and not self.sun_cycle_lock:
                self.sun_cycle_lock = True
            elif self.sun_cycle_lock:
                if self.light_pos.y <= -60 and self.sun_cycle_lock:
                    self.light_pos = Vector3(INITIAL_LIGHT_POS_X, INITIAL_LIGHT_POS_Y, INITIAL_LIGHT_POS_Z)
                    self.sun_cycle_lock = False
                else:
                    self.light_pos.y -= SUN_SPEED_Y

            self.lightbolb_pos = self.light_pos
            self.cube0.update(translation=self.lightbolb_pos, scale=pygame.Vector3(8, 8, 8))
            self.light.position = pygame.Vector3(self.light_pos.x, self.light_pos.y, self.light_pos.z)
            self.light.update(self.mat.program_id)

        if self.s_counter == 2:  # Grab
            self.distance_reset_lock = False
            self.cube0.update(translation=self.camera.target)
            self.object_grab = True
            self.object_creation_0 = True

        elif self.s_counter in [1, 3] and not self.distance_reset_lock:  # Pause
            self.distance_reset_lock = True
            self.object_grab = False
            self.camera.camera_distance = -10

        # #####################SUN&SKY######################

        # ##################ObjectBuilder###################

        if self.b_counter == 1:
            # self.mouse_wheel = 0
            if self.right_click == 0 and not self.object_build_status:
                self.builder_handler("crate")

            if self.right_click == 1 and not self.object_build_status:
                self.builder_handler("wood")

            if self.right_click == 2 and not self.object_build_status:
                self.builder_handler("brick")

            if self.right_click == 3 and not self.object_build_status:
                self.builder_handler("glass")

            if self.right_click == 4 and not self.object_build_status:
                self.builder_handler("library")

            if self.right_click == 5 and not self.object_build_status:
                self.builder_handler("tnt")

            if self.right_click == 6 and not self.object_build_status:
                self.builder_handler("prison")

            if self.right_click == 7 and not self.object_build_status:
                self.builder_handler("metal")

            if self.right_click == 7 and not self.object_build_status:
                self.builder_handler("?")

            if self.object_build_status:
                try:
                    self.build_object.update(translation=self.camera.target)
                    self.build_object.object.draw(self.camera, self.light)
                finally:
                    pass

        # ##################ObjectBuilder###################


if __name__ == "__main__":
    MultiShaders().mainloop()
    if ESP:
        print("Mainloop Ends...")
    end = datetime.now()
    print("Ended at:" + str(end.now()))
    print("---------------------------------------------------------------------")
    print("\n\n")
