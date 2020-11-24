# Importing
import pymunk, pygame

from imports import *

## -------- PyMunk Initialization --------
space = pymunk.Space()  # Create a Space which contain the simulation
space.gravity = 0, GRAVITY  # Set its gravity

screen_flags = pygame.SCALED | pygame.RESIZABLE
screen = pygame.display.set_mode((WW, WH), screen_flags)
# Game
pygame.display.set_caption('Click Ball!')
clock = pygame.time.Clock()


def survival_mode(screen):
    while True:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']

        heading_text = big_font.render('Game Screen!', True, (0, 0, 0))
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW / 2, 50)
        screen.blit(heading_text, heading_rect.topleft)

        pygame.display.update()


to_do = welcome_screen(screen)

# Main Loop
while True:
    if to_do[0] == 'game':
        to_do = game_select_screen(screen)

    elif to_do[0] == 'welcome':
        to_do = welcome_screen(screen)

    elif to_do[0] == 'survival':
        to_do = survival_mode(screen)

    elif to_do[0] == 'campaign':
        print("under Dev")
        to_do = game_select_screen(screen)  # @todo Make a Real Campaign mode


    elif to_do[0] == 'themes':
        print("under Dev")
        to_do = welcome_screen(screen)  # @todo change this to themes Screen later

    elif to_do[0] == 'leaderboard':
        print("under Dev")
        to_do = welcome_screen(screen)  # @todo change this to leaderboard Screen later

    elif to_do[0] == 'ball':
        print("under Dev")
        to_do = welcome_screen(screen)  # @todo change this to ball Screen later

    elif to_do[0] == 'quit':
        break
