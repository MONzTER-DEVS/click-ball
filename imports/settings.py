import os
import pygame
import sqlite3
# import platform

# WW, WH = pygame.display.Info().current_w, pygame.display.Info().current_h
WW, WH = 1200, 720

# Font
tiny_font = pygame.font.Font('assets/Roboto-Thin.ttf', 24)
small_font = pygame.font.Font('assets/Roboto-Thin.ttf', 32)
medium_font = pygame.font.Font('assets/Roboto-Thin.ttf', 48)
big_font = pygame.font.Font('assets/Roboto-Thin.ttf', 64)
GRAVITY = 350
FPS = 60


def game_font_generator(size):
    return pygame.font.Font('assets/Roboto-Thin.ttf', size)


#################   General Settings    #################
# Colors
BLACK = (35, 51, 41)
WHITE = (255, 255, 255)
RED = (255, 100, 100)
GREEN = (201, 242, 199)
BLUE = (105, 255, 241)
L_BLUE = (0, 255, 255)
PINK = (255, 105, 125)
PURPLE = (195, 65, 177)
GRAY = (100, 100, 100)
EMRALD = (99, 212, 113)

## Player Skins
img_path = os.path.join('assets', 'imgs', 'skins_png')
skins = []
for img_name in os.listdir(img_path):
    if os.path.isfile(os.path.join(img_path, img_name)):
        big_img = pygame.image.load(os.path.join(img_path, img_name))
        small_img = pygame.transform.smoothscale(big_img, (32, 32))
        skins.append(small_img)

## Levels
lvl_path_50 = os.path.join('assets', 'levels', '1-50')
levels = []

"""
if platform.system().lower() == "windows":
    try:
        app_data_path = os.path.join(os.getenv('APPDATA'), '..', 'LocalLow')
        db_folder_path = os.path.join(app_data_path, 'click ball')
        if not os.path.exists(os.path.join(db_folder_path)):
            os.mkdir(f"{app_data_path}/click ball")
        db_path = os.path.join(db_folder_path, 'data.db')

        # TESTING
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        conn.commit()
        conn.close()


    except Exception as e:
        try:
            folder_path = os.path.join('C:/', 'click ball')
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            db_path = os.path.join('C:/', 'click ball', 'data.db')
        except:
            db_path = os.path.join('assets', 'data.db')

else:
    db_path = os.path.join('assets', 'data.db')
"""
db_path = 'data.db'
