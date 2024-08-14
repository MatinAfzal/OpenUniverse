from OpenGL.GL import GL_LINES

# OpenUniverse
VERSION = "1.2.3-beta"
CHUNKS = 30
TREES = 30

# Debug settings
ENGINE_STATUS_PRINT = True
ENGINE_STATUS_PRINT_VERY_VERBOSE = False  # Very Verbose, Print Errors and etc.
ENGINE_REPORT_SAVE = False
ENGINE_REPORT_TIME_BASED = False

# Report settings
ESP = ENGINE_STATUS_PRINT
ERT_B = ENGINE_REPORT_TIME_BASED
ESP_VV = ENGINE_STATUS_PRINT_VERY_VERBOSE

# TestSite settings
TEST_SITE_STATUS = False
TEST_SITE_COMMENT = ""

TSS = TEST_SITE_STATUS

# Culling Settings
DISTANCE_CULLING = True
DISTANCE_CULLING_DISTANCE = 15
CHUNK_GENERATION_WIDE = 50
PRO_GAP = 100

CGW = CHUNK_GENERATION_WIDE
DCD = DISTANCE_CULLING_DISTANCE

# Sky settings
SKY_DYNAMIC = False
SUN_STATUS = True
SKY_SPEED = 0.000062
# SUN_SPEED_Y = 0.008
# SUN_SPEED_X = 0.038
SUN_SPEED_Y = 0.408
SUN_SPEED_X = 0.438

INITIAL_LIGHT_POS_X = -80
INITIAL_LIGHT_POS_Z = 110
INITIAL_LIGHT_POS_Y = -60

# World settings
WORLD_DEPTH = 3
WORLD_BORDER = 500  # blocks
WORLD_COLOR_R = 0.5
WORLD_COLOR_G = 0.5
WORLD_COLOR_B = 0.5
WORLD_COLOR_A = 0.5

# World axes settings
WORLD_AXES_VERTICES = [[-100, 0, 0], [100, 0, 0], [0, -100, 0], [0, 100, 0], [0, 0, -100], [0, 0, 100]]
WORLD_AXES_COLORS = [[1, 0, 0], [1, 0, 0], [0, 1, 0], [0, 1, 0], [0, 0, 1], [0, 0, 1]]
WORLD_AXES_DRAWTYPE = GL_LINES

# Chunk settings
CHUNK_COLOR_R = 1
CHUNK_COLOR_G = 1
CHUNK_COLOR_B = 1

# Camera settings
CAMERA_POSITION = (100, 0, 100)  # > 50 not allowed!
CAMERA_MOUSE_SENSITIVITY_X = 0.1
CAMERA_MOUSE_SENSITIVITY_Y = 0.1
# CAMERA_MOVE_SENSITIVITY = 0.31
CAMERA_MOVE_SENSITIVITY = 0.11
CAMERA_VIEW_ANGLE = 60
CAMERA_NEAR_PLANE = 0.01
CAMERA_FAR_PLANE = 10000
CAMERA_ROTATE_YAW_LOCAL = True
CAMERA_ROTATE_PITCH_LOCAL = True
CAMERA_ROTATE_PITCHUP_MAX = 170.0
# CAMERA_ROTATE_PITCHDOWN_MAX = 30
CAMERA_ROTATE_PITCHDOWN_MAX = -170.0

# Screen settings
# SCREEN_POS_X = 850
# SCREEN_POS_Y = 200
SCREEN_POS_X = 100
SCREEN_POS_Y = 30
# SCREEN_WIDTH = 1920
# SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1000
SCREEN_MULTISAMPLEBUFFERS = 1
SCREEN_MULTISAMPLESAMPLES = 4
SCREEN_DEPTH_SIZE = 24
SCREEN_CAPTION_LOADING = "Loading..."
SCREEN_CAPTION = "OpenUniverse V [VANY] from [1.2.3]"
SCREEN_MAX_FPS = 60
