from imports import *
import math

## -------- PyMunk Initialization --------
space = pymunk.Space()  # Create a Space which contain the simulation
space.gravity = 0, GRAVITY  # Set its gravity

# Game
pygame.display.set_caption('Click Ball!')
clock = pygame.time.Clock()

## Common To both modes
p_img = skins[0]
player_speed_factor = 1.2  ## Experimental value
max_speed = 100
player = DynamicBall((WW // 2, WH // 2), 10, 0, p_img, space)
flag = VictoryFlag((WW - 100, WH - 100))


## -------------------- Some functions --------------------
def load_level_by_num(name, i, is_survival=False):
    if not is_survival:
        try:
            return Levels.levels[i - 1]
        except IndexError:
            return Levels.levels[0]
    elif is_survival:
        try:
            return Levels.levels[i - 1]
        except IndexError:
            return "finish"


def remove_lines_and_balls_of_level_by_number(i, lines, balls):
    '''
    Returns empty list, assign this to the lines and balls list
    '''
    for rl in lines:
        space.remove(rl.body, rl.shape)  # Extremely Necessary
    for rb in balls:
        space.remove(rb.body, rb.shape)  # Extremely Necessary
    return []  # Deleting the lines of the prev level


def reset_player_pos(player, WW, WH, current_level):
    if player.body.position[0] > WW or player.body.position[0] < 0:
        player.body.position = current_level.dict["player"][0]  ## Player
        player.body.velocity = (0, 0)
    if player.body.position[1] > WH:
        player.body.position = current_level.dict["player"][0]  ## Player
        player.body.velocity = (0, 0)


def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=20):
    def range_(start_, end_, diff):

        to_return = []
        # times = (start_ - end_) / diff
        #
        # if start_ > end_:
        #     sum_ = start_
        # else:
        #     sum_ = end_
        #
        # for x in range(abs(math.ceil(times))):
        #     if times > 0:
        #         to_return.append(sum_)
        #         sum_ += diff
        #     else:
        #         to_return.append(sum_)
        #         sum_ += diff

        if diff > 0:
            positive = True
        else:
            positive = False

        if not positive:
            while start_ - end_ > 0:
                # end_ -= diff
                # to_return.append(end_)
                start_ += diff
                to_return.append(start_)
        else:
            while end_ - start_ > 0:
                # end_ -= diff
                # to_return.append(end_)
                start_ += diff
                to_return.append(start_)

        return to_return

    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)

    if (x1 == x2):
        ycoords = [int(y) for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif (y1 == y2):
        xcoords = [int(x) for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a ** 2 + b ** 2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in range_(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in range_(y1, y2, dy if y1 < y2 else -dy)]
        # xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
        # ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]
        # print(xcoords)
        # print(ycoords)
        # print()

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    # print(next_coords)
    # print(last_coords)
    # print()
    # print()
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        # print(x1, y1)
        # print(x2, y2)
        # print()
        # print()
        # print()
        rx1, ry1 = round(x1), round(y1)
        rx2, ry2 = round(x2), round(y2)
        start = (rx1, ry1)
        end = (rx2, ry2)
        shading = 5
        start2 = (rx1 + shading, ry1 + shading)
        end2 = (rx2 + shading, ry2 + shading)
        if User_data.line == 'new':
            pygame.draw.line(surf, GRAY, start2, end2, width)
            pygame.draw.line(surf, color, start, end, width)
        if User_data.line == 'old':
            pygame.draw.line(surf, BLUE, start_pos, end_pos, 2)


def load_objects(level, mode='survival'):
    ## -------------------- Initializing Level --------------------
    player.image = p_img  ## Player
    player.body.position = level.dict["player"][0]  ## Player
    player.body.velocity = (0, 0)  ## Player
    flag.rect.bottomleft = level.dict["victory"][0]  ## Flag
    moves = level.dict["moves"]  ## Moves
    ## Lines
    lines = []
    line_number = 0
    for s, e in zip(level.dict["start"],
                    level.dict["end"]):  # can't use nested cuz it makes wierd things happen xD
        l = StaticLine(s, e, level.dict["thickness"][line_number], space)
        lines.append(l)
        line_number += 1
    line_number = 0
    ## Dummy Balls
    balls = []
    try:  ## Incase there are no balls ;)
        for p, r in zip(level.dict["ball_center"],
                        level.dict["ball_radius"]):  # can't use nested cuz it makes wierd things happen xD
            b = DynamicBallWithColor(p, 0, 0, r, space)
            balls.append(b)
    except KeyError:
        pass
    ## Portals
    portals = []
    try:
        for s, e in zip(level.dict["portal_start"],
                        level.dict["portal_end"]):  # can't use nested cuz it makes wierd things happen xD
            p = Portal(s, e, 32)
            portals.append(p)
    except KeyError:
        pass
    ## Coins
    coins = []
    if mode != 'survival':
        try:
            # print(level)
            for p in level.dict["coin_pos"]:
                c = Coins(p)
                coins.append(c)
        except KeyError:
            pass
    level_data = {
        "moves": moves,
        "lines": lines,
        "balls": balls,
        "portals": portals,
        "coins": coins
    }
    return level_data


def draw_objects(moves, clicked, coins_collected_in_current_level, level, lines, balls, portals, coins, death_time):
    ## -------------------- Player --------------------
    # Drawing the direction in which a force will b applied
    mx, my = pygame.mouse.get_pos()
    distx = mx - player.body.position.x
    disty = my - player.body.position.y
    draw_dashed_line(screen, Themes.active_theme.mouse_line, player.body.position, (mx, my), 10)
    pygame.draw.circle(screen, Themes.active_theme.mouse_line, (mx, my), 5)

    # Adding a velocity to the ball if it clicked
    if clicked:
        if moves > 0:
            moves -= 1
            player.body.velocity = (distx * player_speed_factor, disty * player_speed_factor)

        if moves == 0 and death_time == 0:  # Start Death timer if not already running
            death_time = int(time.time())
        clicked = False

    # Limiting the player's velocity (so that it doesn't flies across like hell xD)
    if distx > max_speed:
        distx = max_speed
    if disty > max_speed:
        disty = max_speed

    # reseting player's
    reset_player_pos(player, WW, WH, level)

    ## -------------------- Lines, balls and Portals --------------------
    for line in lines:
        line.draw(screen, Themes.active_theme.platform_c)
    for ball in balls:
        ball.draw(screen, Themes.active_theme.bouncing_ball_c)
    for portal in portals:
        portal.draw(screen, space)
        portal.teleport(player)
        for ball in balls:
            portal.teleport(ball)

    ## -------------------- Flag --------------------
    flag.draw(screen)
    player.draw(screen)

    ## -------------------- Events --------------------
    if moves == 0:
        heading_text = medium_font.render("PRESS 'R' TO quit", True, Themes.active_theme.font_c)
        heading_text.set_alpha(200)
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW // 2, WH // 2)
        screen.blit(heading_text, heading_rect.topleft)

    ## -------------------- Coins --------------------
    for coin in coins:
        if coin.collect(player.rect) == 10:
            coins.remove(coin)
            coins_collected_in_current_level += 10
            # coin_collect_sound.play()
        else:
            coin.draw(screen)

    ## -------------------- In-game UI --------------------
    # Displaying the number of moves left
    moves_text = small_font.render('Moves Left: ' + str(moves), True, Themes.active_theme.font_c)
    moves_rect = moves_text.get_rect()
    moves_rect.center = (WW // 2, 50)
    screen.blit(moves_text, moves_rect.topleft)
    # Displaying the level
    level_text = small_font.render(f"level: {level.number}", True, Themes.active_theme.font_c)
    screen.blit(level_text, (20, 31))

    return [moves, clicked, coins_collected_in_current_level]


## ========================= Survival Mode =========================
def survival_mode(screen, current_level):
    score = 0
    if User_data.save is not None:
        data = User_data.get_save()
        score = data['score']
        current_level = load_level_by_num('', int(data['level']))
    ## -------------------- Initializing Game --------------------
    st_time = 0  # Time
    death_time = 0  # Death time
    clicked = False
    coin_collect_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'coin_appear.wav'))

    level_data = load_objects(current_level, 'survival')
    moves = level_data["moves"]
    lines = level_data["lines"]
    balls = level_data["balls"]
    portals = level_data["portals"]
    coins = level_data["coins"]
    coins_collected_in_current_level = 0

    ## ---------------------------------------- MAIN LOOP ----------------------------------------
    while True:
        screen.fill(Themes.active_theme.background)
        ## -------------------- Time and stuff --------------------
        if st_time == 0:
            # load level
            lines = balls = remove_lines_and_balls_of_level_by_number(current_level.number, lines, balls)
            level_data = load_objects(current_level, 'survival')
            moves = level_data["moves"]
            lines = level_data["lines"]
            balls = level_data["balls"]
            portals = level_data["portals"]
            coins = level_data["coins"]
            coins_collected_in_current_level = 0
            coins_collected_in_current_level = 0

            st_time = time.time()
        if death_time != 0:
            if death_time - int(time.time()) + 10 <= 0:
                lines = balls = remove_lines_and_balls_of_level_by_number(current_level.number, lines, balls)
                return ['death', 'dead', score]

            # giving a 10 seconds timer and Auto reset if not colliding with the Flag
            if death_time != 0:
                screen.blit(
                    small_font.render(str(death_time - int(time.time()) + 10), True, Themes.active_theme.font_c),
                    (WW - 50, 31))

        ## -------------------- Events --------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.KEYDOWN:
                if moves == 0 and event.key == pygame.K_r:
                    lines = balls = remove_lines_and_balls_of_level_by_number(current_level.number, lines, balls)
                    current_level = load_level_by_num('noname', 1)
                    player.body.angular_velocity = 0
                    return ['death', 'dead', score]

        ## Drawing
        draw_data = draw_objects(moves, clicked, coins_collected_in_current_level, current_level, lines, balls, portals,
                                 coins, death_time)
        moves = draw_data[0]
        clicked = draw_data[1]
        coins_collected_in_current_level = draw_data[2]

        # Checking collision b/w player and the victory flag
        if player.rect.colliderect(flag.rect):
            # Adding to Score and reset score Variables
            score += 100 + int(25 * moves) + int(25 - (time.time() - st_time)) * 4
            st_time = 0
            death_time = 0
            current_level = load_level_by_num('noname', current_level.number + 1, is_survival=True)

            if current_level == "finish":
                lines = balls = remove_lines_and_balls_of_level_by_number(current_level, lines, balls)
                return ['death', 'completed', score]

            player.body.angular_velocity = 0

            score_data = score_screen(screen, score, data={"score": score, "level": current_level.number})

            if score_data[0] == 'quit':
                return ['quit']
            if score_data[0] == 'welcome':
                lines = balls = remove_lines_and_balls_of_level_by_number(current_level.number, lines, balls)
                return ['welcome']
            if current_level == "finish":
                lines = balls = remove_lines_and_balls_of_level_by_number(current_level.number, lines, balls)
                return ['death', 'completed', score]
        draw_cursor(screen, Themes.active_theme.cursor_c)

        ## -------------------- Updating--------------------
        space.step(1.5 / FPS)
        clock.tick(FPS)
        pygame.display.update()


## ========================= Campaign Mode =========================
def campaign(screen, current_level):
    ## -------------------- Initializing Game --------------------
    score = 0
    st_time = 0  # Time
    death_time = 0  # Death time
    clicked = False

    level_data = load_objects(current_level, 'campaign')
    moves = level_data["moves"]
    lines = level_data["lines"]
    balls = level_data["balls"]
    portals = level_data["portals"]
    coins = level_data["coins"]
    coins_collected_in_current_level = 0

    ## ---------------------------------------- MAIN LOOP ----------------------------------------
    while True:
        screen.fill(Themes.active_theme.background)
        ## -------------------- Time and stuff --------------------
        if st_time == 0:
            coins_collected_in_current_level = 0
            # load level
            lines = balls = remove_lines_and_balls_of_level_by_number(current_level.number, lines, balls)
            level_data = load_objects(current_level, 'campaign')
            moves = level_data["moves"]
            lines = level_data["lines"]
            balls = level_data["balls"]
            portals = level_data["portals"]
            coins = level_data["coins"]
            coins_collected_in_current_level = 0

            st_time = time.time()
        if death_time != 0:
            if death_time - int(time.time()) + 10 <= 0:
                lines = balls = remove_lines_and_balls_of_level_by_number(current_level.number, lines, balls)
                temp_death_data = campaign_death_screen(screen)
                if temp_death_data[0] == 'quit':
                    return ['quit']
                elif temp_death_data[0] == 'level_map':
                    return ['campaign', 'select']
                if temp_death_data[0] == 'restart':
                    return ['campaign', 'continue', current_level.number]

            # giving a 10 seconds timer and Auto reset if not colliding with the Flag
            if death_time != 0:
                screen.blit(
                    small_font.render(str(death_time - int(time.time()) + 10), True, Themes.active_theme.font_c),
                    (WW - 50, 31))

        ## -------------------- Events --------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ['quit']
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.KEYDOWN:
                if moves == 0 and event.key == pygame.K_r:
                    lines = balls = remove_lines_and_balls_of_level_by_number(current_level, lines, balls)
                    player.body.angular_velocity = 0
                    temp_death_data = campaign_death_screen(screen)
                    if temp_death_data[0] == 'quit':
                        return ['quit']
                    elif temp_death_data[0] == 'level_map':
                        return ['campaign', 'select']
                    if temp_death_data[0] == 'restart':
                        return ['campaign', 'continue', current_level.number]

        ## Drawing
        draw_data = draw_objects(moves, clicked, coins_collected_in_current_level, current_level, lines, balls, portals,
                                 coins, death_time)
        moves = draw_data[0]
        clicked = draw_data[1]
        coins_collected_in_current_level = draw_data[2]

        # Checking collision b/w player and the victory flag
        if player.rect.colliderect(flag.rect):
            # Adding to Score and reset score Variables
            score += 100 + int(float(100 * current_level.dict['moves'] / (current_level.dict['moves'] - moves)) / float(
                time.time() - st_time))
            st_time = 0
            death_time = 0
            if current_level.number == User_data.current_level:
                DB.update_level_progress(str(current_level.number + 1))
            current_level = load_level_by_num('noname', current_level.number + 1)
            lines = balls = remove_lines_and_balls_of_level_by_number(current_level, lines, balls)
            player.body.angular_velocity = 0

            next_data = campaign_continue_screen(screen, coins_collected_in_current_level)
            if next_data[0] == 'quit':
                return ['quit']
            if next_data[0] == 'level_map':
                return ['campaign', 'select']
            if next_data[0] == 'continue':
                return ['campaign', 'continue', current_level.number]
        draw_cursor(screen, Themes.active_theme.cursor_c)

        ## -------------------- Updating--------------------
        space.step(1.5 / FPS)
        clock.tick(FPS)
        pygame.display.update()


for error in errors:
    if error == "no name":
        temp_to_do = name_screen(screen)
        if temp_to_do == 'quit':
            to_do[0] = 'quit'
        else:
            User_data.name = DB.fetch_name()
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

    elif to_do[0] == 'death':
        to_do = death_screen(screen, to_do[1], to_do[2])
    elif to_do[0] == 'line':
        to_do = line_select_screen(screen)
    elif to_do[0] == 'ball':
        to_do = skin_select_screen(screen)
        p_img = to_do[1]

    elif to_do[0] == 'quit':
        break
