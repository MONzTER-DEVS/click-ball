import pymunk

from imports import *
import math
import pymunk
import pygame
from imports.game_modes import *


def tutorial_screen(screen):
    running = True

    # create level object
    with open("assets/tutorial/level.json", "r") as f:
        level_obj = Levels('Tutorial', json.load(f), to_append_to_levels=False, level_number="Tutorial")

    # loading data from level obj
    level_data = load_objects(level_obj, 'campaign')
    moves = level_data["moves"]
    lines = level_data["lines"]
    balls = level_data["balls"]
    portals = level_data["portals"]
    coins = level_data["coins"]

    def tut_content():
        content = [
            ["option", "Do you want to skip the tutorial?"]
        ]

        for x in content:
            yield x

    content = tut_content()
    content.__iter__()
    current_content = content.__next__()

    mz_face = pygame.image.load("assets/tutorial/monzter-face.png")
    mz_face = pygame.transform.scale(mz_face, (220, 220))  # load mz boi image

    mz_face_rect = mz_face.get_rect()
    mz_face_rect.topleft = (WW, 200)

    s = pygame.Surface(screen.get_size())

    max_alpha = 30
    alpha = 0
    d_alpha = 1
    s.set_alpha(alpha)  # alpha level
    s.fill((64, 64, 64))

    text_alpha = 0
    max_text_alpha = 100
    d_text_alpha = 2

    clock = pygame.time.Clock()
    yes_button = small_font.render("Skip", True, (0, 0, 0))
    yes_button_alpha = 0
    yes_button.set_alpha(yes_button_alpha)
    yes_button_rect = yes_button.get_rect()
    yes_button_rect.topleft = (100, 400)

    while running:
        clock.tick(FPS)
        screen.fill(WHITE)
        mx, my = pygame.mouse.get_pos()
        mouse_rect = pygame.rect.Rect(mx, my, 1, 1)
        clicked = False

        screen.blit(s, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        if current_content[0] == "option" or current_content[0] == "text":
            yes_rect_collided = mouse_rect.colliderect(yes_button_rect)
            # no_rect_collided = mouse_rect.colliderect(yes_button_rect)

            if alpha < max_alpha:
                alpha += d_alpha
                s.set_alpha(alpha)

            elif mz_face_rect.x > WW - 360:
                mz_face_rect.x -= 2

            elif text_alpha <= max_text_alpha:
                text_alpha += d_text_alpha

            else:
                if yes_rect_collided:
                    if yes_button_alpha <= 100:
                        yes_button_alpha += 2
                    yes_button.set_alpha(yes_button_alpha)

                    if clicked:
                        return "Finished"
                else:
                    if yes_button_alpha > 60:
                        yes_button_alpha -= 2

                    if yes_button_alpha < 60:
                        yes_button_alpha += 2

                    yes_button.set_alpha(yes_button_alpha)

            screen.blit(s, (0, 0))

            text_surface = medium_font.render(current_content[1], True, (0, 0, 0))
            text_surface.set_alpha(text_alpha)
            screen.blit(text_surface, (100, 200))

            if mz_face_rect.x < WW:
                new_img = pygame.transform.rotate(mz_face, WW - mz_face_rect.x)
                img_rect = new_img.get_rect(center=mz_face_rect.center)

                screen.blit(new_img, img_rect.topleft)

            screen.blit(yes_button, yes_button_rect)

        else:
            draw_objects(moves, clicked, 0, level_obj, lines, balls, portals, coins, 0)

        # screen.blit(mz_face, (200, 200))
        pygame.display.update()


for error in errors:
    if error == "no name":
        temp_to_do = name_screen(screen)
        if temp_to_do == 'quit':
            to_do[0] = 'quit'
        else:
            User_data.name = DB.fetch_name()

    if error == 'tutorial':
        temp_to_do = tutorial_screen(screen)
        if temp_to_do == 'quit':
            to_do[0] = 'quit'

        elif temp_to_do == "finished":
            to_do[0] = "welcome"
            DB.execute("UPDATE tutorial SET data = 'True'")

    if to_do[0] == "quit":
        break
# Main Loop
pygame.mouse.set_visible(False)
while True:
    if to_do[0] == 'game':
        to_do = game_select_screen(screen)

    elif to_do[0] == 'welcome':
        to_do = welcome_screen(screen)

    elif to_do[0] == 'survival':
        to_do = survival_mode(screen, load_level_by_num('noname', 1))

    elif to_do[0] == 'settings':
        to_do = settings_screen(screen)

    elif to_do[0] == 'campaign':
        if to_do[1] == 'continue':
            level_num = to_do[2]
        else:
            level_num = level_select_screen(screen, number_buttons)

        if level_num == 'back':
            to_do = ['game']
        elif level_num == 'quit':
            to_do = ['quit']
        else:
            to_do = campaign(screen, load_level_by_num('noname', level_num))

    elif to_do[0] == 'themes':
        to_do = theme_screen(screen)

    elif to_do[0] == 'leaderboard':
        to_do = leaderboard_screen(screen)

    elif to_do[0] == 'guide':
        to_do = guide_screen(screen)
    elif to_do[0] == 'music':
        to_do = music_screen(screen)

    elif to_do[0] == 'death':
        to_do = death_screen(screen, to_do[1], to_do[2])
    elif to_do[0] == 'line':
        to_do = line_select_screen(screen)
    elif to_do[0] == 'ball':
        to_do = skin_select_screen(screen, skins)
    elif to_do[0] == 'quit':
        break

pygame.quit()
