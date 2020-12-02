import random
import threading

from imports.db_functions import *
from .extra_screen_functions import *

# Declaring some Variables
lboard_data = []
## Size is 204 x 81
## Ratio is 51/20
buttons = {
    "play": pygame.image.load("assets/buttons/Yellow button/Play.png"),
    "settings": pygame.image.load("assets/buttons/Yellow button/settings.png"),
    "leaderboard": pygame.image.load("assets/buttons/Yellow button/Leaderboard.png"),
    "exit": pygame.image.load("assets/buttons/Yellow button/Exit.png"),
    "survival": pygame.image.load("assets/buttons/Yellow button/Survival.png"),
    "campaign": pygame.image.load("assets/buttons/Yellow button/Campaign.png"),
    "theme": pygame.image.load("assets/buttons/Yellow button/Theme.png"),
    "ball": pygame.image.load("assets/buttons/Yellow button/Ball.png"),
    "glossy07": pygame.image.load("assets/buttons/Glossy07.png"),
    "glossy08": pygame.image.load("assets/buttons/Glossy08.png"),
    "glossy09": pygame.image.load("assets/buttons/Glossy09.png"),
    "glossy10": pygame.image.load("assets/buttons/Glossy10.png")
}


def welcome_screen(screen):
    clicked = False
    mx, my = pygame.mouse.get_pos()
    theme = Themes.active_theme
    space = pymunk.Space()

    BORDERS = 50
    NUM_OF_BALLS = 50
    balls = []
    for i in range(NUM_OF_BALLS):
        x, y = random.randint(BORDERS, WW - BORDERS), -BORDERS
        # x, y = WW//2, WH//2
        vx, vy = random.randint(0, 100), random.randint(0, 100)
        r = random.randint(10, 30)
        b = DynamicBallWithColor((x, y), vx, vy, r, space)
        balls.append(b)

    while True:
        screen.fill(theme.background)

        # Ball
        for ball in balls:
            ball.draw(screen, Themes.active_theme.bouncing_ball_c)
            if ball.body.position.x >= WW + BORDERS:
                x, y = -BORDERS, ball.body.position[1]
                ball.body.position = (x, y)
            elif ball.body.position.x <= -BORDERS:
                x, y = WW + BORDERS, ball.body.position[1]
                ball.body.position = (x, y)

            if ball.body.position.y >= WH + BORDERS:
                x, y = ball.body.position[0], -BORDERS
                ball.body.position = (x, y)
            elif ball.body.position.y <= - BORDERS:
                x, y = ball.body.position[0], WH + BORDERS
                ball.body.position = (x, y)

        # display
        heading_text = big_font.render('Clicker Ball!', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW / 2, 50)
        screen.blit(heading_text, heading_rect.topleft)

        # Play button
        play_button = buttons["play"]
        rect = play_button.get_rect(center=(WW // 2, 215))
        if mouse_rect.colliderect(rect):
            play_button = pygame.transform.smoothscale(buttons["play"], (177, 69))
            rect = play_button.get_rect(center=(WW // 2, 215))
        else:
            play_button = pygame.transform.smoothscale(buttons["play"], (150, 65))
            rect = play_button.get_rect(center=(WW // 2, 215))
        if clicked and mouse_rect.colliderect(rect):
            return ['game']
        screen.blit(play_button, rect.topleft)

        # Settings Button
        settings_button = buttons["settings"]
        rect = settings_button.get_rect(center=(WW // 2, WH - 150))
        if mouse_rect.colliderect(rect):
            settings_button = pygame.transform.smoothscale(buttons["settings"], (160, 58))
            rect = settings_button.get_rect(center=(WW // 2, WH - 150))
        else:
            settings_button = pygame.transform.smoothscale(buttons["settings"], (145, 54))
            rect = settings_button.get_rect(center=(WW // 2, WH - 150))
        if clicked and mouse_rect.colliderect(rect):
            return ['settings']
        screen.blit(settings_button, rect.topleft)

        # Leaderboard Button
        leaderboard_button = buttons["leaderboard"]
        rect = leaderboard_button.get_rect(center=(WW // 2, WH - 75))
        if mouse_rect.colliderect(rect):
            leaderboard_button = pygame.transform.smoothscale(buttons["leaderboard"], (200, 60))
            rect = leaderboard_button.get_rect(center=(WW // 2, WH - 75))
        else:
            leaderboard_button = pygame.transform.smoothscale(buttons["leaderboard"], (185, 56))
            rect = leaderboard_button.get_rect(center=(WW // 2, WH - 75))
        if clicked and mouse_rect.colliderect(rect):
            return ['leaderboard']
        screen.blit(leaderboard_button, rect.topleft)

        # Exit
        exit_button = buttons["exit"]
        rect = exit_button.get_rect(center=(WW - 100, WH - 75))
        if mouse_rect.colliderect(rect):
            exit_button = pygame.transform.smoothscale(buttons["exit"], (90, 49))
            rect = exit_button.get_rect(center=(WW - 100, WH - 75))
        else:
            exit_button = pygame.transform.smoothscale(buttons["exit"], (80, 45))
            rect = exit_button.get_rect(center=(WW - 100, WH - 75))
        if clicked and mouse_rect.colliderect(rect):
            return ['quit']
        screen.blit(exit_button, rect.topleft)

        heading_text = small_font.render('Exit', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW - 50, WH - 50)
        hover(heading_rect, screen)
        coin_display(screen)

        # Events
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()

        space.step(1.5 / FPS)
        pygame.display.update()


def game_select_screen(screen):
    clicked = False
    mx, my = pygame.mouse.get_pos()
    theme = Themes.active_theme
    while True:
        screen.fill(theme.background)
        heading_rect = (276, 395, 216, 75)
        # 276, 395, 216, 75
        if mouse_rect.colliderect(heading_rect):
            survival_button = pygame.transform.smoothscale(buttons["survival"], (232, 79))
            screen.blit(survival_button, (266, 390))
        else:
            survival_button = pygame.transform.smoothscale(buttons["survival"], (216, 75))
            screen.blit(survival_button, (276, 395))
        if clicked:
            if 266 < mx < 498 and 390 < my < 469:
                return ['survival']

        heading_text = big_font.render('Campaign', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW * 3 / 4, WH / 2)
        # 1010, 395, 250, 75
        if mouse_rect.colliderect(heading_rect):
            survival_button = pygame.transform.smoothscale(buttons["campaign"], (260, 79))
            screen.blit(survival_button, (1000, 390))
        else:
            survival_button = pygame.transform.smoothscale(buttons["campaign"], (250, 75))
            screen.blit(survival_button, (1010, 395))
        hover(heading_rect, screen)
        if clicked:
            if 1000 < mx < 1260 and 390 < my < 469:
                return ['campaign']

        heading_text = small_font.render('Back', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.topleft = (10, WH - 50)
        screen.blit(heading_text, heading_rect.topleft)

        hover(heading_rect, screen)
        if clicked:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                return ['welcome']

        # Events
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()

        pygame.display.update()


def theme_screen(screen):
    mx, my = pygame.mouse.get_pos()
    clicked = False
    while True:
        theme = Themes.active_theme
        screen.fill(theme.background)

        heading_text = big_font.render('THEMES !', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 50)
        screen.blit(heading_text, heading_rect.topleft)

        back_text = small_font.render('Back', True, theme.font_c)
        back_rect = back_text.get_rect()
        back_rect.bottomleft = (10, WH - 10)
        screen.blit(back_text, back_rect.topleft)
        hover(back_rect, screen)

        if clicked:
            if back_rect.left < mx < back_rect.right and back_rect.top < my < back_rect.bottom:
                return ['settings']

        for them, y in zip(Themes.themes, range(200, WH - 100, 60)):
            heading_text = medium_font.render(them.name, True, theme.font_c)
            heading_rect = heading_text.get_rect()
            heading_rect.center = (WW // 2, y)
            screen.blit(heading_text, heading_rect.topleft)
            hover(heading_rect, screen)

            # CLick detection
            if clicked:
                mx, my = pygame.mouse.get_pos()
                if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                    old = Themes.active_theme
                    them.set_to_active_theme()
                    DB.Cache.change_value('theme', Themes.active_theme.name, old.name)

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()

        pygame.display.update()


def score_screen(screen, score, data='None', coins=0):
    theme = Themes.active_theme
    clicked = False
    mx, my = pygame.mouse.get_pos()

    original_coins = User_data.coins
    coins_shown = 0
    to_increment = True
    increase_coin = True
    coin_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'Coin_sound.wav'))
    while True:
        screen.fill(theme.background)
        heading_text = big_font.render('You passed the Level!', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 50)
        screen.blit(heading_text, heading_rect.topleft)

        heading_text = medium_font.render(f'Your Score {score}', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 350)
        screen.blit(heading_text, heading_rect.topleft)

        heading_text = medium_font.render('Next Level', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW * 3 // 4, WH // 2 + 100)
        screen.blit(heading_text, heading_rect.topleft)

        hover(heading_rect, screen)
        if clicked:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                coin_sound.stop()
                return ['survival']

        heading_text = medium_font.render('Save and go back', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 4, WH // 2 + 100)
        screen.blit(heading_text, heading_rect.topleft)

        hover(heading_rect, screen)
        if clicked:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                DB.save_survival(data)
                coin_sound.stop()
                return ['welcome']

        if coins_shown // 2 != coins:
            coins_shown += 1
            if increase_coin:
                User_data.coins += 1
                increase_coin = False
                coin_sound.play()

            else:
                increase_coin = True

        elif to_increment:
            to_increment = False
            User_data.coins = original_coins
            User_data.increment_coins(50)
        heading_text = medium_font.render(f'Coins Earned: {coins_shown // 2}', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, WH * 3 // 4)
        screen.blit(heading_text, heading_rect.topleft)

        coin_display(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                coin_sound.stop()
                return ['quit']
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()

        pygame.display.update()


# pycharm msg below -_-
# noinspection PyUnboundLocalVariable
# pycharm msg above -_-

def leaderboard_screen(screen):
    theme = Themes.active_theme
    mx, my = pygame.mouse.get_pos()

    def global_some_data():
        global lboard_data
        lboard_data = get_data()

    t = threading.Thread(target=global_some_data)
    t.start()
    clicked = False
    while True:
        initial_coordinates = [50, 100]
        screen.fill(theme.background)
        heading_text = big_font.render('Click Ball Leaderboard!', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 50)
        screen.blit(heading_text, heading_rect.topleft)

        if len(lboard_data) != 0:
            heading_text = medium_font.render('Name', True, theme.font_c)
            heading_rect = heading_text.get_rect()
            heading_rect.topleft = (50, 100)
            screen.blit(heading_text, heading_rect.topleft)

            heading_text = medium_font.render('score', True, theme.font_c)
            heading_rect = heading_text.get_rect()
            heading_rect.topleft = (350, 100)
            screen.blit(heading_text, heading_rect.topleft)

            for obj in lboard_data:
                initial_coordinates[1] += 50  # control Y change
                screen.blit(game_font_generator(28).render(obj[0], True, theme.font_c),
                            (initial_coordinates[0], initial_coordinates[1] + 20))
                screen.blit(game_font_generator(28).render(str(obj[1]), True, theme.font_c),
                            (initial_coordinates[0] + 300, initial_coordinates[1] + 20))
        else:
            heading_text = medium_font.render('Fetching data...', True, theme.font_c)
            heading_rect = heading_text.get_rect()
            heading_rect.center = (WW / 2, 400)
            screen.blit(heading_text, heading_rect.topleft)

        heading_text = small_font.render('Back', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.bottomleft = (10, WH - 10)
        screen.blit(heading_text, heading_rect.topleft)
        hover(heading_rect, screen)

        if clicked:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                return ['welcome']

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()

        pygame.display.update()


def level_select_screen(screen):
    theme = Themes.active_theme
    clicked = False
    mx, my = pygame.mouse.get_pos()
    level = 1  ## Default level
    levels_per_page = 5
    gap = WH // levels_per_page

    max_page, min_page = 10, 1
    page = 1  ## Default page

    level_nums_to_display = range(((page - 1) * levels_per_page) + 1, (page * levels_per_page) + 1)

    while True:
        screen.fill(theme.background)
        heading_text = big_font.render('Level Select!', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 50)
        screen.blit(heading_text, heading_rect.topleft)

        heading_text = medium_font.render('Continue', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW - 100, WH - 50)
        screen.blit(heading_text, heading_rect.topleft)

        hover(heading_rect, screen)
        if clicked:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                return level

        ## Next Page
        heading_text = medium_font.render('->', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2 + 150, WH // 2)
        screen.blit(heading_text, heading_rect.topleft)

        hover(heading_rect, screen)
        if clicked and page < max_page:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                page += 1
                level_nums_to_display = range(((page - 1) * levels_per_page) + 1, (page * levels_per_page) + 1)
                clicked = False

        ## Prev Page
        heading_text = medium_font.render('<-', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2 - 150, WH // 2)
        screen.blit(heading_text, heading_rect.topleft)

        hover(heading_rect, screen)
        if clicked and page > min_page:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                page -= 1
                level_nums_to_display = range(((page - 1) * levels_per_page) + 1, (page * levels_per_page) + 1)
                clicked = False

        ## -------------------- The level selection --------------------
        for y, num in zip(range(125, WH, gap), level_nums_to_display):
            # drawing levels
            heading_text = medium_font.render('LEVEL ' + str(num), True, theme.font_c)
            heading_rect = heading_text.get_rect()
            heading_rect.center = (WW // 2, y)
            screen.blit(heading_text, heading_rect.topleft)
            ## selecting and hovering
            hover(heading_rect, screen)
            if clicked:
                if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                    level = num
            ## Drawing a selection rectangle
            if num == level:
                s_img = pygame.Surface(heading_rect.size)
                s_img.set_alpha(100)
                s_img.fill(select_rect_color)
                screen.blit(s_img, heading_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()

        pygame.display.update()


def settings_screen(screen):
    theme = Themes.active_theme
    clicked = False
    mx, my = pygame.mouse.get_pos()
    while True:
        screen.fill(theme.background)

        heading_text = big_font.render('Settings', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 50)
        screen.blit(heading_text, heading_rect.topleft)
        heading_text = medium_font.render('Change Theme', True, theme.font_c)
        rect = heading_text.get_rect()
        rect.center = (WW // 2, 250)
        if mouse_rect.colliderect(rect):
            theme_button = pygame.transform.scale(buttons["theme"], (195, 61))
            screen.blit(theme_button, (668, 217))
        else:
            theme_button = pygame.transform.scale(buttons["theme"], (180, 57))
            screen.blit(theme_button, (678, 222))

        if clicked:
            if 668 < mx < 863 and 217 < my < 278:
                return ['themes']

        heading_text = medium_font.render('Change Ball', True, theme.font_c)
        rect = heading_text.get_rect()
        rect.center = (WW // 2, 325)
        # 647, 297, 243, 57
        if mouse_rect.colliderect(rect):
            ball_button = pygame.transform.scale(buttons["ball"], (165, 61))
            screen.blit(ball_button, (680, 292))
        else:
            ball_button = pygame.transform.scale(buttons["ball"], (150, 57))
            screen.blit(ball_button, (690, 297))

        # screen.blit(heading_text, rect.topleft)
        # hover(rect, screen)

        if clicked:
            if 680 < mx < 845 and 292 < my < 353:
                return ['ball']

        heading_text = small_font.render('Back', True, theme.font_c)
        rect = heading_text.get_rect()
        rect.bottomleft = (10, WH - 10)
        screen.blit(heading_text, rect.topleft)
        hover(rect, screen)

        if clicked:
            if rect.left < mx < rect.right and rect.top < my < rect.bottom:
                return ['welcome']

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()
        pygame.display.update()


def skin_select_screen(screen):
    theme = Themes.active_theme
    clicked = False
    mx, my = pygame.mouse.get_pos()
    skin = 1  ## Default level
    skins_per_page = 5
    gap = WH // skins_per_page

    max_page, min_page = (len(skins) + skins_per_page) // skins_per_page, 1
    page = 1  ## Default page

    skin_nums_to_display = range(((page - 1) * skins_per_page) + 1, (page * skins_per_page) + 1)

    while True:
        screen.fill(theme.background)
        heading_text = big_font.render('Skin Select!', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 50)
        screen.blit(heading_text, heading_rect.topleft)

        heading_text = small_font.render('Back', True, theme.font_c)
        rect = heading_text.get_rect()
        rect.bottomleft = (10, WH - 10)
        screen.blit(heading_text, rect.topleft)
        hover(rect, screen)

        if clicked:
            if rect.left < mx < rect.right and rect.top < my < rect.bottom:
                return ['welcome', skins[skin]]

        ## Next Page
        heading_text = medium_font.render('->', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2 + 150, WH // 2)
        screen.blit(heading_text, heading_rect.topleft)

        hover(heading_rect, screen)
        if clicked and page < max_page:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                page += 1
                skin_nums_to_display = range(((page - 1) * skins_per_page) + 1, (page * skins_per_page) + 1)
                clicked = False

        ## Prev Page
        heading_text = medium_font.render('<-', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2 - 150, WH // 2)
        screen.blit(heading_text, heading_rect.topleft)

        hover(heading_rect, screen)
        if clicked and page > min_page:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                page -= 1
                skin_nums_to_display = range(((page - 1) * skins_per_page) + 1, (page * skins_per_page) + 1)
                clicked = False

        ## -------------------- The skin selection --------------------
        for y, num in zip(range(125, WH, gap), skin_nums_to_display):
            # drawing skins
            try:
                ball_img = skins[num]
                ball_img = pygame.transform.smoothscale(ball_img, (64, 64))
            except IndexError:
                ball_img = pygame.Surface((0, 0))
                ball_img.set_alpha(0)
            heading_rect = ball_img.get_rect()
            heading_rect.center = (WW // 2, y)
            screen.blit(ball_img, heading_rect.topleft)
            ## selecting and hovering
            hover(heading_rect, screen)
            if clicked:
                if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                    skin = num
            ## Drawing a selection rectangle
            if num == skin:
                s_img = pygame.Surface(heading_rect.size)
                s_img.set_alpha(100)
                s_img.fill(select_rect_color)
                screen.blit(s_img, heading_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()

        pygame.display.update()

# WIll come in handy when we will have Multiple Users :)

# def users(screen):
#     theme = Themes.active_theme
#     clicked = False
#     mx, my = pygame.mouse.get_pos()
#
#     def make_user(screen):
#         inner_running = True
#         theme = Themes.active_theme
#         while inner_running:
#             screen.fill(theme.background)
#             screen.blit(small_font.render('check console', True, theme.font_c), (WW / 2, 100))
#             pygame.display.update()
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     return ['QUIT']
#
#             DB.Users.make_user(input("Username: "), input("Password: "))
#             inner_running = False
#         DB.Cache.change_value('user', str())
#         Users.update_class_from_db(Users.users[-1])
#         data = DB.Cache.load()
#         # make a user signup here
#
#     while True:
#         screen.fill(theme.background)
#
#         heading_text = big_font.render('Users', True, theme.font_c)
#         heading_rect = heading_text.get_rect()
#         heading_rect.center = (WW // 2, 50)
#
#         if len(Users.users) == 0:
#             make_user(screen)
#         else:
#             heading_text = big_font.render(f'Current user: {Users.active_user}', True, theme.font_c)
#             heading_rect = heading_text.get_rect()
#             heading_rect.center = (WW // 2, 350)
#             screen.blit(heading_text, heading_rect.topleft)
#
#             heading_text = small_font.render('Create', True, theme.font_c)
#             heading_rect = heading_text.get_rect()
#             heading_rect.center = (WW // 2, 450)
#             screen.blit(heading_text, heading_rect.topleft)
#
#             hover(heading_rect, screen)
#             if clicked:
#                 if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
#                     make_user(screen)
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 return ['quit']
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 clicked = True
#                 mx, my = pygame.mouse.get_pos()
#
#         pygame.display.update()
