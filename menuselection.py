import pygame
import os

from particle import *

class MenuSelection:
	def __init__(self):
		self.resources = { 'banner' : pygame.image.load(os.path.abspath('res/gfx/menu_banner.png')),
		                   'newgame_cloud' : pygame.image.load(os.path.abspath('res/gfx/menu_newgame_cloud.png')),
						   'exit_cloud' : pygame.image.load(os.path.abspath('res/gfx/menu_exit_cloud.png'))
                           #'menu_bg' : pygame.mixer.music.load(os.path.abspath('res/mus/menu_bg.mp3'))		   
		}
		
		#pygame.mixer.music.play()
		
		self.selector = 1
		self.cloud = self.resources['newgame_cloud']
		
		# Generate rain particles:
		self.particles = []
		for particle in range(0,30):		
			self.particles = self.particles + [RainParticle()]
		
	def logic(self, delta):
		for particle in self.particles:
			particle.logic(delta)
			if(particle.rect[1] > 600 and particle.alive):
				self.particles.remove(particle)
				self.particles = self.particles + [RainParticle(0)]
	
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
		
	def render(self, screen):
		banner_rect = (0,0, 1000, 600)
		cloud_rect = (200,320,500,500)
		
		screen.blit(self.resources['banner'], banner_rect)
		screen.blit(self.cloud, cloud_rect)
		
		for particle in self.particles:
			pygame.draw.rect(screen, particle.color, particle.rect) 