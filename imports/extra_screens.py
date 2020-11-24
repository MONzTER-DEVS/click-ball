from .settings import *

mouse_rect = pygame.Rect(0, 0, 10, 10)
select_rect = pygame.Rect(0, 0, 0, 0)
select_rect_color = GRAY


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


def welcome_screen(screen):
	clicked = False
	mx, my = pygame.mouse.get_pos()
	while True:
		screen.fill((255, 255, 255))

		# display
		heading_text = big_font.render('Clicker Ball!', True, (0, 0, 0))
		heading_rect = heading_text.get_rect()
		heading_rect.center = (WW / 2, 50)
		screen.blit(heading_text, heading_rect.topleft)

		heading_text = medium_font.render('game', True, (0, 0, 0))
		heading_rect = heading_text.get_rect()
		heading_rect.center = (WW / 2, 250)
		screen.blit(heading_text, heading_rect.topleft)

		hover(heading_rect, screen)
		if clicked:
			if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
				return ['game']

		# Themes Screen
		heading_text = small_font.render('Themes', True, (0, 0, 0))
		heading_rect = heading_text.get_rect()
		heading_rect.center = (WW / 2, WH-100)
		screen.blit(heading_text, heading_rect.topleft)
		hover(heading_rect, screen)
		if clicked:
			if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
				return ['themes']

		# Leaderboard
		heading_text = small_font.render('Leaderboard', True, (0, 0, 0))
		heading_rect = heading_text.get_rect()
		heading_rect.center = (WW / 2, WH-50)
		screen.blit(heading_text, heading_rect.topleft)
		hover(heading_rect, screen)
		if clicked:
			if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
				return ['leaderboard']

		# Ball Screen
		heading_text = small_font.render('change Ball', True, (0, 0, 0))
		heading_rect = heading_text.get_rect()
		heading_rect.center = (WW*7/8, WH-50)
		screen.blit(heading_text, heading_rect.topleft)
		hover(heading_rect, screen)
		if clicked:
			if heading_rect.left < mx < heading_rect.right and heading_rect.top < my < heading_rect.bottom:
				return ['ball']


		# Events
		clicked = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return ['quit']
			elif event.type == pygame.MOUSEBUTTONDOWN:
				clicked = True
				mx, my = pygame.mouse.get_pos()

		pygame.display.update()
