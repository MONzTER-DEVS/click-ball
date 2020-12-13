import pygame
import time
import json
import ast

pygame.init()

from .settings import *
from .classes import *

#                      name,               bg,       platform_c, mouse_line, font_c,  hover, bouncing_ball_c
light_theme = Themes('Bright White', WHITE, L_BLUE, GREEN, PINK, WHITE, GREEN)
violet_theme = Themes("Limited Voilet", PURPLE, WHITE, WHITE, WHITE, WHITE, WHITE)
dark_light_theme = Themes("Darkest Light", BLACK, WHITE, WHITE, L_BLUE, WHITE, EMRALD)
dracula_theme = Themes("Dracula", BLACK, PINK, PINK, PINK, WHITE, EMRALD)
green_theme = Themes("Grass", (81,204,64), (121,234,125), (201,242,199), (36,49,25), WHITE, (121,234,125))
hot_chilli_theme = Themes("Hot Chilli", (157,2,8), (232,93,4), WHITE, (255,186,8), WHITE, (220,47,2))
light_theme.set_to_active_theme()

from .extra_screens import *
from .db_functions import *

# Make DB if it doesnt Exist

can_start_game = False

errors = []

number_buttons = [pygame.image.load(os.path.join('assets', 'buttons', 'level number buttons', 'lock.png'))]


def load_data_while_loading_screen():
    global can_start_game
    global number_buttons
    if not os.path.exists(os.path.join('assets', 'data.db')):
        DB.make_db()

    if DB.check_name() == "no name":
        errors.append("no name")
    else:
        User_data.name = DB.fetch_name()
    st_time = time.time()
    data = DB.Cache.load()
    Themes.set_active_by_name(data[0])

    number_buttons_path = os.path.join('assets', 'buttons', 'level number buttons')

    for counter in range(1, 101):
        path = os.path.join(number_buttons_path, f'{int(4 - len(str(counter))) * "0"}{counter}.png')
        number_buttons.append(pygame.image.load(path))

    data = DB.load_user_progress()[0]
    User_data.current_level = int(data[0])
    User_data.save = ast.literal_eval(data[1])
    User_data.coins = ast.literal_eval(data[2])

    for x in range(1, len(os.listdir(os.path.join('assets', 'levels'))) + 1):
        f = open(os.path.join('assets', 'levels', f'level{x}.json'))
        Levels(name='placeholder', data=json.load(f))
        f.close()
    try:
        time.sleep(3 - float(time.time() - st_time))
    except:
        pass

    # change this at the absolute end else conflicts would take place
    can_start_game = True


t_load_data_while_loading_screen = threading.Thread(target=load_data_while_loading_screen)
t_load_data_while_loading_screen.start()
# Starting to load data

# starting screen
screen_flags = pygame.SCALED | pygame.RESIZABLE
screen = pygame.display.set_mode((WW, WH), screen_flags)
pygame.display.set_caption('Click Ball!')
clock = pygame.time.Clock()
loading_screen_running = True

to_do = ['welcome']
while loading_screen_running:
    screen.fill(Themes.active_theme.background)
    text = big_font.render("Loading Screen", True, Themes.active_theme.font_c)
    text_rect = text.get_rect()
    text_rect.center = (WW / 2, WH / 2)
    screen.blit(text, text_rect)

    if can_start_game:
        loading_screen_running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loading_screen_running = False
            to_do = ['quit']
    pygame.display.update()

# @todo handle DB errors
