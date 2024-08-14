# This file prepares the page with initial processing settings and executes the main loop
import os
import time
import pygame
from time import sleep
from pygame.locals import *
from .Camera import *
from .Settings2 import *
from .Utils import *
from Test.TestSite import *
from datetime import datetime


class Screen:
    """
    Screen initialization
    """
    def __init__(self, screen_posX, screen_posY, screen_width, screen_height):
        self.run = True
        self.test_site = None
        if ESP:
            print("Loading Screen...")
        if TSS:
            self.test_site = TestSite(action="test")

        # program window position init
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screen_posX, screen_posY)
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.start_time = datetime.now()
        self.stop_time = None
        
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, SCREEN_DEPTH_SIZE)  # GPU DEPTH BUFFER SIZE
        
        self.screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL, pygame.FULLSCREEN)

        pygame.display.set_caption(SCREEN_CAPTION_LOADING)
        self.clock = pygame.time.Clock()
        self.camera = None
        self.program_id = None
        self.fps_list = []

        # Object control variables
        self.builded_objects = []
        self.mouse_wheel = 0
        self.right_click = 0
        self.object_build_status = False

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

        self.stop_time = datetime.now()
        if TSS:
            self.test_site.fps_test(self.fps_list)
        if ENGINE_REPORT_SAVE:
            result, error_type = save_report(self.fps_list, self.start_time, self.stop_time, time_based=ERT_B)
            if result == 0 and ESP:
                print("ERROR: Failed to save engine report!")
                if ESP_VV:
                    print("ESP_VV -> ", error_type)
        if TSS:
            self.test_site.after()
        self.run = False

    def initialise(self):
        pass

    def display(self):
        pass

    def camera_init(self):
        pass

    def mainloop(self):
        self.initialise()
        if TSS:
            self.test_site.ready()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.engine_shutdown()
                    self.run = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.mouse.set_visible(True)
                        pygame.event.set_grab(False)
                    if event.key == K_SPACE:
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
                    if event.key == K_m:
                        print(f"""
        Memory info:
            {memory_info()}
                        """)
                        sleep(1)
                if event.type == pygame.MOUSEWHEEL:
                    if self.object_grab:
                        if event.y > 0:
                            self.camera.camera_distance -= 0.5
                            self.mouse_wheel += 1
                        if event.y < 0:
                            self.camera.camera_distance += 0.5
                            self.mouse_wheel += 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 1 is left click.
                        self.builded_objects.append(self.build_object)
                        self.object_build_status = False
                    if event.button == 3:  # 3 == Right click
                        if self.right_click >= 7:  # available ObjectBuilder objects
                            self.right_click = 0
                        else:
                            self.object_build_status = False
                            self.right_click += 1

            if TSS:
                self.test_site.inside()
            self.camera_init()
            self.display()
            self.engine_fps()
            pygame.display.flip()
            self.clock.tick(SCREEN_MAX_FPS)
        pygame.quit()
