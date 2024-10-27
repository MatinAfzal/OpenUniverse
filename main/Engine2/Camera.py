import pygame
import math
import time
from .Transformations import *
from .Uniform import *
from .Settings2 import *


class Camera:
    """
    World Camera for 3D rendering.

    Attributes:
        transformation (np.ndarray): The transformation matrix for the camera, representing its
                                      position and orientation in the world.
        last_mouse (pygame.math.Vector2): The last recorded position of the mouse, used for
                                           calculating mouse movement.
        mouse_sensitivity_x (float): Sensitivity for horizontal mouse movement.
        mouse_sensitivity_y (float): Sensitivity for vertical mouse movement.
        key_sensitivity (float): Speed at which the camera moves in response to key inputs.
        projection_mat (np.ndarray): The projection matrix used for rendering the scene.
        projection (Uniform): Uniform variable to hold the projection matrix for shader programs.
        screen_width (int): The width of the rendering screen.
        screen_height (int): The height of the rendering screen.
        yaw (float): The yaw angle of the camera, representing rotation around the Y-axis.
        pitch (float): The pitch angle of the camera, representing rotation around the X-axis.
        camera_distance (float): Distance of the camera from the target point.
        target (pygame.Vector3): The point in 3D space that the camera is looking at.

    Parameters:
        width (int): The width of the camera's viewport.
        height (int): The height of the camera's viewport.

    Methods:
        perspective_mat(view_angle, aspect_ratio, near_plane, far_plane) -> np.ndarray:
            Computes the perspective projection matrix based on the provided parameters.

        rotate(yaw, pitch) -> None:
            Rotates the camera based on the given yaw and pitch values.

        update(program_id) -> None:
            Updates the camera's transformation and projection matrices based on input.

    Notes:
        - The camera's position is initialized from the `CAMERA_POSITION` variable.
        - Input handling for movement is achieved through the keyboard and mouse.
        - Debugging information can be printed when the 'z' key is pressed.
    """
    def __init__(self, width, height) -> None:
        if ESP:
            print("Loading Camera...")
        self.transformation = identity_mat()
        self.transformation[0, 3] = CAMERA_POSITION[0]  # X
        self.transformation[1, 3] = CAMERA_POSITION[1]  # Z
        self.transformation[2, 3] = CAMERA_POSITION[2]  # Y
        self.last_mouse = pygame.math.Vector2(0, 0)
        self.mouse_sensitivity_x = CAMERA_MOUSE_SENSITIVITY_X
        self.mouse_sensitivity_y = CAMERA_MOUSE_SENSITIVITY_Y
        self.key_sensitivity = CAMERA_MOVE_SENSITIVITY
        self.projection_mat = self.perspective_mat(CAMERA_VIEW_ANGLE, width / height,
                                                   CAMERA_NEAR_PLANE, CAMERA_FAR_PLANE)
        self.projection = Uniform("mat4", self.projection_mat)
        self.screen_width = width
        self.screen_height = height
        self.yaw = 0
        self.pitch = 0
        self.camera_distance = -10.0
        self.target = pygame.Vector3(0, 0, 0)

    @staticmethod
    def perspective_mat(view_angle, aspect_ratio, near_plane, far_plane) -> np.ndarray:
        a = math.radians(view_angle)
        d = 1.0 / math.tan(a/2)
        r = aspect_ratio
        b = (far_plane + near_plane) / (near_plane - far_plane)
        c = far_plane * near_plane / (near_plane - far_plane)
        return np.array([[d/r, 0, 0, 0], [0, d, 0, 0], [0, 0, b, c], [0, 0, -1, 0]], np.float32)

    def rotate(self, yaw, pitch) -> None:
        """
        Camera rotation
        """
        self.yaw = yaw
        self.pitch = pitch
        forward = pygame.Vector3(self.transformation[0, 2], self.transformation[1, 2], self.transformation[2, 2])
        up = pygame.Vector3(0, 1, 0)
        angle = forward.angle_to(up)
        
        self.transformation = rotate(self.transformation, yaw, "Y", CAMERA_ROTATE_YAW_LOCAL)
        if (angle < CAMERA_ROTATE_PITCHUP_MAX and pitch > 0) or (angle > CAMERA_ROTATE_PITCHDOWN_MAX and pitch < 0):
            self.transformation = rotate(self.transformation, pitch, "X", CAMERA_ROTATE_PITCH_LOCAL)

        camera_position = pygame.Vector3(self.transformation[0, 3], self.transformation[1, 3],
                                         self.transformation[2, 3])

        camera_target = camera_position + (self.camera_distance * forward)

        self.target = camera_target

        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            print(f"""
            Camera info:
                - Position: {round(camera_position.x, 2)} {round(camera_position.y, 2)}, {round(camera_position.z, 2)}
                - Forward: {round(forward.x, 2)} {round(forward.y, 2)} {round(forward.z, 2)}
            """)
            time.sleep(1)

    def update(self, program_id) -> None:
        if pygame.mouse.get_visible():
            return

        mouse_pos = pygame.mouse.get_pos()
        mouse_change = self.last_mouse - pygame.math.Vector2(mouse_pos)
        pygame.mouse.set_pos(self.screen_width / 2, self.screen_height / 2)
        self.last_mouse = pygame.mouse.get_pos()
        self.rotate(mouse_change.x * self.mouse_sensitivity_x, mouse_change.y * self.mouse_sensitivity_y)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.transformation = translate(self.transformation, 0, 0, self.key_sensitivity)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.transformation = translate(self.transformation, 0, 0, -self.key_sensitivity)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.transformation = translate(self.transformation, self.key_sensitivity, 0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.transformation = translate(self.transformation, -self.key_sensitivity, 0, 0)

        self.projection.find_variable(program_id, "projection_mat")
        self.projection.load()
        lookat_mat = self.transformation
        lookat = Uniform("mat4", lookat_mat)
        lookat.find_variable(program_id, "view_mat")
        lookat.load()
