import pygame
import time
import json
import ast

pygame.init()

from .settings import *
from .classes import *
yellow_buttons = {
    "play": pygame.image.load("assets/buttons/Yellow button/Play.png"),
    "settings": pygame.image.load("assets/buttons/Yellow button/settings.png"),
    "leaderboard": pygame.image.load("assets/buttons/Yellow button/Leaderboard.png"),
    "exit": pygame.image.load("assets/buttons/Yellow button/Exit.png"),
    "survival": pygame.image.load("assets/buttons/Yellow button/Survival.png"),
    "campaign": pygame.image.load("assets/buttons/Yellow button/Campaign.png"),
    "theme": pygame.image.load("assets/buttons/Yellow button/Theme.png"),
    "ball": pygame.image.load("assets/buttons/Yellow button/Ball.png"),
    "back": pygame.image.load("assets/buttons/Yellow button/Back.png"),
    "continue": pygame.image.load("assets/buttons/Yellow button/Continue.png"),
    "next level": pygame.image.load("assets/buttons/Yellow button/Next level.png"),
}

blue_button = {
    "play": pygame.image.load("assets/buttons/Yellow button/Play.png"),
    "settings": pygame.image.load("assets/buttons/Blue button/settings.png"),
    "leaderboard": pygame.image.load("assets/buttons/Blue button/Leaderboard.png"),
    "exit": pygame.image.load("assets/buttons/Blue button/Exit.png"),
    "survival": pygame.image.load("assets/buttons/Blue button/Survival.png"),
    "campaign": pygame.image.load("assets/buttons/Blue button/Campaign.png"),
    "theme": pygame.image.load("assets/buttons/Blue button/Theme.png"),
    "ball": pygame.image.load("assets/buttons/Blue button/Ball.png"),
    "back": pygame.image.load("assets/buttons/Blue button/Back.png"),
    "continue": pygame.image.load("assets/buttons/Blue button/Continue.png"),
    "next level": pygame.image.load("assets/buttons/Blue button/Next level.png"),
}

green_button = {
    "play": pygame.image.load("assets/buttons/Green button/Play.png"),
    "settings": pygame.image.load("assets/buttons/Green button/settings.png"),
    "leaderboard": pygame.image.load("assets/buttons/Green button/Leaderboard.png"),
    "exit": pygame.image.load("assets/buttons/Green button/Exit.png"),
    "survival": pygame.image.load("assets/buttons/Green button/Survival.png"),
    "campaign": pygame.image.load("assets/buttons/Green button/Campaign.png"),
    "theme": pygame.image.load("assets/buttons/Green button/Theme.png"),
    "ball": pygame.image.load("assets/buttons/Green button/Ball.png"),
    "back": pygame.image.load("assets/buttons/Green button/Back.png"),
    "continue": pygame.image.load("assets/buttons/Green button/Continue.png"),
    "next level": pygame.image.load("assets/buttons/Green button/Next level.png"),
}

pink_button = {
    "play": pygame.image.load("assets/buttons/Pink button/Play.png"),
    "settings": pygame.image.load("assets/buttons/Pink button/settings.png"),
    "leaderboard": pygame.image.load("assets/buttons/Pink button/Leaderboard.png"),
    "exit": pygame.image.load("assets/buttons/Pink button/Exit.png"),
    "survival": pygame.image.load("assets/buttons/Pink button/Survival.png"),
    "campaign": pygame.image.load("assets/buttons/Pink button/Campaign.png"),
    "theme": pygame.image.load("assets/buttons/Pink button/Theme.png"),
    "ball": pygame.image.load("assets/buttons/Pink button/Ball.png"),
    "back": pygame.image.load("assets/buttons/Pink button/Back.png"),
    "continue": pygame.image.load("assets/buttons/Pink button/Continue.png"),
    "next level": pygame.image.load("assets/buttons/Pink button/Next level.png"),
}

purple_button = {
    "play": pygame.image.load("assets/buttons/Purple button/Play.png"),
    "settings": pygame.image.load("assets/buttons/Purple button/settings.png"),
    "leaderboard": pygame.image.load("assets/buttons/Purple button/Leaderboard.png"),
    "exit": pygame.image.load("assets/buttons/Purple button/Exit.png"),
    "survival": pygame.image.load("assets/buttons/Purple button/Survival.png"),
    "campaign": pygame.image.load("assets/buttons/Purple button/Campaign.png"),
    "theme": pygame.image.load("assets/buttons/Purple button/Theme.png"),
    "ball": pygame.image.load("assets/buttons/Purple button/Ball.png"),
    "back": pygame.image.load("assets/buttons/Purple button/Back.png"),
    "continue": pygame.image.load("assets/buttons/Purple button/Continue.png"),
    "next level": pygame.image.load("assets/buttons/Purple button/Next level.png"),
}

red_button = {
    "play": pygame.image.load("assets/buttons/Red button/Play.png"),
    "settings": pygame.image.load("assets/buttons/Red button/settings.png"),
    "leaderboard": pygame.image.load("assets/buttons/Red button/Leaderboard.png"),
    "exit": pygame.image.load("assets/buttons/Red button/Exit.png"),
    "survival": pygame.image.load("assets/buttons/Red button/Survival.png"),
    "campaign": pygame.image.load("assets/buttons/Red button/Campaign.png"),
    "theme": pygame.image.load("assets/buttons/Red button/Theme.png"),
    "ball": pygame.image.load("assets/buttons/Red button/Ball.png"),
    "back": pygame.image.load("assets/buttons/Red button/Back.png"),
    "continue": pygame.image.load("assets/buttons/Red button/Continue.png"),
    "next level": pygame.image.load("assets/buttons/Red button/Next level.png"),
}

#                      name,               bg,       platform_c, mouse_line, font_c,  hover, bouncing_ball_c
light_theme = Themes('Bright White', WHITE, L_BLUE, GREEN, PINK, WHITE, GREEN, yellow_buttons)
violet_theme = Themes("Limited Voilet", PURPLE, WHITE, WHITE, WHITE, WHITE, WHITE, blue_button)
dark_light_theme = Themes("Darkest Light", BLACK, WHITE, WHITE, L_BLUE, WHITE, EMRALD, green_button)
dracula_theme = Themes("Dracula", BLACK, PINK, PINK, PINK, WHITE, EMRALD, pink_button)
green_theme = Themes("Grass", (81,204,64), (121,234,125), (201,242,199), (36,49,25), WHITE, (121,234,125), purple_button)
hot_chilli_theme = Themes("Hot Chilli", (157,2,8), (232,93,4), WHITE, (255,186,8), WHITE, (220,47,2), red_button)
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
    if not os.path.exists(DB.db_path):
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

    try:
        for x in range(1, len(os.listdir(os.path.join('assets', 'levels'))) + 1):
            f = open(os.path.join('assets', 'levels', f'level{x}.json'))
            Levels(name='placeholder', data=json.load(f))
            f.close()
    except:
        pass
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
