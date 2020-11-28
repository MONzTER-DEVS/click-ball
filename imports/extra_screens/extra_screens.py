import threading
from imports.classes import *
from .extra_screen_functions import *
from imports.db_functions import *

# Declaring some Variables
lboard_data = []


def welcome_screen(screen):
    clicked = False
    mx, my = pygame.mouse.get_pos()
    theme = Themes.active_theme
    while True:
        screen.fill(theme.background)

        # display
        heading_text = big_font.render('Clicker Ball!', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW / 2, 50)
        screen.blit(heading_text, heading_rect.topleft)

        heading_text = medium_font.render('Game', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW / 2, 250)
        screen.blit(heading_text, heading_rect.topleft)

        hover(heading_rect, screen)
        if clicked:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                return ['game']

        # Themes Screen
        heading_text = small_font.render('Settings', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW / 2, WH - 100)
        screen.blit(heading_text, heading_rect.topleft)
        hover(heading_rect, screen)
        if clicked:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                return ['settings']

        # Leaderboard
        heading_text = small_font.render('Leaderboard', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW / 2, WH - 50)
        screen.blit(heading_text, heading_rect.topleft)
        hover(heading_rect, screen)
        if clicked:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                return ['leaderboard']

        # Exit
        heading_text = small_font.render('Exit', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW - 50, WH - 50)
        screen.blit(heading_text, heading_rect.topleft)
        hover(heading_rect, screen)
        if clicked:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                return ['quit']

        # Events
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()

        pygame.display.update()


def game_select_screen(screen):
    clicked = False
    mx, my = pygame.mouse.get_pos()
    theme = Themes.active_theme
    while True:
        screen.fill(theme.background)

        heading_text = big_font.render('Survival', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW / 4, WH / 2)
        screen.blit(heading_text, heading_rect.topleft)

        hover(heading_rect, screen)
        if clicked:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                return ['survival']

        heading_text = big_font.render('Campaign', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW * 3 / 4, WH / 2)
        screen.blit(heading_text, heading_rect.topleft)

        hover(heading_rect, screen)
        if clicked:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
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


def score_screen(screen, score, data='None'):
    theme = Themes.active_theme
    clicked = False
    mx, my = pygame.mouse.get_pos()
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

        heading_text = medium_font.render('Continue', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 4, WH // 2 + 100)
        screen.blit(heading_text, heading_rect.topleft)

        hover(heading_rect, screen)
        if clicked:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                return ['survival']

        heading_text = medium_font.render('Save and go back', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (int((WW * 3) // 4), WH // 2 + 100)
        screen.blit(heading_text, heading_rect.topleft)

        hover(heading_rect, screen)
        if clicked:
            if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
                DB.save_survival(data)
                return ['welcome']

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
        screen.blit(heading_text, rect.topleft)
        hover(rect, screen)

        if clicked:
            if rect.left < mx < rect.right and rect.top < my < rect.bottom:
                return ['themes']

        heading_text = medium_font.render('Change Ball', True, theme.font_c)
        rect = heading_text.get_rect()
        rect.center = (WW // 2, 325)
        screen.blit(heading_text, rect.topleft)
        hover(rect, screen)

        if clicked:
            if rect.left < mx < rect.right and rect.top < my < rect.bottom:
                return ['ball']

        heading_text = small_font.render('Back', True, theme.font_c)
        rect = heading_text.get_rect()
        rect.bottomleft = (10, WH - 10)
        screen.blit(heading_text, rect.topleft)
        hover(rect, screen)

        if clicked:
            if rect.left < mx < rect.right and rect.top < my < rect.bottom:
                return ['settings']

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
