import pygame

pygame.init()

from .settings import *
from .classes import *

#                      name,               bg,       platform_c, mouse_line, font_c,  hover
light_theme = Themes('Bright White',      WHITE,     L_BLUE,     GREEN,      PINK,   WHITE)
violet_theme = Themes("Limited Voilet",   PURPLE,    WHITE,      WHITE,      WHITE,  WHITE)
dark_light_theme = Themes("Darkest Light",BLACK,     WHITE,      WHITE,      L_BLUE, WHITE)
dracula_theme = Themes("Dracula",         BLACK,     PINK,       PINK,       PINK,   WHITE)
light_theme.set_to_active_theme()

from .extra_screens import *