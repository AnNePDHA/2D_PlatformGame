import pygame
from tiles import AnimatedTile
from support import import_folder
from math import sin
from random import randint

class Boss(AnimatedTile):
	def __init__(self,size,x,y,change_health):
		super().__init__(size,x,y,'../graphics/BiggerBoss/walk')
		self.import_character_assets()
		self.image = self.animations['walk'][self.frame_index]
		self.rect.y += size - self.image.get_size()[1]
		self.animation_speed = 0.15
		self.speed = 3

		# boss status
		self.status = 'walk'
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False
		self.onHit = False
		self.onAttack = False

		# health management
		self.change_health = change_health
		self.invincible = False
		self.invincibility_duration = 500
		self.hurt_time = 0

	def import_character_assets(self):
		character_path = '../graphics/BiggerBoss/'
		self.animations = {'walk':[],'attack':[],'hurt':[], 'death':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def animate(self):
		animation = self.animations[self.status]
		self.image = self.frames[int(self.frame_index)]

		# loop over frame index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
			self.onHit = False
			self.onAttack = False

		self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

	def move(self):
		self.rect.x += self.speed

	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image,True,False)

	def reverse(self):
		self.speed *= -1

	def set_status(self, status):
		self.status = status
		print(self.status)

	def get_status(self):
		if self.onHit:
			self.status = 'hurt'
			self.get_damage()
			if self.change_health <= 0:
				self.kill()
		elif self.onAttack:
			if self.status != 'attack':
				self.status = 'attack'
		else:
			self.move()

	def get_damage(self):
		if not self.invincible:
			self.change_health -= 10
			self.invincible = True
			self.onHit = True
			self.onAttack = False
			self.frame_index = 0
			self.hurt_time = pygame.time.get_ticks()

	def invincibility_timer(self):
		if self.invincible:
			current_time = pygame.time.get_ticks()
			if current_time - self.hurt_time >= self.invincibility_duration:
				self.invincible = False

	def wave_value(self):
		value = sin(pygame.time.get_ticks())
		if value >= 0: return 255
		else: return 0

	def update(self,shift):
		self.rect.x += shift
		self.get_status()
		self.animate()
		self.invincibility_timer()
		self.wave_value()
		self.reverse_image()
