# This file prepares the page with initial processing settings and executes the main loop
import datetime
import os
from pygame.locals import *
from .Camera import *
from .Settings2 import *
from .Utils import *


class Screen:
    """
    Sceeen initialization
    """
    def __init__(self, screen_posX, screen_posY, screen_width, screen_height):
        print("Loading Screen...")
        # program window position init
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screen_posX, screen_posY)
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.start_time = datetime.datetime.now()
        self.stop_time = None
        
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24) # GPU DEPTH BUFFER SIZE
        
        self.screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption(SCREEN_CAPTION_LOADING)
        self.clock = pygame.time.Clock()
        self.camera = None
        self.program_id = None
        self.fps_list = []

    def engine_fps(self) -> None:
        """
        Live fps counter
        """

        fps = str(int(self.clock.get_fps()))
        self.fps_list.append(int(fps))

        pygame.display.set_caption(f"FPS: {fps} {SCREEN_CAPTION}")

    def engine_shutdown(self):
        """
        Shots the engine down
        """

        self.stop_time = datetime.datetime.now()
        save_report(self.fps_list, self.start_time, self.stop_time, time_based=False)
        self.run = False

    def initialise(self):
        pass

    def display(self):
        pass

    def camera_init(self):
        pass

    def mainloop(self):
        run = True
        self.initialise()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.engine_shutdown()
                    run = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.mouse.set_visible(True)
                        pygame.event.set_grab(False)
                    if event.key == K_SPACE:
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)

            self.camera_init()
            self.display()
            self.engine_fps()
            pygame.display.flip()
            self.clock.tick(SCREEN_MAX_FPS)
        pygame.quit()
