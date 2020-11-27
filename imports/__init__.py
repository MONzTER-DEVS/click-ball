import pygame
import time

pygame.init()

from .settings import *
from .classes import *

#                      name,               bg,       platform_c, mouse_line, font_c,  hover
light_theme = Themes('Bright White', WHITE, L_BLUE, GREEN, PINK, WHITE)
violet_theme = Themes("Limited Voilet", PURPLE, WHITE, WHITE, WHITE, WHITE)
dark_light_theme = Themes("Darkest Light", BLACK, WHITE, WHITE, L_BLUE, WHITE)
dracula_theme = Themes("Dracula", BLACK, PINK, PINK, PINK, WHITE)
light_theme.set_to_active_theme()

from .extra_screens import *
from .db_functions import *

# Make DB if it doesnt Exist

can_start_game = False


def load_data_while_loading_screen():
    global can_start_game
    if not os.path.exists(os.path.join('assets', 'data.db')):
        DB.make_db()
    data = DB.load_all_data()
    Themes.set_active_by_name(data[0])

    for x in range(1, len(os.listdir(os.path.join('assets', 'levels'))) + 1):
        f = open(os.path.join('assets', 'levels', f'level{x}.json'))
        Levels(name='placeholder', data=json.load(f))
        f.close()
    time.sleep(2)

    # change this at the absolute end else conflicts will happen
    can_start_game = True


t_load_data_while_loading_screen = threading.Thread(target=load_data_while_loading_screen)
t_load_data_while_loading_screen.start()
# Starting to load data

# starting screen
screen_flags = pygame.SCALED
screen = pygame.display.set_mode((WW, WH), screen_flags)
pygame.display.set_caption('Click Ball!')
clock = pygame.time.Clock()
loading_screen_running = True

to_do = ['welcome']
while loading_screen_running:
    screen.fill(Themes.active_theme.background)
    text = big_font.render("Loading Screen", True, Themes.active_theme.font_c)
    text_rect = text.get_rect()
    text_rect.center = (WW / 2, 50)
    screen.blit(text, text_rect)

    if can_start_game:
        loading_screen_running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loading_screen_running = False
            to_do = ['quit']
    pygame.display.update()
