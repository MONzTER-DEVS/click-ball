# Imports
import math
import pygame
import pymunk
import os
import sqlite3
import time
import threading
from .settings import *
from .encryption import *

# from settings import WW, WH

GLOBAL_FRICTION = 0.5
shading = 5
shade = False
border = 5


# Dynamic means it will move
class DynamicBall:
    def __init__(self, pos, vx, vy, img_of_32px, space):
        ## Image
        self.image = img_of_32px
        ## Body
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)  ## name suggests everything -_-
        self.body.position = tuple(pos)  ## name suggests everything -_-
        self.body.velocity = vx, vy  ## name suggests everything -_-
        ## Shape
        self.shape = pymunk.Circle(self.body, 16)  ## this is the collision shape
        self.shape.density = 1  ## if set to 0, body will behave wierdly
        self.shape.elasticity = 0.50  ## name suggests everything -_-
        self.shape.friction = GLOBAL_FRICTION
        ## Adding to the space
        space.add(self.body, self.shape)
        self.shape.collision_type = 1  ## idk wht this does, but if i comment it, the ball doesn't move
        ## This will b used for collsions for pygame
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(
            self.body.position.x,
            self.body.position.y,
            self.shape.radius * 2,
            self.shape.radius * 2
        )

    def draw(self, surf):
        ## Pygame comes into action ;)
        x, y = self.body.position
        self.rect.center = self.shape.body.position

        rotated_image = pygame.transform.rotate(self.image, -math.degrees(self.body.angle))
        new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=self.rect.topleft).center)

        if shade:
            pygame.draw.circle(surf, GRAY, (self.rect.centerx + shading, self.rect.centery + shading), 16)

        surf.blit(rotated_image, new_rect.topleft)


class DynamicBallWithColor:
    def __init__(self, pos, vx, vy, radius, space):
        ## Body
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)  ## name suggests everything -_-
        self.body.position = tuple(pos)  ## name suggests everything -_-
        self.body.velocity = vx, vy  ## name suggests everything -_-
        ## Shape
        self.shape = pymunk.Circle(self.body, radius)  ## this is the collision shape
        self.shape.density = 1  ## if set to 0, body will behave wierdly
        self.shape.elasticity = 0.50  ## name suggests everything -_-
        self.shape.friction = GLOBAL_FRICTION
        ## Adding to the space
        space.add(self.body, self.shape)
        self.shape.collision_type = 1  ## idk wht this does, but if i comment it, the ball doesn't move
        ## This will b used for collsions for pygame
        self.radius = radius
        self.rect = pygame.Rect(
            self.body.position.x,
            self.body.position.y,
            self.shape.radius * 2,
            self.shape.radius * 2
        )

    def draw(self, surf, color):
        ## Pygame comes into action ;)
        x, y = self.body.position
        self.rect.center = self.shape.body.position
        if shade:
            pygame.draw.circle(surf, GRAY, (self.rect.centerx + shading, self.rect.centery + shading), self.radius // 2)
        pygame.draw.ellipse(surf, color, self.rect)


# Box is slow so just draw a line with the width ;)
# looks the same tho
class StaticLine:
    all_lines = []

    def __init__(self, start_point, end_point, w, space):
        ## Body
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)  ## name suggests everything -_-
        # self.body.position = x, y                   ## name suggests everything -_-
        ## Shape
        self.shape = pymunk.Segment(self.body, start_point, end_point, w)  ## this is the collision shape
        self.shape.elasticity = 1  ## name suggests everything -_-
        self.shape.friction = GLOBAL_FRICTION
        ## Adding to the space
        space.add(self.body, self.shape)
        self.shape.collision_type = 1  ## idk wht this does
        StaticLine.all_lines.append(self)

    def draw(self, surf, color):
        if shade:
            sx1, sy1 = self.shape.a[0] + shading, self.shape.a[1] + shading
            sx2, sy2 = self.shape.b[0] + shading, self.shape.b[1] + shading
            pygame.draw.line(surf, GRAY, (sx1, sy1), (sx2, sy2), int(self.shape.radius) * 2)
        spos = self.shape.a
        epos = self.shape.b
        thicc = int(self.shape.radius) * 2
        x1, y1 = spos
        x2, y2 = epos
        # pygame.draw.lines()
        pygame.draw.line(surf, color, spos, epos, thicc)


# Victory Flag
class VictoryFlag:
    def __init__(self, pos):  # U have to put bottom point of the flag while making an instance
        self.image = pygame.image.load(os.path.join('assets', 'imgs', 'victory_flag.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = tuple(pos)

    def draw(self, screen):
        if shade:
            pygame.draw.circle(screen, GRAY, (self.rect.centerx + shading, self.rect.centery + shading),
                               self.rect.w // 2)
        screen.blit(self.image, self.rect.topleft)


class Themes:
    themes = []
    active_theme = None

    def __init__(self, name, bg, platform_c, mouse_line, font_c, hover, bouncing_ball_c, button_c, cursor_c):
        self.name = name
        self.background = bg
        self.platform_c = platform_c
        self.mouse_line = mouse_line
        self.font_c = font_c
        self.hover = hover
        self.bouncing_ball_c = bouncing_ball_c
        self.button_c = button_c
        self.cursor_c = cursor_c
        Themes.themes.append(self)

    def set_to_active_theme(self):
        Themes.active_theme = self

    @staticmethod
    def set_active_by_name(name):
        for theme in Themes.themes:
            if theme.name == name:
                Themes.active_theme = theme


class Portal:
    def __init__(self, start_pos, end_pos, radius, size = "big"):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.radius = radius
        self.size = size
        if self.size == "big":
            self.start_img = pygame.image.load('assets/imgs/PortalStart.png').convert_alpha()
            self.end_img = pygame.image.load('assets/imgs/PortalEnd.png').convert_alpha()
        elif self.size == "med":
            self.start_img = pygame.image.load('assets/imgs/PortalStartMed.png').convert_alpha()
            self.end_img = pygame.image.load('assets/imgs/PortalEndMed.png').convert_alpha()

        elif self.size == "small":
            pass
        self.start_rect = self.start_img.get_rect()
        self.end_rect = self.end_img.get_rect()
        self.start_rect.center = self.start_pos
        self.end_rect.center = self.end_pos

    def draw(self, surf, space):
        self.start_rect.center = self.start_pos
        self.end_rect.center = self.end_pos
        if shade:
            pygame.draw.circle(surf, GRAY, (self.start_rect.centerx + shading, self.start_rect.centery + shading),
                               self.start_rect.w // 2)
            pygame.draw.circle(surf, GRAY, (self.end_rect.centerx + shading, self.end_rect.centery + shading),
                               self.start_rect.w // 2)
        surf.blit(self.start_img, self.start_rect.topleft)
        surf.blit(self.end_img, self.end_rect.topleft)
        pygame.draw.line(surf, (100, 100, 100), self.start_pos, self.end_pos)

    def teleport(self, obj):
        if obj.rect.colliderect(self.start_rect):
            obj.body.position = self.end_rect.center


class Coins:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.images = [
            pygame.transform.smoothscale(pygame.image.load(f"assets/imgs/coins/{x}.png").convert_alpha(), (35, 35)) for
            x in range(1, 11)]
        self.step = 0
        self.step_step = 0
        self.rect = self.images[0].get_rect()
        self.rect.center = (self.x, self.y)
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            self.rect.center = (self.x, self.y)
            self.step_step += 1
            if self.step_step > 4:
                self.step_step = 0
                self.step += 1
            if self.step > 9:
                self.step = 0
            if shade:
                pygame.draw.circle(screen, GRAY, (self.rect.centerx + shading, self.rect.centery + shading),
                                   self.rect.w // 2)
            screen.blit(self.images[self.step], self.rect.topleft)

    def collect(self, player_rect):
        if self.rect.colliderect(player_rect) and not self.collected:
            self.collected = True
            return 10
        return 0


class Levels:
    levels = []

    def __init__(self, name, data):
        self.dict = data
        self.name = name
        self.number = len(Levels.levels) + 1
        Levels.levels.append(self)


class User_data:
    current_level = None
    save = None
    coins = None
    name = None
    line = "new"

    @staticmethod
    def get_save():
        """
        Use this Function to get data
        """

        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        to_return = User_data.save

        query = f"UPDATE user_data SET save = '{Crypt.en('None')}'"
        c.execute(query)
        User_data.save = None
        conn.commit()

        conn.close()
        return to_return

    @staticmethod
    def increment_coins(number_of_coins_to_increment):
        """
        use this function to increment Value of coins
        """

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        query = f"UPDATE user_data SET coins = '{Crypt.en(str(User_data.coins + number_of_coins_to_increment))}'"
        c.execute(query)
        User_data.coins += number_of_coins_to_increment
        conn.commit()
        conn.close()


class Music:
    play = False

    @staticmethod
    def play_music():
        def inner():
            Music.play = True
            pygame.mixer.music.load('assets/sounds/music/intro.ogg')
            pygame.mixer.music.play(1)
            time.sleep(24)
        music_thread = threading.Thread(target=inner)
        music_thread.start()
        music_thread.join()

        if Music.play:
            if pygame.mixer.get_init():
                pygame.init()
                pygame.mixer.music.load('assets/sounds/music/loop.ogg')
                pygame.mixer.music.play(-1)

    @staticmethod
    def stop_music():
        pygame.mixer.music.fadeout(1500)
        Music.play = False
