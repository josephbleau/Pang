import pygame
import os

from particle import *

class MenuSelection:
	def __init__(self):
		self.resources = { 'banner' : pygame.image.load(os.path.abspath('res/gfx/menu_banner.png')),
		                   'newgame_cloud' : pygame.image.load(os.path.abspath('res/gfx/menu_newgame_cloud.png')),
						   'exit_cloud' : pygame.image.load(os.path.abspath('res/gfx/menu_exit_cloud.png')),
                           'menu_bgm' : os.path.abspath('res/mus/menu_bg.mp3')		   
		}

		self.selector = 1
		self.cloud = self.resources['newgame_cloud']
		self.nextstate = None

		# Generate rain particles:
		self.particles = []
		for particle in range(0,30):		
			self.particles = self.particles + [RainParticle()]

		#pygame.mixer.music.load(self.resources['menu_bgm'])
		#pygame.mixer.music.play()
		
	def logic(self, delta):
		for particle in self.particles:
			particle.logic(delta)
			if(particle.rect[1] > 600 and particle.alive):
				self.particles.remove(particle)
				self.particles = self.particles + [RainParticle()]
	
	def input(self, event):
		if(event.type == pygame.KEYUP):
			if(event.key == pygame.K_LEFT or
			   event.key == pygame.K_RIGHT):
				if(self.selector == 1): 
					self.selector = 0
					self.cloud = self.resources['exit_cloud']
				elif(self.selector == 0): 
					self.selector = 1
					self.cloud = self.resources['newgame_cloud']

			if(event.key == pygame.K_RETURN):
				if(self.selector == 1):
					self.nextstate = 'level'
					#pygame.mixer.music.pause()
				if(self.selector == 0):
					exit()
		
	def render(self, screen):
		banner_rect = (0,0, 1000, 600)
		cloud_rect = (200,320,500,500)
		
		screen.blit(self.resources['banner'], banner_rect)
		screen.blit(self.cloud, cloud_rect)
		
		for particle in self.particles:
			pygame.draw.rect(screen, particle.color, particle.rect) 
