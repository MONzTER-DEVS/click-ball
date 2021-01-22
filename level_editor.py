'''
YaY i made it finally
Instructions:
    > Run the file
    > 'S' to print the coordinates (for now atleast)
    > 'M' to change mode (line, flag, player, bouncing ball)
    > If u wanna change these shortcuts, u can tell me or change urself!!
MODES:
    line:
        > Click to place line
        > 'F' to change end of line
        > use 'UP' and "DOWN" arrow keys to increase and decrease the thickness of the selected line
        > 'N' to add a new line and 'D' to delete the current line 
        > 'Enter' to change line 
    flag:
        > Click to place flag
    player:
        > Click to place player
    bouncing ball:
        > 'N' to add a new ball and 'D' to delete the current ball 
        > Click to place ball
        > use 'UP' and "DOWN" arrow keys to increase and decrease the radius of the selected ball
        > 'Enter' to change ball
    portal:
        > 'N' to add a new pair of portals and 'D' to delete the current portal
        > Click to place portal
        > 'F' to change end of portal
        > 'Enter' to change portal
    coin:
        > 'N' to add a new coin and 'D' to delete the current coin
        > 'Enter' to change coin
        > Click to place coin
EDIT : U can now select the end or individual objects using ur mouse ;)

'''

from imports.settings import WW, WH, small_font, medium_font, big_font
from imports.classes import Themes
from imports.classes import Levels
import pygame, math, json, os

if not os.path.exists(os.path.join('assets', 'level_editor_saves')):
    os.mkdir('assets/level_editor_saves')

n = int(input("Which level do you want to edit(Press 0 to create a new level):"))

pygame.init()

level_dict = Levels.levels[n - 1].dict
# print(level_dict)

screen_flags = pygame.SCALED | pygame.RESIZABLE
screen = pygame.display.set_mode((WW, WH), screen_flags)

GRID_SIZE = 20
GRID_COLOR = (100, 100, 100)

DRAG_OFFSET = 150

SELECTED_LINE_COLOR = (255, 255, 50)
LINE_COLOR = (100, 255, 255)

SELECTED_BALL_COLOR = (255, 255, 50)
BALL_COLOR = (100, 255, 255)

mouse_rect = pygame.Rect(0, 0, 10, 10)
select_rect = pygame.Rect(0, 0, 0, 0)
select_rect_color = Themes.active_theme.hover

obj_rect = pygame.Rect(0, 0, 0, 0)


def hover(obj_rect, Screen):
    mouse_rect.center = pygame.mouse.get_pos()
    if mouse_rect.colliderect(obj_rect):
        select_rect.topleft = obj_rect.topleft
        select_rect.size = obj_rect.size

        ## Not using pygame.draw.rect cuz usme opacity set nhi hoti
        s_img = pygame.Surface(select_rect.size)
        s_img.set_alpha(50)
        s_img.fill(select_rect_color)
        Screen.blit(s_img, select_rect.topleft)


class Line:
    def __init__(self, x1, y1, x2, y2, width):
        self.start_pos = (x1, y1)
        self.end_pos = (x2, y2)
        self.width = width
        self.color = LINE_COLOR

    def draw(self):
        pygame.draw.line(screen, self.color, self.start_pos, self.end_pos, self.width)


class Flag:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/imgs/victory_flag.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect.topleft)


class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/imgs/skins_png/01.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect.topleft)


class BouncingBall:
    def __init__(self, x, y, r, color):
        self.center = (x, y)
        self.radius = r
        self.color = color
        self.rect = pygame.Rect(
            self.center[0] - self.radius,
            self.center[1] - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def draw(self):
        self.rect.center = self.center
        self.rect.size = (self.radius * 2, self.radius * 2)
        pygame.draw.circle(screen, self.color, self.center, self.radius)


class Portal:
    def __init__(self, start_pos, end_pos, r):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.start_img = pygame.image.load('assets/imgs/PortalStart.png')
        self.end_img = pygame.image.load('assets/imgs/PortalEnd.png')
        self.start_rect = self.start_img.get_rect()
        self.end_rect = self.end_img.get_rect()

    def draw(self):
        self.start_rect.center = self.start_pos
        self.end_rect.center = self.end_pos
        pygame.draw.line(screen, (0, 0, 0), self.start_pos, self.end_pos)
        screen.blit(self.start_img, self.start_rect.topleft)
        screen.blit(self.end_img, self.end_rect.topleft)


class Coin:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/imgs/dollar.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect.topleft)


# flag = Flag(WW//2, WH//2)
# player = Player(WW//2, WH//2)
if n != 0:
    flag = Flag(level_dict["victory"][0][0], level_dict["victory"][0][1])
    player = Player(level_dict["player"][0][0], level_dict["player"][0][1])
    num_of_lines = len(level_dict["start"])
    lines = []
    for i in range(num_of_lines):
        # l = Line(WW // 2, WH // 2, WW // 2, WH // 2, 10)
        l = Line(level_dict["start"][i][0],
                 level_dict["start"][i][1],
                 level_dict["end"][i][0],
                 level_dict["end"][i][1], 10)
        lines.append(l)

    selected_line_index = 0

    selected_line = lines[selected_line_index]
    selected_line_end = 'start'
    if len(level_dict['portal_start']):
        num_of_portals = len(level_dict["portal_start"])
    else:
        num_of_portals = 0
    portals = []
    if level_dict["portal_start"]:
        for i in range(num_of_portals):
            # p = Portal((WW // 2, 100), (WW // 2, WH - 100), 10)
            p = Portal(level_dict["portal_start"][i],
                       level_dict["portal_end"][i], 10)
            portals.append(p)

    selected_portal_index = 0
    selected_portal_end = 'start'
    try:
        selected_portal = portals[selected_portal_index]
    except IndexError:
        pass
    if level_dict["ball_radius"]:
        num_of_balls = len(level_dict["ball_radius"])
    else:
        num_of_balls = 0
    balls = []

    for i in range(num_of_balls):
        # b = BouncingBall(WW // 2, WH // 2, 10, BALL_COLOR)
        b = BouncingBall(level_dict["ball_center"][i][0],
                         level_dict["ball_center"][i][1], 10, BALL_COLOR)
        balls.append(b)
        selected_ball_index = 0
        selected_ball = balls[selected_ball_index]
    if level_dict["coin_pos"]:
        num_of_coins = len(level_dict["coin_pos"])
    else:
        num_of_coins = 0
    coins = []
    if level_dict["coin_pos"]:
        for i in range(num_of_coins):
            c = Coin(level_dict["coin_pos"][i][0], level_dict["coin_pos"][i][1])
            coins.append(c)
    if level_dict["coin_pos"]:
        selected_coin_index = 0
        selected_coin = coins[selected_coin_index]
elif n == 0:
    flag = Flag(WW // 2, WH // 2)
    player = Player(WW // 2, WH // 2)
    num_of_balls = 1
    balls = []
    for i in range(num_of_balls):
        b = BouncingBall(WW // 2, WH // 2, 10, BALL_COLOR)
        balls.append(b)

    selected_ball_index = 0
    selected_ball = balls[selected_ball_index]

    ## lines
    num_of_lines = 1
    lines = []
    for i in range(num_of_lines):
        l = Line(WW // 2, WH // 2, WW // 2, WH // 2, 10)
        lines.append(l)

    selected_line_index = 0
    selected_line = lines[selected_line_index]
    selected_line_end = 'start'

    ## portals
    num_of_portals = 0
    portals = []
    for i in range(num_of_portals):
        p = Portal((WW // 2, 100), (WW // 2, WH - 100), 10)
        portals.append(p)

    selected_portal_index = 0
    selected_portal_end = 'start'
    try:
        selected_portal = portals[selected_portal_index]
    except IndexError:
        pass
    num_of_coins = 1
    coins = []
    for i in range(num_of_coins):
        c = Coin(WW // 2, WH // 2)
        coins.append(c)
    selected_coin_index = 0
    selected_coin = coins[selected_coin_index]

## balls


running = True
clicked = False

#
# def change_line_color(lines, selected_line_index, original_color, new_color):
#     for line in lines:
#         if lines[lines.index(line)] == lines[selected_line_index]:
#             lines[lines.index(line)].color =

# def change_color(list, selected_object_index, original_color, new_color):


def save():
    ## saving data
    start_positions = []
    end_positions = []
    widths = []
    ball_positions = []
    ball_radius = []
    portal_start_positions = []
    portal_end_positions = []
    coin_positions = []
    ## Lines
    for line in lines:
        start_positions.append(line.start_pos)
        end_positions.append(line.end_pos)
        widths.append(line.width)
    ## Flag
    victory_position = [flag.rect.bottomleft]
    ## Player
    player_position = [player.rect.center]
    ## Balls
    for ball in balls:
        ball_positions.append(ball.center)
        ball_radius.append(ball.radius)
    ## Portals
    for portal in portals:
        portal_start_positions.append(portal.start_pos)
        portal_end_positions.append(portal.end_pos)
    for coin in coins:
        coin_positions.append(coin.rect.center)

    to_dump_dict = {
        'start': start_positions,
        'end': end_positions,
        'thickness': widths,
        'moves': 5,
        'victory': victory_position,
        'player': player_position,
        'ball_center': ball_positions,
        'ball_radius': ball_radius,
        'portal_start': portal_start_positions,
        'portal_end': portal_end_positions,
        'coin_pos': coin_positions,
        'portal_thickness': ["med" for _ in range(len(portal_end_positions))]
    }

    f_name = str(len(os.listdir(os.path.join('assets', 'level_editor_saves'))))
    f_path = os.path.join('assets', 'level_editor_saves', f_name + '.json')

    with open(os.path.join('assets', 'level_editor_saves', f_name + '.json'), "w") as f:
        json.dump(to_dump_dict, f, indent=4)
    print('saved at', f_path)


## line / flag / player / portal
modes = ['line', 'flag', 'player', 'bouncing ball', 'portal', 'coin']
mode_index = 0
mode = modes[mode_index]
while running:

    # Snapping to the grid
    mx, my = pygame.mouse.get_pos()
    real_mx, real_my = pygame.mouse.get_pos()
    mx = round(mx / GRID_SIZE) * GRID_SIZE
    my = round(my / GRID_SIZE) * GRID_SIZE
    mouse_rect.center = pygame.mouse.get_pos()

    screen.fill(Themes.active_theme.background)

    ## Events
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        ## Clicking
        if e.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        elif e.type == pygame.MOUSEBUTTONUP:
            clicked = False

        ## Shortcuts (maybe will b removed in the future)
        if e.type == pygame.KEYDOWN:
            ## Will Run ALWAYS
            if e.key == pygame.K_m:
                mode_index += 1

            ## To save press S
            if e.key == pygame.K_s:
                save()

            ## Will only run if mode is coin
            if mode == 'coin':
                if e.key == pygame.K_RETURN:
                    selected_coin_index += 1
                if e.key == pygame.K_n:
                    c = Coin(WW // 2, WH // 2)
                    coins.append(c)
                    selected_coin_index = coins.index(c)
                    selected_coin = coins[selected_coin_index]
                if e.key == pygame.K_d:
                    coins.remove(selected_coin)

            ## Will only run if mode is line
            if mode == 'line':
                ## iterating thru lines
                if e.key == pygame.K_RETURN:
                    selected_line_index += 1

                    # lines[selected_line_index].color = SELECTED_LINE_COLOR
                    # for line in lines:
                    #     if lines.index(line) == selected_line_index:
                    #         lines[selected_line_index].color = SELECTED_LINE_COLOR
                    #     else:
                    #         lines[line].color = LINE_COLOR
                ## iterating thru line ends
                if e.key == pygame.K_f:
                    if selected_line_end == 'start':
                        selected_line_end = 'end'
                    elif selected_line_end == 'end':
                        selected_line_end = 'start'

                ## adding a new line
                if e.key == pygame.K_n:
                    l = Line(WW // 2, WH // 2, WW // 2, WH // 2, 10)
                    lines.append(l)
                    selected_line_index = lines.index(l)

                    ## deleting the current line
                if e.key == pygame.K_d:
                    lines.remove(selected_line)

                ## To increase width, press up arrow
                if e.key == pygame.K_UP:
                    selected_line.width += 5

                ## To decrease width, press down arrow
                if e.key == pygame.K_DOWN:
                    selected_line.width -= 5

            ## Will only run if mode is bouncing ball
            if mode == 'bouncing ball':
                ## adding a new ball
                if e.key == pygame.K_n:
                    b = BouncingBall(WW // 2, WH // 2, 10, BALL_COLOR)
                    balls.append(b)
                    selected_ball = balls[-1]

                ## deleting the current ball
                if e.key == pygame.K_d:
                    balls.remove(selected_ball)

                ## To increase radius, press up arrow
                if e.key == pygame.K_UP:
                    selected_ball.radius += 5

                ## To decrease radius, press down arrow
                if e.key == pygame.K_DOWN:
                    selected_ball.radius -= 5

            ## Will only run if mode is portal
            if mode == 'portal':
                ## iterating thru portals
                if e.key == pygame.K_RETURN:
                    selected_portal_index += 1

                ## iterating thru portal ends
                if e.key == pygame.K_f:
                    if selected_portal_end == 'start':
                        selected_portal_end = 'end'
                    elif selected_portal_end == 'end':
                        selected_portal_end = 'start'

                ## adding a new portal
                if e.key == pygame.K_n:
                    p = Portal((WW // 2, 100), (WW // 2, WH - 100), 10)
                    portals.append(p)
                    selected_portal_index = portals.index(p)

                    ## deleting the current portal
                if e.key == pygame.K_d:
                    portals.remove(selected_portal)

    ## GUI STUFF
    # mode indicator
    mode_text = small_font.render("Mode: " + mode, True, Themes.active_theme.font_c)
    mode_rect = mode_text.get_rect()
    mode_rect.center = (WW // 2, 50)
    screen.blit(mode_text, mode_rect.topleft)

    # Next mode
    heading_text = small_font.render(' -> ', True, Themes.active_theme.font_c)
    heading_rect = heading_text.get_rect()
    heading_rect.center = (WW // 2 + 175, 50)
    screen.blit(heading_text, heading_rect.topleft)

    hover(heading_rect, screen)
    if clicked:
        if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
            mode_index += 1
            clicked = False

    # Previous mode
    heading_text = small_font.render(' <- ', True, Themes.active_theme.font_c)
    heading_rect = heading_text.get_rect()
    heading_rect.center = (WW // 2 - 175, 50)
    screen.blit(heading_text, heading_rect.topleft)

    hover(heading_rect, screen)
    if clicked:
        if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
            mode_index -= 1
            clicked = False

    ## Drawing the grid
    for x in range(0, WW, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WH))
    for y in range(0, WH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WW, y))

    ## Defining the selected line
    try:
        selected_line = lines[selected_line_index]
    except IndexError:
        selected_line_index = 0

    ## Defining the selected portal
    try:
        selected_portal = portals[selected_portal_index]
    except IndexError:
        selected_portal_index = 0

    ## Defining the selected coin
    if level_dict["coin_pos"]:
        try:
            selected_coin = coins[selected_coin_index]
        except IndexError:
            selected_coin_index = 0
    ## Defining mode
    try:
        mode = modes[mode_index]  ## Managing modes
    except IndexError:
        mode_index = 0

    ## Drawing coins
    for coin in coins:
        coin.draw()
        if clicked and mode == "coin":
            obj_rect = coin.rect.copy()
            dist = math.sqrt(
                (coin.rect.centerx - mouse_rect.centerx) ** 2 +
                (coin.rect.centery - mouse_rect.centery) ** 2
            )
            if dist < DRAG_OFFSET:
                coin.rect.center = (mx, my)

    ## Drawing lines
    for line in lines:
    #     # print(lines[selected_line_index])
    #     # if selected_line_index == 1:
    #     #     for line in lines:
    #     if lines[lines.index(line)] == lines[selected_line_index]:
    #         lines[lines.index(line)].color = SELECTED_LINE_COLOR
    #     else:
    #         lines[lines.index(line)].color = LINE_COLOR
        line.draw()
            # for line in lines:
        # print(lines.index(line))
        # selected_line_index = 1
        # if selected_line_index == 1:
        #     lines[selected_line_index].color = (0, 0, 0)
        # else:
        #     lines[selected_line_index].color = LINE_COLOR

        ## Selecting line
        # if mouse_rect.centerx in range(line.start_pos[0], line.end_pos[0] + 1):
        #     if mouse_rect.centery in range(line.start_pos[1], line.end_pos[1] + 1):
        #         # if clicked and mode == 'line':
        #         selected_line = line
        # dist_from_start = math.sqrt(
        #     (line.start_pos[0] - mouse_rect.centerx)**2 + 
        #     (line.start_pos[1] - mouse_rect.centery)**2
        # )
        # dist_from_end = math.sqrt(
        #     (line.end_pos[0] - mouse_rect.centerx)**2 + 
        #     (line.end_pos[1] - mouse_rect.centery)**2
        # )

        ## Selected line
        if mode == 'line':
            if lines[lines.index(line)] == lines[selected_line_index]:
                lines[lines.index(line)].color = SELECTED_LINE_COLOR
            else:
                lines[lines.index(line)].color = LINE_COLOR
        if line == selected_line and mode == 'line':
                # print(lines[selected_line_index])
                # if selected_line_index == 1:
                #     for line in lines:

                # line.draw()
            # obj_rect = line.rect.copy()
            if clicked and mode == 'line':
                dist = math.sqrt(
                    (line.start_pos[0] - mouse_rect.centerx) ** 2 +
                    (line.start_pos[1] - mouse_rect.centery) ** 2
                )
                if dist < DRAG_OFFSET:
                    selected_line_end = 'start'

                dist = math.sqrt(
                    (line.end_pos[0] - mouse_rect.centerx) ** 2 +
                    (line.end_pos[1] - mouse_rect.centery) ** 2
                )
                if dist < DRAG_OFFSET:
                    selected_line_end = 'end'

                if selected_line_end == 'start':
                    line.start_pos = (mx, my)
                if selected_line_end == 'end':
                    line.end_pos = (mx, my)

    ## Drawing balls
    for ball in balls:
        ball.draw()
        # Selecting ball
        dist = math.sqrt(
            (ball.center[0] - mouse_rect.centerx) ** 2 +
            (ball.center[1] - mouse_rect.centery) ** 2
        )
        if dist < DRAG_OFFSET:
            selected_ball = ball

        # Selected ball
        if mode == 'bouncing ball':
            if balls[balls.index(ball)] == balls[selected_ball_index]:
                balls[balls.index(ball)].color = SELECTED_BALL_COLOR
            else:
                balls[balls.index(ball)].color = BALL_COLOR
        if ball == selected_ball and mode == 'bouncing ball':
            obj_rect = ball.rect.copy()
            if clicked and mode == 'bouncing ball':
                if dist < DRAG_OFFSET:
                    ball.center = (mx, my)

    ## Drawing portals
    for portal in portals:
        portal.draw()
        if portal == selected_portal and mode == 'portal':
            dist = math.sqrt(
                (portal.start_pos[0] - mouse_rect.centerx) ** 2 +
                (portal.start_pos[1] - mouse_rect.centery) ** 2
            )
            if dist < DRAG_OFFSET:
                selected_portal_end = 'start'
                obj_rect = portal.start_rect.copy()

            dist = math.sqrt(
                (portal.end_pos[0] - mouse_rect.centerx) ** 2 +
                (portal.end_pos[1] - mouse_rect.centery) ** 2
            )
            if dist < DRAG_OFFSET:
                selected_portal_end = 'end'
                obj_rect = portal.end_rect.copy()

            if clicked and mode == 'portal':
                if selected_portal_end == 'start':
                    portal.start_pos = (mx, my)
                if selected_portal_end == 'end':
                    portal.end_pos = (mx, my)

    ## Drawing flag
    if clicked and mode == 'flag':
        obj_rect = flag.rect.copy()
        dist = math.sqrt(
            (flag.rect.centerx - mouse_rect.centerx) ** 2 +
            (flag.rect.centery - mouse_rect.centery) ** 2
        )
        if dist < DRAG_OFFSET:
            flag.rect.center = (mx, my)
    flag.draw()

    ## Drawing player
    if clicked and mode == 'player':
        obj_rect = player.rect.copy()
        dist = math.sqrt(
            (player.rect.centerx - mouse_rect.centerx) ** 2 +
            (player.rect.centery - mouse_rect.centery) ** 2
        )
        if dist < DRAG_OFFSET:
            player.rect.center = (mx, my)
    player.draw()

    # Obj selection rect
    pygame.draw.rect(screen, (200, 200, 200), obj_rect, 3)

    pygame.display.update()

save()

pygame.quit()
