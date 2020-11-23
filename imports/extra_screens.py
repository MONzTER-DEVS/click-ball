from .settings import *

def welcome_screen(screen):
    clicked = False
    while True:
        screen.fill((255,255,255))

        # display 
        heading_text = big_font.render('Clicker Ball!', True, (0, 0, 0))
        heading_rect = heading_text.get_rect()
        heading_rect.center = (WW/2, 50)
        screen.blit(heading_text, heading_rect.topleft)

       	pygame.display.update()

       	# Events
       	for event in pygame.event.get():
       		if event.type == pygame.QUIT:
       			return 'quit'
       		elif event.type == pygame.KEYDOWN:
       			return 'start'
       		elif event.type == pygame.MOUSEBUTTONDOWN:
       			clicked = True