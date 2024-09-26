import pygame
import random

from pygame.locals import (
	RLEACCEL,
	K_UP,
	K_DOWN,
	K_LEFT,
	K_RIGHT,
	K_ESCAPE,
	KEYDOWN,
	QUIT,
)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.surf = pygame.image.load("Player.png").convert()
		self.surf.set_colorkey((128, 128, 128), RLEACCEL)
		self.rect = self.surf.get_rect(center = (80, 80))
		self.mask = pygame.mask.from_surface(self.surf)
		self.Yspeed = 0
		self.Xspeed = 0
		
	def update(self, pressedKeys, solids):
		self.Yspeed += 1
		
		self.rect.move_ip(0, 1)
		if pressedKeys[K_UP]:
			if not pygame.sprite.collide_mask(self, solids) == None:
				self.Yspeed = -10
		self.rect.move_ip(0, -1)

		if pressedKeys[K_LEFT]:
			self.Xspeed -= 1
		if pressedKeys[K_RIGHT]:
			self.Xspeed += 1
			
		self.Xspeed *= 0.9
		
		self.rect.move_ip(self.Xspeed, 0)
		if not pygame.sprite.collide_mask(self, solids) == None:
			if self.Xspeed > 0:
				while not pygame.sprite.collide_mask(self, solids) == None:
					self.rect.move_ip(-1,0)
			else:
				while not pygame.sprite.collide_mask(self, solids) == None:
					self.rect.move_ip(1,0)
			self.Xspeed = 0

		self.rect.move_ip(0, self.Yspeed)
		if not pygame.sprite.collide_mask(self, solids) == None:
			if self.Yspeed > 0:
				while not pygame.sprite.collide_mask(self, solids) == None:
					self.rect.move_ip(0,-1)
			else:
				while not pygame.sprite.collide_mask(self, solids) == None:
					self.rect.move_ip(0,1)
			self.Yspeed = 0
		
			
class Platforms(pygame.sprite.Sprite):
	def __init__(self):
		super(Platforms, self).__init__()
		self.surf = pygame.image.load("Platforms.png").convert()
		self.surf.set_colorkey((128, 128, 128), RLEACCEL)
		self.rect = self.surf.get_rect()
		self.mask = pygame.mask.from_surface(self.surf)

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()
player = Player()
platforms = Platforms()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(platforms)



running = True
while running:

	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
		elif event.type == QUIT:
			running = False
			
			
	pressed_keys = pygame.key.get_pressed()
	player.update(pressed_keys, platforms)
	
	screen.fill((50, 100, 150))
	
	for entity in all_sprites:
		screen.blit(entity.surf, entity.rect)
	
	pygame.display.flip()
	clock.tick(30)
