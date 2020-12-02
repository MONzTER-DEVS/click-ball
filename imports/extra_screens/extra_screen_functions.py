import requests
from imports.settings import *
from imports.classes import *
mouse_rect = pygame.Rect(0, 0, 10, 10)
select_rect = pygame.Rect(0, 0, 0, 0)
select_rect_color = GRAY
coin = pygame.image.load("assets/imgs/dollar.png")
# coin = pygame.Surface((40, 40))
coin = pygame.transform.scale(coin, (40, 40))

def get_data():
    req = requests.get("http://cb-leaderboard.herokuapp.com/get", params={'game': 'physics'}, timeout=90)
    req = req.json()
    to_return = []
    if len(req) > 10:
        arg_2 = 11
    else:
        arg_2 = len(req) + 1
    for x in range(1, arg_2):
        to_return.append(req[str(x)])
    return to_return


def hover(obj_rect, Screen):
    mouse_rect.center = pygame.mouse.get_pos()
    if mouse_rect.colliderect(obj_rect):
        select_rect.topleft = obj_rect.topleft
        select_rect.size = obj_rect.size

        ## Not using pygame.draw.rect cuz usme opacity set nhi hoti
        s_img = pygame.Surface(select_rect.size)
        s_img.set_alpha(0)
        s_img.fill(select_rect_color)
        Screen.blit(s_img, select_rect.topleft)


def coin_display(screen):
    screen.blit(coin, (WW-200, 10))
    text = small_font.render(f": {User_data.coins}", True, Themes.active_theme.font_c)
    screen.blit(text, (WW-155, 10))
