# Imports
import json
import math
import os
import pygame
import pymunk

# from settings import WW, WH

GLOBAL_FRICTION = 0.5


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

        surf.blit(rotated_image, new_rect.topleft)


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
        pygame.draw.line(surf, color, self.shape.a, self.shape.b, int(self.shape.radius) * 2)


# Victory Flag
class VictoryFlag:
    def __init__(self, pos):  # U have to put bottom point of the flag while making an instance
        self.image = pygame.image.load(os.path.join('assets', 'imgs', 'victory_flag.png'))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = tuple(pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Themes:
    themes = []
    active_theme = None

    def __init__(self, name, bg, platform_c, mouse_line, font_c, hover):
        self.name = name
        self.background = bg
        self.platform_c = platform_c
        self.mouse_line = mouse_line
        self.font_c = font_c
        self.hover = hover
        Themes.themes.append(self)

    def set_to_active_theme(self):
        Themes.active_theme = self

    @staticmethod
    def set_active_by_name(name):
        for theme in Themes.themes:
            if theme.name == name:
                Themes.active_theme = theme


class Portal:
    def __init__(self, start_pos, end_pos, radius):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.radius = radius
        self.start_rect = pygame.Rect(self.start_pos, 2 * self.radius, 2 * self.radius)
        self.end_rect = pygame.Rect(self.end_pos, 2 * self.radius, 2 * self.radius)

    def draw(self, surf, color):
        pygame.draw.ellipse(surf, color, self.start_rect)
        pygame.draw.ellipse(surf, color, self.end_rect)

    def teleport(self, obj):
        if obj.rect.colliderect(self.start_rect):
            obj.body.position = self.end_pos
        if obj.rect.colliderect(self.end_rect):
            obj.body.position = self.start_pos


class Particle():
    particles = []

    def __init__(self, pos, ran, num):
        self.pos = pygame.Vector2(pos)
        self.ran = ran
        for p in range(num):
            Particle.particles.append(self)

    @staticmethod
    def do_particle_thingy():
        pass


class Levels:
    levels = []

    def __init__(self, name, data):
        self.dict = data
        self.name = name
        self.number = len(Levels.levels) + 1
        Levels.levels.append(self)
