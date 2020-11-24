# Importing
import pymunk, pygame, time

from imports import *

## -------- PyMunk Initialization --------
space = pymunk.Space()  # Create a Space which contain the simulation
space.gravity = 0, GRAVITY  # Set its gravity

screen_flags = pygame.SCALED | pygame.RESIZABLE
screen = pygame.display.set_mode((WW, WH), screen_flags)
# Game
pygame.display.set_caption('Click Ball!')
clock = pygame.time.Clock()

## Common To both modes
p_img = skins[0]
max_speed = 100
player = DynamicBall((WW//2, WH//2), 10, 0, p_img, space)
flag = VictoryFlag((WW-100, WH-100))
line = StaticLine((WW//2-100, WH//2+100), (WW//2+100, WH//2+100), 10, space)
level_path = os.path.join('assets', 'levels', '1-50')
level = Levels('AvdaKadavra', os.path.join(level_path, 'level1.json'))

## -------------------- Some functions --------------------
def restart_game():
    pass

def reset_level():
    pass

def survival_mode(screen):
    # Initialization of the game ;)
    score = 0
    st_time = 0  # Time
    level_number_to_display = 1
    death_time = 0 # Death time
    moves = 5
    clicked = False
    while True:
        screen.fill(Themes.active_theme.background)

        ## -------------------- Events --------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.KEYDOWN:
                if moves == 0 and event.key == pygame.K_r:
                    restart_game()

        ## -------------------- Player --------------------
        player.draw(screen)
        # Drawing the direction in which a force will b applied
        mx, my = pygame.mouse.get_pos()
        distx = mx - player.body.position.x
        disty = my - player.body.position.y
        pygame.draw.aaline(screen, Themes.active_theme.mouse_line, player.body.position, (mx, my), 10)
        # Adding a velocity to the ball if it clicked
        if clicked:
            if moves > 0:
                moves -= 1
                player.body.velocity = (distx, disty)
            clicked = False
        # Limiting the player's velocity (so that it doesn't flies across like hell xD)
        if distx > max_speed:
            distx = max_speed
        if disty > max_speed:
            disty = max_speed

        ## -------------------- Lines --------------------
        line.draw(screen, Themes.active_theme.platform_c)

        ## Flag
        flag.draw(screen)
        # Checking collision b/w player and the victory flag
        if player.rect.colliderect(flag.rect):
            # Adding to Score and reset score Variables
            # score += 100 + int(float(100 * current_level['moves']/(current_level['moves']-moves)) / float(time.time() - st_time))
            st_time = 0
            death_time = 0

        ## -------------------- In-game UI --------------------
        # Displaying the number of moves left
        moves_text = small_font.render('Moves Left: ' + str(moves), True, Themes.active_theme.font_c)
        moves_rect = moves_text.get_rect()
        moves_rect.center = (WW // 2, 50)
        screen.blit(moves_text, moves_rect.topleft)
        # Displaying the level
        # level_text = small_font.render(f"level: {level_number_to_display}", True, active_theme.font_c)
        # screen.blit(level_text, (20, 31))

        ## -------------------- Time and stuff --------------------
        if st_time == 0:
            st_time = time.time()
        if death_time!=0:
            if death_time - int(time.time()) + 10 <= 0:
                restart_game()

            # giving a 10 seconds timer and Auto reset if not colliding with the Flag
            if death_time!=0:
                screen.blit(small_font.render(str(death_time - int(time.time()) + 10), True, Themes.active_theme.font_c), (WW-50, 31))

        space.step(2/FPS)
        clock.tick(FPS)
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
        to_do = theme_screen(screen)  # @todo change this to themes Screen later

    elif to_do[0] == 'leaderboard':
        print("under Dev")
        to_do = welcome_screen(screen)  # @todo change this to leaderboard Screen later

    elif to_do[0] == 'ball':
        print("under Dev")
        to_do = welcome_screen(screen)  # @todo change this to ball Screen later

    elif to_do[0] == 'quit':
        break
