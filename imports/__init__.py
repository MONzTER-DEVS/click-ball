import pygame

pygame.init()

from .settings import *
from .classes import *

#                      name,               bg,       platform_c, mouse_line, font_c,  hover
light_theme = Themes('Bright White', WHITE, L_BLUE, GREEN, PINK, WHITE)
violet_theme = Themes("Limited Voilet", PURPLE, WHITE, WHITE, WHITE, WHITE)
dark_light_theme = Themes("Darkest Light", BLACK, WHITE, WHITE, L_BLUE, WHITE)
dracula_theme = Themes("Dracula", BLACK, PINK, PINK, PINK, WHITE)

from .extra_screens import *
from .db_functions import *

# Make DB if it doesnt Exist
if not os.path.exists(os.path.join('assets', 'data.db')):
    DB.make_db()

data = DB.load_all_data()
Themes.set_active_by_name(data[0])

values = DB.load_save()