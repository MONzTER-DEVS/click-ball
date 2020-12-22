import random
import threading

from imports.db_functions import *
from .extra_screen_functions import *

# Declaring some Variables
lboard_data = []

## Size is 204 x 81
## Ratio is 51/20
bg_sound = pygame.mixer.Sound("assets/sounds/music2.ogg")


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
    name_text = medium_font.render(f"Name: {DB.fetch_name()}", True, theme.font_c)
    name_rect = name_text.get_rect()
    name_rect.midleft = (10, WH - 50)
    start_time = pygame.time.get_ticks()
    click = 0
    for i in range(NUM_OF_BALLS):
        x, y = random.randint(BORDERS, WW - BORDERS), random.randint(BORDERS, WH - BORDERS)
        # x, y = WW//2, WH//2
        vx, vy = random.randint(0, 100), random.randint(0, 100)
        r = random.randint(10, 30)
        b = DynamicBallWithColor((x, y), vx, vy, r, space)
        balls.append(b)

    mouse_ball = DynamicBallWithColor((mx, my), 0, 0, 100, space)

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

        heading_text = pygame.image.load(os.path.join('assets', 'imgs', 'ClickBall.png')).convert_alpha()
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW / 2, 75)
        # screen.blit(music_button, (20, 40))
        music_button = theme.button_c["music"]
        music_button = pygame.transform.smoothscale(music_button, (60, 60))
        rect = music_button.get_rect(center=(40, 40))
        music_sign = pygame.image.load("assets/imgs/music.png").convert_alpha()
        music_sign = pygame.transform.smoothscale(music_sign, (50, 50))

        if mouse_rect.colliderect(rect):
            music_button = pygame.transform.smoothscale(theme.button_c["music"], (70, 64))
            music_sign = pygame.transform.smoothscale(music_sign, (60, 54))
            rect = music_button.get_rect(center=(40, 40))
        else:
            music_button = pygame.transform.smoothscale(theme.button_c["music"], (60, 60))
            music_sign = pygame.transform.smoothscale(music_sign, (50, 50))
            rect = music_button.get_rect(center=(40, 40))
        music_sign_rect = (rect.topleft[0] + 5, rect.topleft[1] + 5)
        screen.blit(music_button, rect.topleft)
        screen.blit(music_sign, music_sign_rect)

        if clicked and mouse_rect.colliderect(rect):
            if User_data.music:
                toggle_music()
            else:
                toggle_music()

        if not User_data.music:
            pygame.draw.line(screen, RED, (music_sign_rect[0] + 5, music_sign_rect[1] + 10),
                             (rect.bottomright[0] - 10, rect.bottomright[1] - 15), 7)

        # if clicked and mouse_rect.colliderect(rect) and click_count == 0:
        #     click = 1
        #     click_count = 1
        # if clicked and mouse_rect.colliderect(rect) and click_count == 2:
        #     pygame.mixer.music.play(-1)
        #     current_time = pygame.time.get_ticks()
        #     if start_time - current_time < 1000:
        #         if clicked and mouse_rect.colliderect(rect):
        #             click_count = 1
        #             click = 1
        # if click_count == 1 and click == 1:
        #     pygame.mixer.music.stop()
        #     click_count = 2

        screen.blit(heading_text, heading_rect.topleft)
        screen.blit(name_text, name_rect.topleft)

        # Play button
        try:
            play_button.draw(screen, mx, my)
        except Exception as e:
            play_button = Buttons(theme.button_c["play"], WW//2, 215, 150, 65)
        if play_button.is_clicked(clicked, mx, my):
            return ['game']
        hover(heading_rect, screen)

        # Settings Button
        try:
            settings_button.draw(screen, mx, my)
        except Exception as e:
            settings_button = Buttons(theme.button_c["settings"], WW // 2, WH - 225, 145, 54)
        if settings_button.is_clicked(clicked, mx, my):
            return ['settings']
        hover(heading_rect, screen)

        # How to play button
        instructions_text = small_font.render("Instructions", True, theme.font_c)
        try:
            instructions_button.draw(screen, mx, my)
        except Exception as e:
            instructions_button = Buttons(instructions_text, WW // 2, WH - 150, 200, 54)
        if instructions_button.is_clicked(clicked, mx, my):
            return ['guide']

        # Leaderboard Button
        try:
            leaderboard_button.draw(screen, mx, my)
        except Exception as e:
            leaderboard_button = Buttons(theme.button_c["leaderboard"], WW // 2, WH - 75, 185, 56)
        if leaderboard_button.is_clicked(clicked, mx, my):
            return ['leaderboard']
        hover(heading_rect, screen)

        # Exit
        try:
            exit_button.draw(screen, mx, my)
        except Exception as e:
            exit_button = Buttons(theme.button_c["exit"], WW - 100, WH - 75, 100, 50)
        if exit_button.is_clicked(clicked, mx, my):
            return ['quit']

        hover(heading_rect, screen)

        coin_display(screen, coins=User_data.coins)

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


def game_select_screen(screen):
    clicked = False
    mx, my = pygame.mouse.get_pos()
    theme = Themes.active_theme
    while True:

        screen.fill(theme.background)
        mx, my = pygame.mouse.get_pos()

        # survival button
        try:
            survival_button.draw(screen, mx, my)
        except Exception as e:
            survival_button = Buttons(theme.button_c["survival"], WW/4,  WH/2, 216, 75)
        if survival_button.is_clicked(clicked, mx, my):
            return ['survival']

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

        # Campaign button
        try:
            campaign_button.draw(screen, mx, my)
        except Exception as e:
            campaign_button = Buttons(theme.button_c["campaign"], WW * 3 / 4, WH / 2, 250, 75)
        if campaign_button.is_clicked(clicked, mx, my):
            return ['campaign', 'map']

        # Back Button
        try:
            back_button.draw(screen, mx, my)
        except Exception as e:
            back_button = Buttons(theme.button_c["back"], 60, WH - 50, 100, 60)
        if back_button.is_clicked(clicked, mx, my):
            return ['welcome']

        # Events
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
            back_button.draw(screen, mx, my)
        except Exception as e:
            back_button = Buttons(theme.button_c["back"], 60, WH - 50, 100, 60)
        if back_button.is_clicked(clicked, mx, my):
            return ['settings']

        for them, y in zip(Themes.themes, range(200, WH - 100, 60)):
            theme_text = medium_font.render(them.name, True, theme.font_c)
            theme_rect = theme_text.get_rect()
            theme_button = Buttons(theme_text, WW // 2, y, theme_rect.w, theme_rect.h)
            theme_button.draw(screen, mx, my)
            if theme_button.is_clicked(clicked, mx, my):
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
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False

        pygame.display.update()


def score_screen(screen, score, data='None', coins=0):
    theme = Themes.active_theme
    clicked = False
    mx, my = pygame.mouse.get_pos()

    coin_state = "ongoing"
    step = 0
    coins_shown = 0  # show Number of coins

    # coin_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'coin_appear.wav'))
    # coin_sound.set_volume(0.004)

    while True:
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
        heading_text = big_font.render('You passed the Level!', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 50)
        screen.blit(heading_text, heading_rect.topleft)

        heading_text = medium_font.render(f'Your Score {score}', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 350)
        screen.blit(heading_text, heading_rect.topleft)

        hover(heading_rect, screen)
        # next level button
        try:
            next_button.draw(screen, mx, my)
        except Exception as e:
            next_button = Buttons(theme.button_c["next level"], WW * 3 // 4, WH // 2 + 100, 250, 75)
        if next_button.is_clicked(clicked, mx, my):
            return ['survival']

        # next_level_button = theme.button_c["next level"]
        # rect = next_level_button.get_rect(center=(WW * 3 // 4, WH // 2 + 100))
        # if mouse_rect.colliderect(rect):
        #     next_level_button = pygame.transform.smoothscale(theme.button_c["next level"], (260, 79))
        #     rect = next_level_button.get_rect(center=(WW * 3 // 4, WH // 2 + 100))
        # else:
        #     next_level_button = pygame.transform.smoothscale(theme.button_c["next level"], (250, 75))
        #     rect = next_level_button.get_rect(center=(WW * 3 // 4, WH // 2 + 100))
        # hover(heading_rect, screen)
        # if clicked and mouse_rect.colliderect(rect):
        #     # coin_sound.stop()
        #     return ['survival']
        # screen.blit(next_level_button, rect.topleft)
        exit_button = theme.button_c["exit"]
        rect = exit_button.get_rect(center=(WW // 4, WH // 2 + 100))
        if mouse_rect.colliderect(rect):
            exit_button = pygame.transform.smoothscale(theme.button_c["exit"], (130, 79))
            rect = exit_button.get_rect(center=(WW // 4, WH // 2 + 100))
        else:
            exit_button = pygame.transform.smoothscale(theme.button_c["exit"], (120, 75))
            rect = exit_button.get_rect(center=(WW // 4, WH // 2 + 100))
        if clicked and mouse_rect.colliderect(rect):
            DB.save_survival(data)
            # coin_sound.stop()
            return ['welcome']
        screen.blit(exit_button, rect.topleft)
        hover(heading_rect, screen)

        if coin_state == "ongoing":
            if coins_shown == coins:
                coin_state = "finished"
                User_data.increment_coins(coins)
            else:
                coins_shown += 1

        heading_text = medium_font.render(f'Coins Earned: {coins_shown}', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, WH * 3 // 4)
        screen.blit(heading_text, heading_rect.topleft)

        if coin_state == "ongoing":
            coin_display(screen, coins=coins_shown + User_data.coins)
        else:
            coin_display(screen, coins=User_data.coins)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # coin_sound.stop()
                return ['quit']
            if coin_state != "ongoing":
                if event.type == pygame.MOUSEBUTTONDOWN:
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

        initial_coordinates = [WW // 2 - 200, 100]
        screen.fill(theme.background)
        heading_text = big_font.render('Click Ball Leaderboard!', True, theme.font_c)
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
        if len(lboard_data) != 0:
            heading_text = medium_font.render('Name', True, theme.font_c)
            heading_rect = heading_text.get_rect()
            heading_rect.topleft = (WW // 2 - 200, 100)
            screen.blit(heading_text, heading_rect.topleft)

            heading_text = medium_font.render('Score', True, theme.font_c)
            heading_rect = heading_text.get_rect()
            heading_rect.topleft = (WW // 2 + 100, 100)
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

        back_button = theme.button_c["back"]
        rect = back_button.get_rect(center=(10, WH - 50))
        if mouse_rect.colliderect(rect):
            back_button = pygame.transform.smoothscale(theme.button_c["back"], (110, 64))
            rect = back_button.get_rect(center=(60, WH - 50))
        else:
            back_button = pygame.transform.smoothscale(theme.button_c["back"], (100, 60))
            rect = back_button.get_rect(center=(60, WH - 50))
        hover(heading_rect, screen)
        if clicked and mouse_rect.colliderect(rect):
            return ['welcome']
        screen.blit(back_button, rect.topleft)

        if clicked and mouse_rect.colliderect(rect):
            return ['welcome']

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False

        pygame.display.update()


def guide_screen(screen):
    start_time_guide = pygame.time.get_ticks()
    print(start_time_guide)
    theme = Themes.active_theme
    mx, my = pygame.mouse.get_pos()
    clicked = False
    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill(theme.background)
        heading_text = big_font.render('Instructions For The Game!', True, theme.font_c)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, 50)
        screen.blit(heading_text, heading_rect.topleft)
        if not clicked:
            instruction_text = medium_font.render("Instructions!", True, theme.font_c)
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
                    current_text = tiny_font.render(exp_list[l], True, theme.font_c)
                    current_rect = current_text.get_rect()
                    if top_right[0] > WW - 200:
                        top_right[0] = 15
                        top_right[1] += 40

                    current_rect.topleft = (top_right[0] + 10, top_right[1])
                    top_right = list(current_rect.topright)
                    screen.blit(current_text, current_rect.topleft)

        back_button = theme.button_c["back"]
        rect = back_button.get_rect(center=(10, WH - 50))
        if mouse_rect.colliderect(rect):
            back_button = pygame.transform.smoothscale(theme.button_c["back"], (110, 64))
            rect = back_button.get_rect(center=(60, WH - 50))
        else:
            back_button = pygame.transform.smoothscale(theme.button_c["back"], (100, 60))
            rect = back_button.get_rect(center=(60, WH - 50))
        hover(heading_rect, screen)
        if clicked and rect.left < mx < rect.right and rect.top < my < rect.bottom:
            return ['welcome']
        screen.blit(back_button, rect.topleft)

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

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
        back_button = theme.button_c["back"]
        rect = back_button.get_rect(center=(10, WH - 50))
        if rect.left < mx < rect.right and rect.top < my < rect.bottom:
            back_button = pygame.transform.smoothscale(theme.button_c["back"], (110, 64))
            rect = back_button.get_rect(center=(60, WH - 50))
        else:
            back_button = pygame.transform.smoothscale(theme.button_c["back"], (100, 60))
            rect = back_button.get_rect(center=(60, WH - 50))

        if clicked and rect.left < mx < rect.right and rect.top < my < rect.bottom:
            return 'back'
        screen.blit(back_button, rect.topleft)

        counter = 0
        for i in range(1, 6):
            for j in range(1, 6):
                counter += 1

                if counter <= User_data.current_level:
                    temp_img = number_buttons[counter]
                    _rect = temp_img.get_rect()
                    _rect.center = (j * WW / 6, i * WH / 6 + 50)
                    if _rect.left < mx < _rect.right and _rect.top < my < _rect.bottom:
                        temp_img = pygame.transform.smoothscale(temp_img, (70, 70))
                        _rect = temp_img.get_rect(center=(j * WW / 6, i * WH / 6 + 50))
                    else:
                        temp_img = pygame.transform.smoothscale(temp_img, (65, 65))
                        _rect = temp_img.get_rect(center=(j * WW / 6, i * WH / 6 + 50))

                    if _rect.left < mx < _rect.right and _rect.top < my < _rect.bottom:
                        if clicked:
                            return counter
                    screen.blit(temp_img, _rect.topleft)
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

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

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
            theme_button = pygame.transform.scale(theme.button_c["theme"], (195, 61))
            rect = theme_button.get_rect(center=(WW // 2, 250))
        else:
            theme_button = pygame.transform.scale(theme.button_c["theme"], (180, 57))
            rect = theme_button.get_rect(center=(WW // 2, 250))

        screen.blit(theme_button, rect.topleft)

        if clicked and mouse_rect.colliderect(rect):
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
        heading_text = medium_font.render('Change Ball', True, theme.font_c)
        rect = heading_text.get_rect()
        rect.center = (WW // 2, 325)
        # 647, 297, 243, 57

        if mouse_rect.colliderect(rect):
            ball_button = pygame.transform.scale(theme.button_c["ball"], (165, 61))
            rect = ball_button.get_rect(center=(WW // 2, 325))
        else:
            ball_button = pygame.transform.scale(theme.button_c["ball"], (150, 57))
            rect = ball_button.get_rect(center=(WW // 2, 325))

        if clicked and mouse_rect.colliderect(rect):
            return ['ball']

        screen.blit(ball_button, rect.topleft)

        heading_text = medium_font.render('Toggle Fullscreen', True, theme.font_c)
        rect = heading_text.get_rect()
        rect.center = (WW // 2, 400)

        screen.blit(heading_text, rect)
        if mouse_rect.colliderect(rect) and clicked:
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

        # screen.blit(heading_text, rect.topleft)
        # hover(rect, screen)

        back_button = theme.button_c["back"]
        rect = back_button.get_rect(center=(10, WH - 50))
        if mouse_rect.colliderect(rect):
            back_button = pygame.transform.smoothscale(theme.button_c["back"], (110, 64))
            rect = back_button.get_rect(center=(60, WH - 50))
        else:
            back_button = pygame.transform.smoothscale(theme.button_c["back"], (100, 60))
            rect = back_button.get_rect(center=(60, WH - 50))
        hover(heading_rect, screen)
        screen.blit(back_button, rect.topleft)
        if clicked and mouse_rect.colliderect(rect):
            return ['welcome']
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mx, my = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
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
        back_button = theme.button_c["back"]
        rect = back_button.get_rect(center=(10, WH - 50))
        if mouse_rect.colliderect(rect):
            back_button = pygame.transform.smoothscale(theme.button_c["back"], (110, 64))
            rect = back_button.get_rect(center=(60, WH - 50))
        else:
            back_button = pygame.transform.smoothscale(theme.button_c["back"], (100, 60))
            rect = back_button.get_rect(center=(60, WH - 50))
        hover(heading_rect, screen)
        screen.blit(back_button, rect.topleft)
        if clicked and mouse_rect.colliderect(rect):
            return ['settings', skins[skin]]

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
                    clicked = False
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
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False

        pygame.display.update()


def death_screen(screen, status, score):
    theme = Themes.active_theme
    clicked = False
    mx, my = pygame.mouse.get_pos()

    if status == "completed":
        header_text = big_font.render('Well played! You completed the Game', True, theme.font_c)
    else:
        header_text = big_font.render('Better luck next time', True, theme.font_c)
    header_rect = header_text.get_rect()
    header_rect.center = (WW // 2, 50)

    send_data_text = small_font.render('Send Data to Leaderboard', True, theme.font_c)
    send_data_rect = send_data_text.get_rect()
    send_data_rect.center = (WW // 4, 350)

    back_button = theme.button_c["back"]
    # if clicked and mouse_rect.colliderect(rect):
    #     return ['quit']
    # screen.blit(exit_button, rect.topleft)

    while True:
        screen.fill(theme.background)
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
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
        rect = back_button.get_rect(center=(WW // 2 + 400, WH // 2 - 20))
        if mx > rect.left and rect.top < my < rect.bottom:
            back_button = pygame.transform.smoothscale(theme.button_c["back"], (100, 64))
            rect = back_button.get_rect(center=(WW // 2 + 400, WH // 2 - 20))
        else:
            back_button = pygame.transform.smoothscale(theme.button_c["back"], (90, 60))
            rect = back_button.get_rect(center=(WW // 2 + 400, WH // 2 - 20))
        if clicked and mx > rect.left and rect.top < my < rect.bottom:
            return ['welcome']
        screen.blit(back_button, rect.topleft)
        screen.blit(header_text, header_rect)
        screen.blit(send_data_text, send_data_rect)
        if send_data_rect.left < mx < send_data_rect.right and send_data_rect.top < my < send_data_rect.bottom:
            # todo Replace with Button
            if clicked:
                def sending_thread(name, score):
                    send_data_to_leaderboard(name, score)

                threading.Thread(target=sending_thread, args=(User_data.name, score)).start()  # sends Score
                return ['welcome']

        clicked = False
        pygame.display.update()


def name_screen(screen):
    name = ""
    theme = Themes.active_theme
    name_text = big_font.render("Enter your Name", True, theme.font_c)
    name_rect = name_text.get_rect()
    name_rect.center = WW // 2, 50

    running = True
    rect_border_gap = 2
    error = medium_font.render("", True, theme.font_c)
    error_rect = error.get_rect()
    error_rect.center = (WW // 2, 500)
    while running:
        screen.fill(theme.background)
        screen.blit(name_text, name_rect)
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                name += event.unicode

                if event.key == pygame.K_RETURN:
                    if len(name) > 32:
                        error = medium_font.render("Name Too long", True, theme.font_c)
                        error_rect = error.get_rect()
                        error_rect.center = (WW // 2, 500)

                    elif name == "":
                        error = medium_font.render("Empty Name", True, theme.font_c)
                        error_rect = error.get_rect()
                        error_rect.center = (WW // 2, 500)

                    else:
                        while name[-1] == " ":
                            name = name[:-1]
                        DB.save_name(name)
                        running = False

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

        if len(name) >= 1:
            if name[0] == " ":
                name = name[1:]

        screen.blit(error, error_rect.topleft)
        input_name_text = small_font.render(name, True, theme.font_c)
        input_name_rect = input_name_text.get_rect()
        input_name_rect.center = (WW // 2, 400)
        screen.blit(input_name_text, input_name_rect)

        pygame.draw.rect(screen, (255, 0, 0), (input_name_rect.x - rect_border_gap, input_name_rect.y - rect_border_gap,
                                               input_name_rect.width + (rect_border_gap * 2),
                                               input_name_rect.height + (rect_border_gap * 2)), width=2)

        pygame.display.update()


def campaign_continue_screen(screen):
    theme = Themes.active_theme
    clicked = False
    running = True

    heading_text = big_font.render('Congratulations! You passed the Level', True, theme.font_c)
    heading_rect = heading_text.get_rect()
    heading_rect.center = (WW // 2, 50)

    continue_button = theme.button_c["continue"]

    # continue_text = small_font.render('Continue', True, theme.font_c)
    # continue_rect = continue_text.get_rect()
    # continue_rect.center = (WW // 4, WH // 2)

    map_text = small_font.render('Level Map', True, theme.font_c)
    map_rect = map_text.get_rect()
    map_rect.center = (int(WW * 3) // 4, WH // 2)

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
        rect = continue_button.get_rect(center=(WW // 4, WH // 2))
        if rect.left < mx < rect.right and rect.top < my < rect.bottom:
            continue_button = pygame.transform.smoothscale(theme.button_c["continue"], (160, 64))
            rect = continue_button.get_rect(center=(WW // 4, WH // 2))
        else:
            continue_button = pygame.transform.smoothscale(theme.button_c["continue"], (150, 60))
            rect = continue_button.get_rect(center=(WW // 4, WH // 2))
        screen.blit(continue_button, rect.topleft)
        if clicked and rect.left < mx < rect.right and rect.top < my < rect.bottom:
            return ['continue']
        if rect.left < mx < rect.right and rect.top < my < rect.bottom:
            # todo make Hover Effect
            if clicked:
                return ['continue']

        rect = map_rect

        if rect.left < mx < rect.right and rect.top < my < rect.bottom:
            # todo make Hover Effect
            if clicked:
                return ['level_map']

        screen.blit(map_text, map_rect.topleft)

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        pygame.display.update()


def campaign_death_screen(screen):
    theme = Themes.active_theme
    clicked = False

    running = True

    heading_text = big_font.render('Game Over!', True, theme.font_c)
    heading_rect = heading_text.get_rect()
    heading_rect.center = (WW // 2, 50)

    restart_text = small_font.render('Restart', True, theme.font_c)
    restart_rect = restart_text.get_rect()
    restart_rect.center = (WW // 4, WH // 2)

    map_text = small_font.render('Level Map', True, theme.font_c)
    map_rect = map_text.get_rect()
    map_rect.center = (int(WW * 3) // 4, WH // 2)

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

        rect = restart_rect
        screen.blit(restart_text, rect.topleft)
        if rect.left < mx < rect.right and rect.top < my < rect.bottom:
            # todo make Hover Effect
            if clicked:
                return ['restart']

        rect = map_rect

        if rect.left < mx < rect.right and rect.top < my < rect.bottom:
            # todo make Hover Effect
            if clicked:
                return ['level_map']

        screen.blit(map_text, map_rect.topleft)

        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

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
