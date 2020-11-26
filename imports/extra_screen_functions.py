import requests

from .settings import *
mouse_rect = pygame.Rect(0, 0, 10, 10)
select_rect = pygame.Rect(0, 0, 0, 0)
select_rect_color = GRAY


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
        s_img.set_alpha(50)
        s_img.fill(select_rect_color)
        Screen.blit(s_img, select_rect.topleft)

