import math

RES = WIDTH, HEIGHT = 1600, 900
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60

GAME_BG_COLOR = '#212121'
#GAME_BG_COLOR = 'black'
CEILING_COLOR = (0, 108, 112)
FLOOR_COLOR = (70, 70, 70)
MAP_BLOCK_COLOR = 'white'
MAP_RECT_SIZE = 10

PLAYER_START_POSITION = 29.5, 57.5
PLAYER_ANGLE = 0 #-3.14 / 2
PLAYER_SPEED = 0.004
PLAYER_ROTATION_SPEED = 0.002
PLAYER_SIZE = 3 
PLAYER_SIZE_SCALE = 70
PLAYER_COLOR = 'green'
PLAYER_ANGLE_COLOR = 'yellow'

MOUSE_SENSITIVITY = 0.0002
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

#RAY CASTING
FIELD_OF_VIEW = math.pi / 3 #60°
HALF_FIELD_OF_VIEW = FIELD_OF_VIEW / 2
NUMBER_OF_RAYS = WIDTH // 2
HALF_NUMBER_OF_RAYS = NUMBER_OF_RAYS // 2
DELTA_ANGLE = FIELD_OF_VIEW / NUMBER_OF_RAYS
MAX_DEPTH = 30 

SCREEN_DISTANCE_TO_PLAYER = HALF_WIDTH / math.tan(HALF_FIELD_OF_VIEW)
SCALE = WIDTH // NUMBER_OF_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

TMX_WALLS_ITEMS_INDEX = 2
TMX_NPC_ITEMS_INDEX = 1