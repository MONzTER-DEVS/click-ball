import pygame, os
WW,WH = 1200,720

# Font
tiny_font = pygame.font.Font('Roboto-Thin.ttf', 24)
small_font = pygame.font.Font('Roboto-Thin.ttf', 32)
medium_font = pygame.font.Font('Roboto-Thin.ttf', 48)
big_font = pygame.font.Font('Roboto-Thin.ttf', 64)
GRAVITY = 350
FPS = 60

def game_font_generator(size):
    return pygame.font.Font('Roboto-Thin.ttf', size)


#################   General Settings    #################
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
L_BLUE = (0, 255, 255)
PINK = (255, 0, 255)
PURPLE = (148, 0, 211)
GRAY = (100, 100, 100)

## Player Skins
img_path = os.path.join('assets', 'imgs', 'skins_png')
skins = []
for img_name in os.listdir(img_path):
    if os.path.isfile(os.path.join(img_path, img_name)):
        skins.append(pygame.image.load(os.path.join(img_path, img_name)))

## Levels
lvl_path_50 = os.path.join('assets', 'levels', '1-50')
levels = []
for lvl_name in os.listdir(lvl_path_50):
    if os.path.isfile(os.path.join(lvl_path_50, lvl_name)):
        levels.append(os.path.join(lvl_path_50, lvl_name))