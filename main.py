import pymunk

from imports import *
import math
import pymunk
import pygame
from imports.game_modes import *


# Main Loop
pygame.mouse.set_visible(False)
while True:

    if to_do[0] == 'welcome':
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
            to_do = ['welcome']
        elif level_num == 'quit':
            to_do = ['quit']
        else:
            to_do = campaign(screen, load_level_by_num('noname', level_num))

    elif to_do[0] == 'themes':
        to_do = theme_screen(screen)

    elif to_do[0] == 'guide':
        to_do = guide_screen(screen)

    elif to_do[0] == 'music':
        to_do = music_screen(screen)

    elif to_do[0] == 'line':
        to_do = line_select_screen(screen)

    elif to_do[0] == 'ball':
        to_do = skin_select_screen(screen, skins)

    elif to_do[0] == 'quit':
        break

pygame.quit()
