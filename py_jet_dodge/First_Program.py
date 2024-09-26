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
		self.surf = pygame.image.load("Jet.png").convert()
		self.surf.set_colorkey((25, 25, 25), RLEACCEL)
		self.rect = self.surf.get_rect()
		
	def update(self, pressedKeys):
		if pressedKeys[K_UP]:
			self.rect.move_ip(0, -5)
		if pressedKeys[K_DOWN]:
			self.rect.move_ip(0, 5)
		if pressedKeys[K_LEFT]:
			self.rect.move_ip(-5, 0)
		if pressedKeys[K_RIGHT]:
			self.rect.move_ip(5, 0)
		
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.right > screenWidth:
			self.rect.right = screenWidth
		if self.rect.top <= 0:
			self.rect.top = 0
		if self.rect.bottom >= screenHeight:
			self.rect.bottom = screenHeight
			
			
			
class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super(Enemy, self).__init__()
		self.surf = pygame.image.load("Missle.png").convert()
		self.surf.set_colorkey((255, 255, 255), RLEACCEL)
		self.rect = self.surf.get_rect(
			center=(
				random.randint(screenWidth +20, screenWidth +100),
				random.randint(0, screenHeight),
			)
		)
		self.speed = random.randint(5, 20)
		
	def update(self):
		self.rect.move_ip(-self.speed, 0)
		if self.rect.right < 0:
			self.kill()
			
class Cloud(pygame.sprite.Sprite):
	def __init__(self):
		super(Cloud, self).__init__()
		self.surf = pygame.image.load("Cloud.png").convert()
		self.surf.set_colorkey((0, 0, 0), RLEACCEL)
		
		self.rect = self.surf.get_rect(
			center=(
				random.randint(screenWidth+20, screenWidth+100),
				random.randint(0, screenHeight),
			)
		)
	
	def update(self):
		self.rect.move_ip(-5, 0)
		if self.rect.right < 0:
			self.kill()



pygame.mixer.init()
pygame.init()

screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode([screenWidth, screenHeight])

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

player = Player()
clock = pygame.time.Clock()
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

while running:
	
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False
		elif event.type == QUIT:
			running = False
		
		elif event.type == ADDENEMY:
			
			new_enemy = Enemy()
			enemies.add(new_enemy)
			all_sprites.add(new_enemy)
			
		elif event.type == ADDCLOUD:
			new_cloud = Cloud()
			clouds.add(new_cloud)
			all_sprites.add(new_cloud)
			
			
	pressed_keys = pygame.key.get_pressed()
	player.update(pressed_keys)
	
	enemies.update()
	clouds.update()
	
	screen.fill((135, 206, 250))
	
	for entity in all_sprites:
		screen.blit(entity.surf, entity.rect)
		
	if pygame.sprite.spritecollideany(player, enemies):
		player.kill()
		running = False

	pygame.display.flip()
	clock.tick(30)
