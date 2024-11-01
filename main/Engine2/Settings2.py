# OpenUniverse Configuration Settings
from OpenGL.GL import GL_LINES
# Version of the engine
VERSION = "1.8.8-beta"

# Wall of names
WON = ["MatinAfzal"]

# World generation parameters
CHUNKS = 40          # Number of chunks to load in the game world
TREES = 40           # Number of trees to generate in the game world

# ASCII art banner for the engine
BANNER = f"""
     ___ ___ ___
   /___/___/___/|
  /___/___/___/||
 /___/___/__ /|/|
|   |   |   | /||
|___|___|___|/|/|
|   |   |   | /||
|___|___|___|/|/
|   |   |   | /
|___|___|___|/
    OpenUniverse V{VERSION}
"""

# Debug settings to control logging and error reporting
ENGINE_STATUS_PRINT = False
ENGINE_STATUS_PRINT_VERY_VERBOSE = False    # Detailed logging for debugging
ENGINE_REPORT_SAVE = False                  # Save error reports to a file
ENGINE_REPORT_TIME_BASED = False            # Enable time-based reporting

# Report settings for easier access
ESP = ENGINE_STATUS_PRINT                    # Alias for status printing
ERT_B = ENGINE_REPORT_TIME_BASED             # Alias for time-based reporting
ESP_VV = ENGINE_STATUS_PRINT_VERY_VERBOSE    # Alias for verbose logging

# Test site configuration
TEST_SITE_STATUS = False                      # Enable or disable test site features
TEST_SITE_COMMENT = ""                       # Comments regarding the test site
TSS = TEST_SITE_STATUS                       # Alias for test site status

# Culling settings for performance optimization
DISTANCE_CULLING = True                      # Enable distance-based culling
DISTANCE_CULLING_DISTANCE = 15               # Max distance for culling objects
CHUNK_GENERATION_WIDE = 50                   # Width for chunk generation
PRO_GAP = 100                                # Gap between generated chunks

# Sky settings for environmental effects
SKY_DYNAMIC = False                           # Enable dynamic sky effects
SUN_STATUS = True                             # Enable sun in the sky
SKY_SPEED = 0.000062                          # Speed of sky movement
SUN_SPEED_Y = 0.018                           # Vertical speed of the sun
SUN_SPEED_X = 0.018                           # Horizontal speed of the sun

# Light source initial position
INITIAL_LIGHT_POS_X = -80
INITIAL_LIGHT_POS_Z = (CHUNKS * 8) / 2
INITIAL_LIGHT_POS_Y = -60

# World settings for visual aspects
WORLD_DEPTH = 3                               # Depth of the game world
WORLD_BORDER = 500                            # Border size for the world in blocks
WORLD_COLOR_R = 0.5                           # Red component of world color
WORLD_COLOR_G = 0.5                           # Green component of world color
WORLD_COLOR_B = 0.5                           # Blue component of world color
WORLD_COLOR_A = 0.5                           # Alpha component of world color

# Settings for world axes visualization
WORLD_AXES_VERTICES = [[-100, 0, 0], [100, 0, 0], [0, -100, 0], [0, 100, 0], [0, 0, -100], [0, 0, 100]]
WORLD_AXES_COLORS = [[1, 0, 0], [1, 0, 0], [0, 1, 0], [0, 1, 0], [0, 0, 1], [0, 0, 1]]
WORLD_AXES_DRAWTYPE = GL_LINES                # OpenGL draw type for axes

# Chunk color settings
CHUNK_COLOR_R = 1                             # Red component of chunk color
CHUNK_COLOR_G = 1                             # Green component of chunk color
CHUNK_COLOR_B = 1                             # Blue component of chunk color

# Camera settings for controlling the view
CAMERA_POSITION = (0, 0, 0)                   # Initial camera position
CAMERA_MOUSE_SENSITIVITY_X = 0.1              # Mouse sensitivity for horizontal movement
CAMERA_MOUSE_SENSITIVITY_Y = 0.1              # Mouse sensitivity for vertical movement
CAMERA_MOVE_SENSITIVITY = 0.001               # Sensitivity for camera movement
CAMERA_VIEW_ANGLE = 60                        # Camera field of view angle
CAMERA_NEAR_PLANE = 0.01                      # Near clipping plane distance
CAMERA_FAR_PLANE = 10000                      # Far clipping plane distance
CAMERA_ROTATE_YAW_LOCAL = True                # Enable local yaw rotation
CAMERA_ROTATE_PITCH_LOCAL = True              # Enable local pitch rotation
CAMERA_ROTATE_PITCHUP_MAX = 170.0             # Max pitch-up angle
CAMERA_ROTATE_PITCHDOWN_MAX = -170.0          # Max pitch-down angle

# Screen settings for display properties
SCREEN_POS_X = 100                            # X position of the screen window
SCREEN_POS_Y = 30                             # Y position of the screen window
SCREEN_WIDTH = 1000                           # Width of the screen
SCREEN_HEIGHT = 800                           # Height of the screen
SCREEN_MULTISAMPLEBUFFERS = 1                 # Number of multisample buffers for anti-aliasing
SCREEN_MULTISAMPLESAMPLES = 4                 # Samples per pixel for anti-aliasing
SCREEN_DEPTH_SIZE = 24                        # Depth buffer size
SCREEN_CAPTION_LOADING = "Loading..."         # Caption for loading screen
SCREEN_CAPTION = f"OpenUniverse V [V ANY] from [{VERSION}]"  # Main screen caption
SCREEN_MAX_FPS = 30                           # Maximum frames per second for the game loop
