import pygame
import time
import json
import ast

pygame.init()

from .db_functions import *
from .extra_screens import *
from .settings import *
from .classes import *

# screen = pygame.display.set_mode((WW, WH), screen_flags)
screen_flags = pygame.SCALED | pygame.RESIZABLE
screen, val = DB.make_screen()

yellow_buttons = {
    "play": pygame.image.load("assets/buttons/Yellow button/Play.png").convert_alpha(),
    "settings": pygame.image.load("assets/buttons/Yellow button/settings.png").convert_alpha(),
    "leaderboard": pygame.image.load("assets/buttons/Yellow button/Leaderboard.png").convert_alpha(),
    "exit": pygame.image.load("assets/buttons/Yellow button/Exit.png").convert_alpha(),
    "survival": pygame.image.load("assets/buttons/Yellow button/Survival.png").convert_alpha(),
    "campaign": pygame.image.load("assets/buttons/Yellow button/Campaign.png").convert_alpha(),
    "theme": pygame.image.load("assets/buttons/Yellow button/Theme.png").convert_alpha(),
    "ball": pygame.image.load("assets/buttons/Yellow button/Ball.png").convert_alpha(),
    "back": pygame.image.load("assets/buttons/Yellow button/Back.png").convert_alpha(),
    "continue": pygame.image.load("assets/buttons/Yellow button/Continue.png").convert_alpha(),
    "next level": pygame.image.load("assets/buttons/Yellow button/Next level.png").convert_alpha(),
    "music": pygame.image.load("assets/buttons/Yellow button/music.png").convert_alpha()
}

blue_button = {
    "play": pygame.image.load("assets/buttons/Blue button/Play.png").convert_alpha(),
    "settings": pygame.image.load("assets/buttons/Blue button/settings.png").convert_alpha(),
    "leaderboard": pygame.image.load("assets/buttons/Blue button/Leaderboard.png").convert_alpha(),
    "exit": pygame.image.load("assets/buttons/Blue button/Exit.png").convert_alpha(),
    "survival": pygame.image.load("assets/buttons/Blue button/Survival.png").convert_alpha(),
    "campaign": pygame.image.load("assets/buttons/Blue button/Campaign.png").convert_alpha(),
    "theme": pygame.image.load("assets/buttons/Blue button/Theme.png").convert_alpha(),
    "ball": pygame.image.load("assets/buttons/Blue button/Ball.png").convert_alpha(),
    "back": pygame.image.load("assets/buttons/Blue button/Back.png").convert_alpha(),
    "continue": pygame.image.load("assets/buttons/Blue button/Continue.png").convert_alpha(),
    "next level": pygame.image.load("assets/buttons/Blue button/Next level.png").convert_alpha(),
    "music": pygame.image.load("assets/buttons/Blue button/music.png").convert_alpha()
}

green_button = {
    "play": pygame.image.load("assets/buttons/Green button/Play.png").convert_alpha(),
    "settings": pygame.image.load("assets/buttons/Green button/settings.png").convert_alpha(),
    "leaderboard": pygame.image.load("assets/buttons/Green button/Leaderboard.png").convert_alpha(),
    "exit": pygame.image.load("assets/buttons/Green button/Exit.png").convert_alpha(),
    "survival": pygame.image.load("assets/buttons/Green button/Survival.png").convert_alpha(),
    "campaign": pygame.image.load("assets/buttons/Green button/Campaign.png").convert_alpha(),
    "theme": pygame.image.load("assets/buttons/Green button/Theme.png").convert_alpha(),
    "ball": pygame.image.load("assets/buttons/Green button/Ball.png").convert_alpha(),
    "back": pygame.image.load("assets/buttons/Green button/Back.png").convert_alpha(),
    "continue": pygame.image.load("assets/buttons/Green button/Continue.png").convert_alpha(),
    "next level": pygame.image.load("assets/buttons/Green button/Next level.png").convert_alpha(),
    "music": pygame.image.load("assets/buttons/Green button/music.png").convert_alpha(),
}

pink_button = {
    "play": pygame.image.load("assets/buttons/Pink button/Play.png").convert_alpha(),
    "settings": pygame.image.load("assets/buttons/Pink button/settings.png").convert_alpha(),
    "leaderboard": pygame.image.load("assets/buttons/Pink button/Leaderboard.png").convert_alpha(),
    "exit": pygame.image.load("assets/buttons/Pink button/Exit.png").convert_alpha(),
    "survival": pygame.image.load("assets/buttons/Pink button/Survival.png").convert_alpha(),
    "campaign": pygame.image.load("assets/buttons/Pink button/Campaign.png").convert_alpha(),
    "theme": pygame.image.load("assets/buttons/Pink button/Theme.png").convert_alpha(),
    "ball": pygame.image.load("assets/buttons/Pink button/Ball.png").convert_alpha(),
    "back": pygame.image.load("assets/buttons/Pink button/Back.png").convert_alpha(),
    "continue": pygame.image.load("assets/buttons/Pink button/Continue.png").convert_alpha(),
    "next level": pygame.image.load("assets/buttons/Pink button/Next level.png").convert_alpha(),
    "music": pygame.image.load("assets/buttons/Pink button/music.png").convert_alpha()
}

purple_button = {
    "play": pygame.image.load("assets/buttons/Purple button/Play.png").convert_alpha(),
    "settings": pygame.image.load("assets/buttons/Purple button/settings.png").convert_alpha(),
    "leaderboard": pygame.image.load("assets/buttons/Purple button/Leaderboard.png").convert_alpha(),
    "exit": pygame.image.load("assets/buttons/Purple button/Exit.png").convert_alpha(),
    "survival": pygame.image.load("assets/buttons/Purple button/Survival.png").convert_alpha(),
    "campaign": pygame.image.load("assets/buttons/Purple button/Campaign.png").convert_alpha(),
    "theme": pygame.image.load("assets/buttons/Purple button/Theme.png").convert_alpha(),
    "ball": pygame.image.load("assets/buttons/Purple button/Ball.png").convert_alpha(),
    "back": pygame.image.load("assets/buttons/Purple button/Back.png").convert_alpha(),
    "continue": pygame.image.load("assets/buttons/Purple button/Continue.png").convert_alpha(),
    "next level": pygame.image.load("assets/buttons/Purple button/Next level.png").convert_alpha(),
    "music": pygame.image.load("assets/buttons/Purple button/music.png").convert_alpha(),
}

red_button = {
    "play": pygame.image.load("assets/buttons/Red button/Play.png").convert_alpha(),
    "settings": pygame.image.load("assets/buttons/Red button/settings.png").convert_alpha(),
    "leaderboard": pygame.image.load("assets/buttons/Red button/Leaderboard.png").convert_alpha(),
    "exit": pygame.image.load("assets/buttons/Red button/Exit.png").convert_alpha(),
    "survival": pygame.image.load("assets/buttons/Red button/Survival.png").convert_alpha(),
    "campaign": pygame.image.load("assets/buttons/Red button/Campaign.png").convert_alpha(),
    "theme": pygame.image.load("assets/buttons/Red button/Theme.png").convert_alpha(),
    "ball": pygame.image.load("assets/buttons/Red button/Ball.png").convert_alpha(),
    "back": pygame.image.load("assets/buttons/Red button/Back.png").convert_alpha(),
    "continue": pygame.image.load("assets/buttons/Red button/Continue.png").convert_alpha(),
    "next level": pygame.image.load("assets/buttons/Red button/Next level.png").convert_alpha(),
    "music": pygame.image.load("assets/buttons/Red button/music.png").convert_alpha(),
}

#                      name,               bg,       platform_c, mouse_line, font_c,  hover, bouncing_ball_c, cursor
light_theme = Themes('Bright White', WHITE, L_BLUE, GREEN, PINK, WHITE, GREEN, yellow_buttons, L_BLUE)
violet_theme = Themes("Limited Voilet", PURPLE, WHITE, WHITE, WHITE, WHITE, WHITE, blue_button, WHITE)
dark_light_theme = Themes("Darkest Light", BLACK, WHITE, WHITE, L_BLUE, WHITE, EMRALD, green_button, EMRALD)
dracula_theme = Themes("Dracula", BLACK, PINK, PINK, PINK, WHITE, EMRALD, pink_button, WHITE)
green_theme = Themes("Grass", (81, 204, 64), (121, 234, 125), (201, 242, 199), (36, 49, 25), WHITE, (121, 234, 125),
                     purple_button, WHITE)
hot_chilli_theme = Themes("Hot Chilli", (157, 2, 8), (232, 93, 4), WHITE, (255, 186, 8), WHITE, (220, 47, 2),
                          red_button, PINK)
light_theme.set_to_active_theme()

# Make DB if it doesnt Exist

can_start_game = False

errors = []

number_buttons = [
    pygame.image.load(os.path.join('assets', 'buttons', 'level number buttons', 'lock.png')).convert_alpha()]

loading_percent = 0

pygame.init()


def load_data_while_loading_screen():
    global can_start_game
    global number_buttons
    global loading_percent
    st_time = time.time()

    loading_percent = 1

    DB.check_tables()
    loading_percent = 2
    if DB.check_name() == "no name":
        errors.append("no name")
    else:
        User_data.name = DB.fetch_name()
    loading_percent = 4
    loading_percent = 5
    loading_percent = 6

    number_buttons_path = os.path.join('assets', 'buttons', 'level number buttons')
    loading_percent = 7
    for counter in range(1, 101):
        path = os.path.join(number_buttons_path, f'{int(4 - len(str(counter))) * "0"}{counter}.png')
        number_buttons.append(pygame.image.load(path).convert_alpha())
        loading_percent += 0.1

    loading_percent = 17.5

    data_u_p = DB.load_user_progress()[0]
    loading_percent += 0.5
    User_data.current_level = int(data_u_p[0])
    loading_percent += 0.5
    User_data.coins = ast.literal_eval(data_u_p[2])
    loading_percent += 0.5

    try:
        for x in range(1, len(os.listdir(os.path.join('assets', 'levels'))) + 1):
            f = open(os.path.join('assets', 'levels', f'level{x}.json'))
            Levels(name='placeholder', data=json.load(f))
            f.close()
            loading_percent += 0.2
    except:
        pass

    sleep = (3 - float(time.time() - st_time)) / (int(100 - loading_percent) * 5)

    if sleep < 0:
        loading_percent = 99
    else:
        while loading_percent < 100:
            loading_percent += 0.2
            time.sleep(sleep)

    # change this at the absolute end else conflicts would take place
    data = DB.Cache.load()
    Music.play = ast.literal_eval(data[1][0][0])
    User_data.line = data[2][0][0]
    Themes.set_active_by_name(data[0][0][0])
    can_start_game = True
    pygame.init()
    User_data.save = ast.literal_eval(data_u_p[1])
    loading_percent += 0.5
    if Music.play:
        Music.play_music()


t_load_data_while_loading_screen = threading.Thread(target=load_data_while_loading_screen)
t_load_data_while_loading_screen.start()
# Starting to load data

# starting screen
pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'imgs', 'ClickBall.png')).convert_alpha())
pygame.display.set_caption('Click Ball!')
# pygame.mouse.cursor()
clock = pygame.time.Clock()
loading_screen_running = True

to_do = ['welcome']
template = pygame.image.load('assets/imgs/loading bar/template.png')
template_rect = template.get_rect()
template_rect.center = (WW // 2, WH - 200)
fill_img = pygame.image.load('assets/imgs/loading bar/Fill.png')
fill_rect = fill_img.get_rect()
fill_rect.center = (WW // 2, WH - 200)

while loading_screen_running:
    screen.fill(Themes.active_theme.background)
    text = big_font.render("Loading...", True, Themes.active_theme.font_c)
    text_rect = text.get_rect()
    text_rect.center = (WW / 2, WH / 2)
    screen.blit(text, text_rect)
    screen.blit(template, template_rect)

    screen.blit(fill_img, fill_rect, (0, 0, fill_rect.width * loading_percent / 100, fill_rect.height))

    if can_start_game:
        loading_screen_running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loading_screen_running = False
            to_do = ['quit']
    pygame.display.update()

# @todo handle DB errors
