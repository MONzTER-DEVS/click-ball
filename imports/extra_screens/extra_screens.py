import random
import threading
import webbrowser

from imports.db_functions import *
from .extra_screen_functions import *

# bg_sound = pygame.mixer.Sound("assets/sounds/music.ogg")
line_mode = 1


# bg_sound.set_volume(0.04)

def welcome_screen(screen):
    mode = 0
    clicked = False
    mx, my = pygame.mouse.get_pos()
    theme = Themes.active_theme
    space = pymunk.Space()
    BORDERS = 50
    NUM_OF_BALLS = 100
    balls = []

    start_time = pygame.time.get_ticks()
    click = 0

    # https: // discord.gg / b3ScQB5bpJ
    for i in range(NUM_OF_BALLS):
        x, y = random.randint(
            BORDERS, WW - BORDERS), random.randint(BORDERS, WH - BORDERS)
        # x, y = WW//2, WH//2
        vx, vy = random.randint(0, 100), random.randint(0, 100)
        r = random.randint(10, 30)
        b = DynamicBallWithColor((x, y), vx, vy, r, space)
        b.body.mass = r * 10
        balls.append(b)

    mouse_ball = DynamicBallWithColor((mx, my), 0, 0, 100, space)

    discord_button = pygame.transform.scale(pygame.image.load('assets/imgs/discord.png').convert_alpha(), (64, 64))
    discord_rect = discord_button.get_rect()
    discord_rect.width = 64
    discord_rect.height = 64
    discord_rect.center = (50, WH - 50)

    github_button = pygame.transform.scale(pygame.image.load('assets/imgs/github.png').convert_alpha(), (64, 64))
    github_rect = discord_button.get_rect()
    github_rect.width = 64
    github_rect.height = 64
    github_rect.center = (50, WH - 120)

    more_games = Buttons(theme.button_c["more_games"], WW // 2, WH - 200, 145, 50)
    settings_button = Buttons(theme.button_c["settings"], WW // 2, WH - 125, 145, 54)

    while True:

        screen.fill(theme.background)
        # Ball
        mouse_ball.body.position = mx, my
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

        heading_text = pygame.image.load(os.path.join(
            'assets', 'imgs', 'ClickBall.png')).convert_alpha()
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW / 2, 75)
        # screen.blit(music_button, (20, 40))
        music_button = theme.button_c["music"]
        music_button = pygame.transform.smoothscale(music_button, (60, 60))
        rect = music_button.get_rect(center=(40, 40))
        music_sign = pygame.image.load("assets/imgs/music.png").convert_alpha()
        music_sign = pygame.transform.smoothscale(music_sign, (50, 50))

        if mouse_rect.colliderect(rect):
            music_button = pygame.transform.smoothscale(
                theme.button_c["music"], (70, 64))
            music_sign = pygame.transform.smoothscale(music_sign, (60, 54))
            rect = music_button.get_rect(center=(40, 40))
        else:
            music_button = pygame.transform.smoothscale(
                theme.button_c["music"], (60, 60))
            music_sign = pygame.transform.smoothscale(music_sign, (50, 50))
            rect = music_button.get_rect(center=(40, 40))
        music_sign_rect = (rect.topleft[0] + 5, rect.topleft[1] + 5)
        screen.blit(music_button, rect.topleft)
        screen.blit(music_sign, music_sign_rect)

        if clicked and mouse_rect.colliderect(rect):
            toggle_music()

        if not Music.play:
            pygame.draw.line(screen, RED, (music_sign_rect[0] + 5, music_sign_rect[1] + 10),
                             (rect.bottomright[0] - 10, rect.bottomright[1] - 15), 7)

        screen.blit(heading_text, heading_rect.topleft)

        # Play button
        try:
            play_button.draw(screen, mx, my)
        except Exception:
            play_button = Buttons(
                theme.button_c["play"], WW // 2, 215, 150, 65)
        if play_button.is_clicked(clicked, mx, my):
            return ['campaign', "select"]
        hover(heading_rect, screen)

        # Settings Button
        settings_button.draw(screen, mx, my)
        if settings_button.is_clicked(clicked, mx, my):
            return ['settings']
        hover(heading_rect, screen)

        more_games.draw(screen, mx, my)
        if more_games.is_clicked(clicked, mx, my):
            return ["more_games"]

        # How to play button
        instructions_text = small_font.render(
            "Instructions", True, theme.font_c)
        try:
            instructions_button.draw(screen, mx, my)
        except Exception as e:
            instructions_button = Buttons(
                theme.button_c['instructions'], WW // 2, WH - 50, 180, 54)
        if instructions_button.is_clicked(clicked, mx, my):
            return ['guide']

        # Exit
        try:
            exit_button.draw(screen, mx, my)
        except Exception as e:
            exit_button = Buttons(
                theme.button_c["exit"], WW - 100, WH - 75, 100, 50)
        if exit_button.is_clicked(clicked, mx, my):
            return ['quit']

        # todo make Discord image better
        screen.blit(discord_button, discord_rect)

        if mouse_rect.colliderect(discord_rect) and clicked:
            webbrowser.open_new('https://discord.gg/b3ScQB5bpJ')

        screen.blit(github_button, github_rect)

        if mouse_rect.colliderect(github_rect) and clicked:
            webbrowser.open_new('https://github.com/MONzTER-DEVS/click-ball')

        hover(heading_rect, screen)

        coin_display(screen, coins=User_data.coins)
        draw_cursor(screen, theme.cursor_c)

        # Events
        mx, my = pygame.mouse.get_pos()
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False

        space.step(1.5 / FPS)
        pygame.display.update()


def theme_screen(screen):
    clicked = False
    while True:
        theme = Themes.active_theme
        screen.fill(theme.background)
        mx, my = pygame.mouse.get_pos()
        # music_button = theme.button_c["music"]
        # music_button = pygame.transform.smoothscale(music_button, (60, 60))
        # rect = music_button.get_rect(center=(40, 40))
        # if mouse_rect.colliderect(rect):
        #     music_button = pygame.transform.smoothscale(theme.button_c["music"], (70, 64))
        #     rect = music_button.get_rect(center=(40, 40))
        # else:
        #     music_button = pygame.transform.smoothscale(theme.button_c["music"], (60, 60))
        #     rect = music_button.get_rect(center=(40, 40))
        # screen.blit(music_button, rect.topleft)
        # if clicked and mouse_rect.colliderect(rect):
        #     pass
        heading_text = big_font.render('THEMES !', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 50)
        screen.blit(heading_text, heading_rect.topleft)

        # Back button
        try:
            back_button = Buttons(theme.button_c["back"], 60, WH - 50, 100, 60)
            back_button.draw(screen, mx, my)
        except Exception as e:
            back_button = Buttons(theme.button_c["back"], 60, WH - 50, 100, 60)
        if back_button.is_clicked(clicked, mx, my):
            return ['settings']

        for them, y in zip(Themes.themes, range(200, WH - 100, 60)):
            theme_text = medium_font.render(them.name, True, theme.font_c)
            theme_rect = theme_text.get_rect()
            theme_button = Buttons(theme_text, WW // 2,
                                   y, theme_rect.w, theme_rect.h)
            theme_button.draw(screen, mx, my)
            if theme_button.is_clicked(clicked, mx, my):
                old = Themes.active_theme
                them.set_to_active_theme()
                DB.Cache.change_value(
                    'theme', Themes.active_theme.name, old.name)

        draw_cursor(screen, theme.cursor_c)
        coin_display(screen, coins=User_data.coins)  ## coins

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False

        pygame.display.update()


def score_screen(screen, score, data=None):
    theme = Themes.active_theme
    clicked = False

    while True:
        screen.fill(theme.background)
        mx, my = pygame.mouse.get_pos()

        heading_text = big_font.render(
            'You passed the Level!', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 50)
        screen.blit(heading_text, heading_rect.topleft)

        heading_text = medium_font.render(
            f'Your Score {score}', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 350)
        screen.blit(heading_text, heading_rect.topleft)

        hover(heading_rect, screen)
        # next level button
        try:
            next_button.draw(screen, mx, my)
        except Exception as e:
            next_button = Buttons(
                theme.button_c["next level"], WW * 3 // 4, WH // 2 + 100, 250, 75)
        if next_button.is_clicked(clicked, mx, my):
            return ['survival']

        # Exit button
        try:
            exit_button.draw(screen, mx, my)
        except Exception as e:
            exit_button = Buttons(
                theme.button_c["exit"], WW // 4, WH // 2 + 100, 120, 75)
        if exit_button.is_clicked(clicked, mx, my):
            if data is not None:
                DB.save_survival(data)
            return ['welcome']

        coin_display(screen, User_data.coins)
        draw_cursor(screen, theme.cursor_c)

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # coin_sound.stop()
                return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()

        pygame.display.update()


def guide_screen(screen):
    start_time_guide = pygame.time.get_ticks()
    theme = Themes.active_theme
    mx, my = pygame.mouse.get_pos()
    clicked = False
    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill(theme.background)
        heading_text = big_font.render(
            'Instructions For The Game!', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 50)
        screen.blit(heading_text, heading_rect.topleft)
        if not clicked:
            instruction_text = medium_font.render(
                "Instructions!", True, theme.font_c)
            instruction_rect = instruction_text.get_rect()
            instruction_rect.center = (WW // 6 - 55, WH // 6)
            screen.blit(instruction_text, instruction_rect.topleft)
            explanation = "aim of the game is the player(ball) has to reach the flag by clicking on the different spots. Each click counts one move.The level has to be completed in limited moves after dodging the obstacles in the way likes ball, etc." \
                          "There are two modes in the game - 'Campaign' and 'Survival'." \
                          "In the Campaign Mode, there are 25 levels.Clearing each level would hop on to the next level." \
                          "In the Survival Mode, you have to clear each level simultaneously. Losing a level would result in playing the game from the first level....After you lose then you can send your data to the Leaderboard and check you position there afterwards..." \
                          "There are many themes and ball skins available in the Settings which can be unlocked and used on the basis of the coins collected...So what's the delay for ? Play and Enjoy the Game...."
            exp_list = explanation.split(" ")
            current_time = pygame.time.get_ticks()
            text = tiny_font.render("The", True, theme.font_c)
            rect = text.get_rect()
            rect.topleft = (22, rect.top)
            rect.top = instruction_rect.bottom
            screen.blit(text, rect.topleft)
            top_right = rect.topright

            for l in range(0, len(exp_list)):
                if current_time - start_time_guide > exp_list.index(exp_list[l]) * 100:
                    current_text = tiny_font.render(
                        exp_list[l], True, theme.font_c)
                    current_rect = current_text.get_rect()
                    if top_right[0] > WW - 200:
                        top_right[0] = 15
                        top_right[1] += 40

                    current_rect.topleft = (top_right[0] + 10, top_right[1])
                    top_right = list(current_rect.topright)
                    screen.blit(current_text, current_rect.topleft)

        # Back button
        try:
            back_button.draw(screen, mx, my)
        except Exception as e:
            back_button = Buttons(theme.button_c["back"], 60, WH - 50, 100, 60)
        if back_button.is_clicked(clicked, mx, my):
            return ['welcome']

        draw_cursor(screen, theme.cursor_c)
        coin_display(screen, coins=User_data.coins)  ## coins

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                start_time_guide -= 1000000

        pygame.display.update()


def level_select_screen(screen, number_buttons):
    theme = Themes.active_theme
    clicked = False
    mx, my = pygame.mouse.get_pos()
    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill(theme.background)
        heading_text = big_font.render('Level Map!', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 50)
        screen.blit(heading_text, heading_rect.topleft)
        # music_button = theme.button_c["music"]
        # music_button = pygame.transform.smoothscale(music_button, (60, 60))
        # rect = music_button.get_rect(center=(40, 40))
        # if mouse_rect.colliderect(rect):
        #     music_button = pygame.transform.smoothscale(theme.button_c["music"], (70, 64))
        #     rect = music_button.get_rect(center=(40, 40))
        # else:
        #     music_button = pygame.transform.smoothscale(theme.button_c["music"], (60, 60))
        #     rect = music_button.get_rect(center=(40, 40))
        # screen.blit(music_button, rect.topleft)
        # if clicked and mouse_rect.colliderect(rect):
        #     pass
        # Back button
        try:
            back_button.draw(screen, mx, my)
        except Exception as e:
            back_button = Buttons(theme.button_c["back"], 60, WH - 50, 100, 60)
        if back_button.is_clicked(clicked, mx, my):
            return 'back'

        counter = 0
        for i in range(1, 6):
            for j in range(1, 6):
                counter += 1

                if counter <= User_data.current_level:
                    temp_img = number_buttons[counter]
                    temp_button = Buttons(
                        temp_img, j * WW / 6, i * WH / 6 + 50, 65, 65)
                    temp_button.draw(screen, mx, my)
                    if temp_button.is_clicked(clicked, mx, my):
                        return counter
                else:
                    temp_img = number_buttons[0]
                    _rect = temp_img.get_rect()
                    _rect.center = (j * WW / 6, i * WH / 6 + 50)
                    screen.blit(temp_img, _rect.topleft)

        # if clicked:
        #     if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
        # #         return level
        #
        # ## Next Page
        # heading_text = medium_font.render('->', True, theme.font_c)
        # heading_rect = heading_text.get_rect()
        # heading_rect.center = (WW // 2 + 150, WH // 2)
        # screen.blit(heading_text, heading_rect.topleft)
        #
        # hover(heading_rect, screen)
        # if clicked and page < max_page:
        #     if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
        #         page += 1
        #         level_nums_to_display = range(((page - 1) * levels_per_page) + 1, (page * levels_per_page) + 1)
        #         clicked = False
        #
        # ## Prev Page
        # heading_text = medium_font.render('<-', True, theme.font_c)
        # heading_rect = heading_text.get_rect()
        # heading_rect.center = (WW // 2 - 150, WH // 2)
        # screen.blit(heading_text, heading_rect.topleft)
        #
        # hover(heading_rect, screen)
        # if clicked and page > min_page:
        #     if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
        #         page -= 1
        #         level_nums_to_display = range(((page - 1) * levels_per_page) + 1, (page * levels_per_page) + 1)
        #         clicked = False
        #
        # ## -------------------- The level selection --------------------
        # for y, num in zip(range(125, WH, gap), level_nums_to_display):
        #     # drawing levels
        #     heading_text = medium_font.render('LEVEL ' + str(num), True, theme.font_c)
        #     heading_rect = heading_text.get_rect()
        #     heading_rect.center = (WW // 2, y)
        #     screen.blit(heading_text, heading_rect.topleft)
        #     ## selecting and hovering
        #     hover(heading_rect, screen)
        #     if clicked:
        #         if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
        #             level = num

        draw_cursor(screen, theme.cursor_c)
        coin_display(screen, coins=User_data.coins)  ## coins

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        pygame.display.update()


def music_screen(screen):
    theme = Themes.active_theme
    clicked = False
    mx, my = pygame.mouse.get_pos()
    while True:
        screen.fill(theme.background)
        mx, my = pygame.mouse.get_pos()

        heading_text = big_font.render('Select Music', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 50)
        screen.blit(heading_text, heading_rect.topleft)
        draw_cursor(screen, theme.cursor_c)
        coin_display(screen, coins=User_data.coins)  ## coins
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
        try:
            back_button.draw(screen, mx, my)
        except Exception as e:
            back_button = Buttons(theme.button_c["back"], 60, WH - 50, 100, 60)
        if back_button.is_clicked(clicked, mx, my):
            return ['settings']
        # ball_text = medium_font.render('Change Ball', True, theme.font_c)
        # try:
        #     ball_button.draw(screen, mx, my)
        # except Exception as e:
        #     ball_button = Buttons(ball_text, WW // 2, 325, 250, 57)
        # if ball_button.is_clicked(clicked, mx, my):
        #     return ['ball']
        pygame.display.update()


def settings_screen(screen):
    theme = Themes.active_theme
    clicked = False
    mx, my = pygame.mouse.get_pos()
    while True:
        screen.fill(theme.background)
        mx, my = pygame.mouse.get_pos()

        heading_text = big_font.render('Settings', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 50)
        screen.blit(heading_text, heading_rect.topleft)
        # Change Theme button
        theme_text = medium_font.render('Change Theme', True, theme.font_c)
        try:
            theme_button.draw(screen, mx, my)
        except Exception as e:
            theme_button = Buttons(theme_text, WW // 2, 250, 300, 57)
        if theme_button.is_clicked(clicked, mx, my):
            return ['themes']

        # music_button = theme.button_c["music"]
        # music_button = pygame.transform.smoothscale(music_button, (60, 60))
        # rect = music_button.get_rect(center=(40, 40))
        # if mouse_rect.colliderect(rect):
        #     music_button = pygame.transform.smoothscale(theme.button_c["music"], (70, 64))
        #     rect = music_button.get_rect(center=(40, 40))
        # else:
        #     music_button = pygame.transform.smoothscale(theme.button_c["music"], (60, 60))
        #     rect = music_button.get_rect(center=(40, 40))
        # screen.blit(music_button, rect.topleft)
        # if clicked and mouse_rect.colliderect(rect):
        #     pass

        # Change ball button
        ball_text = medium_font.render('Change Ball', True, theme.font_c)
        try:
            ball_button.draw(screen, mx, my)
        except Exception as e:
            ball_button = Buttons(ball_text, WW // 2, 325, 250, 57)
        if ball_button.is_clicked(clicked, mx, my):
            return ['ball']

        # Change line button
        line_text = medium_font.render('Change Line', True, theme.font_c)
        try:
            line_button.draw(screen, mx, my)
        except Exception as e:
            line_button = Buttons(line_text, WW // 2, 400, 250, 57)
        if line_button.is_clicked(clicked, mx, my):
            return ['line']

        # Change Music button
        music_text = medium_font.render('Change Music', True, theme.font_c)
        try:
            music_button.draw(screen, mx, my)
        except Exception as e:
            music_button = Buttons(music_text, WW // 2, 475, 250, 57)
        if music_button.is_clicked(clicked, mx, my):
            return ['music']

        # Fullscreen button
        full_text = medium_font.render('Toggle Fullscreen', True, theme.font_c)
        try:
            full_button.draw(screen, mx, my)
        except Exception as e:
            full_button = Buttons(full_text, WW // 2, 550, 300, 57)
        if full_button.is_clicked(clicked, mx, my):
            conn = sqlite3.connect(DB.db_path)
            c = conn.cursor()
            c.execute(f"SELECT * FROM display")
            size = c.fetchall()[0][0]
            if size == "full":
                c.execute("UPDATE display SET size = 'standard'")
            else:
                c.execute("UPDATE display SET size = 'full'")

            conn.commit()
            conn.close()
            pygame.display.toggle_fullscreen()

        # Back button
        try:
            back_button.draw(screen, mx, my)
        except Exception as e:
            back_button = Buttons(theme.button_c["back"], 60, WH - 50, 100, 60)
        if back_button.is_clicked(clicked, mx, my):
            return ['welcome']
        clicked = False

        draw_cursor(screen, theme.cursor_c)
        coin_display(screen, coins=User_data.coins)  ## coins

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
        pygame.display.update()


def line_select_screen(screen):
    print(1)
    theme = Themes.active_theme
    clicked = False
    mx, my = pygame.mouse.get_pos()
    mouse_ = pygame.Rect(0, 0, 10, 10)
    mouse_.center = (mx, my)
    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill(theme.background)
        heading_text = big_font.render('Line Select!', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 50)
        screen.blit(heading_text, heading_rect.topleft)

        # Line one
        line_one = pygame.image.load("assets/imgs/lines/line_one.png")
        try:
            line_one_button.draw(screen, mx, my)
        except Exception as e:
            line_one_button = Buttons(
                line_one, WW // 2, WH // 2 - 100, 680, 60)

        if line_one_button.is_clicked(clicked, mx, my):
            line_select("old")
            return ['welcome']

        # Line two
        line_two = pygame.image.load("assets/imgs/lines/line_two.png")
        try:
            line_two_button.draw(screen, mx, my)
        except Exception as e:
            line_two_button = Buttons(
                line_two, WW // 2, WH // 2 + 100, 680, 60)

        if line_two_button.is_clicked(clicked, mx, my):
            line_select("new")
            return ['welcome']

        try:
            back_button.draw(screen, mx, my)
        except Exception as e:
            back_button = Buttons(theme.button_c["back"], 60, WH - 50, 100, 60)

        if back_button.is_clicked(clicked, mx, my):
            return ['welcome']

        draw_cursor(screen, theme.cursor_c)
        coin_display(screen, coins=User_data.coins)  ## coins

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()
                mouse_ = pygame.Rect(0, 0, 10, 10)
                mouse_.center = (mx, my)

        pygame.display.update()


def skin_select_screen(screen, skins):
    theme = Themes.active_theme
    heading_text = big_font.render('Shop', True, theme.font_c)
    heading_rect = heading_text.get_rect()
    heading_rect.center = (WW // 2, 50)

    clicked = False
    active_ball = None
    while True:
        pygame.display.update()
        mx, my = pygame.mouse.get_pos()
        screen.fill(theme.background)
        screen.blit(heading_text, heading_rect.topleft)

        counter = 0
        radius = 30
        for i in range(1, 6):
            for j in range(1, 6):
                ball = skins[counter][1]
                coords = (j * WW / 6, (i * WH / 8) + 50)

                if ball.name in User_data.skins:
                    pygame.draw.circle(screen, (0, 255, 0), (coords[0], coords[1]), radius)

                # screen.blit(ball.surface, coords)
                ball_button = Buttons(ball.surface, coords[0], coords[1], ball.surface.get_rect().w,
                                      ball.surface.get_rect().h)
                ball_button.draw(screen, mx, my)

                if ball_button.is_clicked(clicked, mx, my):
                    active_ball = ball
                    active_ball_cost = counter * 100

                if counter < 22:
                    counter += 1
                else:
                    break
            else:
                continue
            break

        try:
            back_button.draw(screen, mx, my)
        except Exception as e:
            back_button = Buttons(theme.button_c["back"], 60, WH - 50, 100, 60)
        if back_button.is_clicked(clicked, mx, my):
            return ['welcome']

        if active_ball is not None:
            if active_ball.name not in User_data.skins:
                if User_data.coins > active_ball_cost:
                    text = medium_font.render(f"Buy now: {active_ball_cost}", True, theme.font_c)
                    text_button = Buttons(text, WW - 200, WH - 50, text.get_rect().w, text.get_rect().h)
                    text_button.draw(screen, mx, my)
                    if text_button.is_clicked(clicked, mx, my):
                        User_data.active_skin = skins[int(active_ball_cost / 100)][0]
                        User_data.increment_coins(-active_ball_cost)
                        User_data.add_skin(active_ball.name)

                else:
                    text = medium_font.render(f"Not enough Money!", True, theme.font_c)
                    text_button = Buttons(text, WW - 250, WH - 50, text.get_rect().w, text.get_rect().h)
                    text_button.draw(screen, mx, my)
            else:
                text = medium_font.render("Activate", True, theme.font_c)
                text_button = Buttons(text, WW - 200, WH - 50, text.get_rect().w, text.get_rect().h)
                text_button.draw(screen, mx, my)
                if text_button.is_clicked(clicked, mx, my):
                    User_data.active_skin = skins[int(active_ball_cost / 100)][0]

        draw_cursor(screen, theme.cursor_c)
        coin_display(screen, int(str(User_data.coins)))  # coins
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False


def campaign_continue_screen(screen, coins):
    theme = Themes.active_theme
    clicked = False
    running = True

    heading_text = big_font.render(
        'Congratulations! You passed the Level', True, theme.font_c)
    heading_rect = heading_text.get_rect()
    heading_rect.center = (WW // 2, 50)

    # continue_text = small_font.render('Continue', True, theme.font_c)
    # continue_rect = continue_text.get_rect()
    # continue_rect.center = (WW // 4, WH // 2)

    User_data.increment_coins(coins)
    while running:
        mx, my = pygame.mouse.get_pos()
        screen.fill(theme.background)
        # music_button = theme.button_c["music"]
        # music_button = pygame.transform.smoothscale(music_button, (60, 60))
        # rect = music_button.get_rect(center=(40, 40))
        # if mouse_rect.colliderect(rect):
        #     music_button = pygame.transform.smoothscale(theme.button_c["music"], (70, 64))
        #     rect = music_button.get_rect(center=(40, 40))
        # else:
        #     music_button = pygame.transform.smoothscale(theme.button_c["music"], (60, 60))
        #     rect = music_button.get_rect(center=(40, 40))
        # screen.blit(music_button, rect.topleft)
        # if clicked and mouse_rect.colliderect(rect):
        #     pass

        screen.blit(heading_text, heading_rect.topleft)  # Heading

        coin_text = small_font.render(
            f'Coins Earned: {coins}', True, theme.font_c)
        coin_rect = coin_text.get_rect()
        coin_rect.center = (WW // 2, 300)
        screen.blit(coin_text, coin_rect)

        # Continue button
        try:
            continue_button.draw(screen, mx, my)
        except Exception as e:
            continue_button = Buttons(
                theme.button_c["continue"], WW // 4, WH // 2, 150, 60)
        if continue_button.is_clicked(clicked, mx, my):
            return ['continue']

        # map button
        map_text = small_font.render('Level Map', True, theme.font_c)
        try:
            map_button.draw(screen, mx, my)
        except Exception as e:
            map_button = Buttons(theme.button_c['level_map'], int(WW * 3) // 4, WH // 2, 150, 60)
        if map_button.is_clicked(clicked, mx, my):
            return ['level_map']

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        draw_cursor(screen, theme.cursor_c)
        coin_display(screen, coins=User_data.coins)  ## coins
        pygame.display.update()


def campaign_death_screen(screen):
    theme = Themes.active_theme
    clicked = False

    running = True

    heading_text = big_font.render('Game Over!', True, theme.font_c)
    heading_rect = heading_text.get_rect()
    heading_rect.center = (WW // 2, 50)

    while running:
        mx, my = pygame.mouse.get_pos()
        screen.fill(theme.background)
        # music_button = theme.button_c["music"]
        # music_button = pygame.transform.smoothscale(music_button, (60, 60))
        # rect = music_button.get_rect(center=(40, 40))
        # if mouse_rect.colliderect(rect):
        #     music_button = pygame.transform.smoothscale(theme.button_c["music"], (70, 64))
        #     rect = music_button.get_rect(center=(40, 40))
        # else:
        #     music_button = pygame.transform.smoothscale(theme.button_c["music"], (60, 60))
        #     rect = music_button.get_rect(center=(40, 40))
        # screen.blit(music_button, rect.topleft)
        # if clicked and mouse_rect.colliderect(rect):
        #     pass
        screen.blit(heading_text, heading_rect.topleft)

        map_text = small_font.render('Level Map', True, theme.font_c)
        try:
            map_button.draw(screen, mx, my)
        except Exception as e:
            map_button = Buttons(theme.button_c['level_map'], int(WW * 3) // 4, WH // 2, 150, 60)
        if map_button.is_clicked(clicked, mx, my):
            return ['level_map']

        restart_text = small_font.render('Restart', True, theme.font_c)
        try:
            restart_button.draw(screen, mx, my)
        except Exception as e:
            restart_button = Buttons(theme.button_c['restart'], WW // 4, WH // 2, 150, 60)
        if restart_button.is_clicked(clicked, mx, my):
            return ['restart']

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        draw_cursor(screen, theme.cursor_c)
        coin_display(screen, coins=User_data.coins)  ## coins
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
# if event.type == pygame.MOUSEBUTTONUP:
#     clicked = False
#
#         pygame.display.update()
