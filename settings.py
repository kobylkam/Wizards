import pygame

pygame.font.init()

# Game options
TITLE = "Hallows"
WIDTH = 1280
HEIGHT = 720
FPS = 200

# Player global properties

PLAYER_ACC = 0.2
PLAYER_FRICTION = -0.15
PLAYER_GRAVITY = 0.2
PLAYER_HEALTH = 100

# Game properties

BULLET_SPEED = 10
BULLET_LIFETIME = 1000.0
BULLET_DAMAGE = 10
GRENADE_SPEED = 7
GRENADE_DAMAGE = 30
TURN_TIME = 15

# Colors (R, G, B)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHTGREEN = (0, 255, 130)
YELLOW = (255, 255, 80)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (66, 134, 244)


# Display

FONT_TIME = pygame.font.Font("fonts/lucida_console.ttf", 25)
FONT_PLAYERS = pygame.font.Font("fonts/lucida_console.ttf", 18)
FONT_PLAYERS_2 = pygame.font.Font("fonts/lucida_console.ttf", 35)
FONT_MENU = pygame.font.Font("fonts/franklin_gothic_heavy_regular.ttf", 40)
FONT_OPTIONS = pygame.font.Font("fonts/franklin_gothic_heavy_regular.ttf", 30)
FONT_DETAIL = pygame.font.Font("fonts/lucida_console.ttf", 15)