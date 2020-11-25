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
player = DynamicBall((WW // 2, WH // 2), 10, 0, p_img, space)
flag = VictoryFlag((WW - 100, WH - 100))

## -------------------- Some functions --------------------
def load_level_by_num(name, i):
    return Levels(name, os.path.join(lvl_path_50, f'level{i}.json'))

def remove_lines_of_level_by_number(i, lines):
    '''
    Returns empty list, assign this to the lines list
    '''
    for rl in lines:
        space.remove(rl.body, rl.shape)  # Extremely Necessary
    return []  # Deleting the lines of the prev level

current_level = load_level_by_num('The Beginning', 1)

## ========================= Survival Mode =========================
def survival_mode(screen):
    global current_level
    ## -------------------- Initializing Game --------------------
    score = 0
    st_time = 0  # Time
    death_time = 0  # Death time
    clicked = False

    ## -------------------- Initializing Level --------------------
    player.body.position = current_level.dict["player"][0]      ## Player
    player.body.velocity = (0, 0)                               ## Player
    flag.rect.bottomleft = current_level.dict["victory"][0]     ## Flag
    moves = 5                                                   ## Moves
    ## Lines
    lines = []
    line_number = 0
    for s, e in zip(current_level.dict["start"], current_level.dict["end"]):  # can't use nested cuz it makes wierd things happen xD
        l = StaticLine(s, e, current_level.dict["thickness"][line_number], space)
        lines.append(l)
        line_number += 1
    line_number = 0

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
                    return ['welcome']


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
        for line in lines:
            line.draw(screen, Themes.active_theme.platform_c)


        ## -------------------- Flag --------------------
        flag.draw(screen)
        # Checking collision b/w player and the victory flag
        if player.rect.colliderect(flag.rect):
            # Adding to Score and reset score Variables
            score += 100 + int(float(100 * current_level.dict['moves']/(current_level.dict['moves']-moves)) / float(time.time() - st_time))
            st_time = 0
            death_time = 0
            current_level = load_level_by_num('noname', current_level.number + 1)
            lines = remove_lines_of_level_by_number(current_level, lines)
            return ['welcome']          # @todo make a score screen ;)


        ## -------------------- In-game UI --------------------
        # Displaying the number of moves left
        moves_text = small_font.render('Moves Left: ' + str(moves), True, Themes.active_theme.font_c)
        moves_rect = moves_text.get_rect()
        moves_rect.center = (WW // 2, 50)
        screen.blit(moves_text, moves_rect.topleft)
        # Displaying the level
        level_text = small_font.render(f"level: {current_level.number}", True, Themes.active_theme.font_c)
        screen.blit(level_text, (20, 31))


        ## -------------------- Time and stuff --------------------
        if st_time == 0:
            st_time = time.time()
        if death_time != 0:
            if death_time - int(time.time()) + 10 <= 0:
                restart_game()

            # giving a 10 seconds timer and Auto reset if not colliding with the Flag
            if death_time != 0:
                screen.blit(
                    small_font.render(str(death_time - int(time.time()) + 10), True, Themes.active_theme.font_c),
                    (WW - 50, 31))


        ## -------------------- Updating--------------------
        space.step(2 / FPS)
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
