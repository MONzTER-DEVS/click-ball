import requests
from imports.settings import *
from imports.classes import *

mouse_rect = pygame.Rect(0, 0, 10, 10)
select_rect = pygame.Rect(0, 0, 0, 0)
select_rect_color = GRAY
coin = pygame.image.load(os.path.join('assets', 'imgs', 'dollar.png'))
coin = pygame.transform.scale(coin, (40, 40))

URL = "http://cb-leaderboard.herokuapp.com"


def send_data_to_leaderboard(name, score):
    params = {
        'game': 'physics',
        'name': name,
        'score': score
    }

    requests.get(URL, params=params, timeout=90)


def get_data():
    req = requests.get(f"{URL}/get", params={'game': 'physics'}, timeout=90)
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


def coin_display(screen, coins=User_data.coins):
    if coins is None:
        coins = User_data.coins
    screen.blit(coin, (WW - 200, 10))
    text = small_font.render(f": {coins}", True, Themes.active_theme.font_c)
    screen.blit(text, (WW - 155, 10))


class Buttons:
    shift = 1.1

    def __init__(self, img, x, y, width, height):
        try:
            self.small_img = pygame.transform.smoothscale(img, (width, height))
        except Exception:
            self.small_img = pygame.transform.smoothscale(img.surface, (width, height))

        try:
            self.big_img = pygame.transform.smoothscale(img, (int(width * Buttons.shift), int(height * Buttons.shift)))
        except Exception:
            self.big_img = pygame.transform.smoothscale(img.surface,
                                                        (int(width * Buttons.shift), int(height * Buttons.shift)))
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.small_rect = self.small_img.get_rect(center=(self.x, self.y))
        self.big_rect = self.big_img.get_rect(center=(self.x, self.y))

    def draw(self, screen, mx, my):
        mouse_rect = pygame.Rect(mx - 5, my - 5, 10, 10)
        if not (mouse_rect.colliderect(self.small_rect) or mouse_rect.colliderect(self.big_rect)):
            screen.blit(self.small_img, self.small_rect.topleft)
        else:
            screen.blit(self.big_img, self.big_rect.topleft)

    def is_clicked(self, clicked, mx, my):
        mouse_rect = pygame.Rect(mx - 5, my - 5, 10, 10)
        if mouse_rect.colliderect(self.small_rect) or mouse_rect.colliderect(self.big_rect):
            if clicked:
                return True
        return False


def draw_cursor(screen, color=(0, 0, 0)):
    pygame.draw.circle(screen, color, pygame.mouse.get_pos(), 15, 10)
