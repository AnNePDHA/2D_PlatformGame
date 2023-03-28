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
		self.rect.y += size - 64
		self.animation_speed = 0.15
		self.speed = 3

		# boss status
		self.status = 'walk'
		self.onHit = False
		self.onAttack = False

		# health management
		self.change_health = change_health
		self.invincible = False
		self.invincibility_duration = 500
		self.hurt_time = 0

	def import_character_assets(self):
		character_path = '../graphics/BiggerBoss/'
		self.animations = {'idle':[], 'walk':[],'attack':[],'hurt':[], 'death':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def animate(self):
		animation = self.animations[self.status]

		# loop over frame index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
			self.onHit = False
			self.onAttack = False

		self.image = animation[int(self.frame_index)]

		if self.invincible:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

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

	def get_status(self):
		if self.onHit:
			if self.status != 'hurt':
				self.status = 'hurt'
				self.frame_index = 0
				self.get_damage()
				if self.change_health <= 0:
					self.kill()
		elif self.onAttack:
			if self.status != 'attack':
				self.status = 'attack'
				self.frame_index = 0
		else:
			if self.status != 'walk':
				self.status = 'walk'
				self.frame_index = 0
			self.move()

	def get_damage(self):
		if not self.invincible:
			self.change_health -= 5
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
