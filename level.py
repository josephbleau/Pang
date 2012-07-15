import pygame
import os
import string
import random

from player import *

class Skypiece:
	def __init__(self, rect, velocity, color):
		self.rect = rect
		self.lastrect = self.rect.copy()
		self.velocity = velocity
		self.color = color 
		self.size = 3
		
		
	def logic(self, delta):
		self.lastrect = self.rect.copy()
		
		if(self.velocity[0] < 0):
			self.rect[0] = self.rect[0] + (self.velocity[0] * delta)
		else:
			self.rect[0] = self.rect[0] + 1 + (self.velocity[0] * delta)
			
		if(self.velocity[1] < 0):
			self.rect[1] = self.rect[1] + (self.velocity[1] * delta)
		else:
			self.rect[1] = self.rect[1] + 1 + (self.velocity[1] * delta)
		
		if(self.rect[0] <= 0 or self.rect[0] > 1000):
			self.rect = self.lastrect.copy()
			self.velocity[0] = self.velocity[0] * -1
		if(self.rect[1] <= 0 or self.rect[1] > 600):
			self.rect = self.lastrect.copy()
			self.velocity[1] = self.velocity[1] * -1
	
		
	def render(self, screen):
		pygame.draw.rect(screen, self.color, self.rect)

	def split(self):
		if(self.size > 1):
			left = Skypiece(self.rect.copy(), [self.velocity[0] * -1, self.velocity[1]], self.color)
			right = Skypiece(self.rect.copy(), [self.velocity[0], self.velocity[1]], self.color)
			left.rect[2] /= 2
			left.rect[3] /= 2
			right.rect[2] /= 2
			right.rect[3] /=2
			left.size  = self.size - 1
			right.size = self.size - 1
		 	
			return [left,right]
		return None
		
class Piece:
	def __init__(self, rect, color, name):
		self.rect = rect
		self.color = color
		self.name = name
		
class Level:
	def __init__(self, name):
		self.world = pygame.Rect(0,0,1000,600)
		self.background = pygame.image.load(os.path.abspath('res/lvl/'+str(name)+'.png'))
		self.data = {}

		self.nextstate = None
		
		self.bullets = []
		self.skypieces = []
		self.pieces = []
		
		self.player = Player(self)
		
		# Analyze level map, pull out appropriate rects
		self.surfarray = pygame.PixelArray(self.background)
		
		# Get level information
		self.data['background'] = self.background.unmap_rgb(self.surfarray[0][0])
		self.data['platform'] = self.background.unmap_rgb(self.surfarray[1][0])
		self.data['ladder'] = self.background.unmap_rgb(self.surfarray[2][0])
		self.data['enemy'] = self.background.unmap_rgb(self.surfarray[3][0])
		self.data['player'] = self.background.unmap_rgb(self.surfarray[4][0])
			
		for x in range(0,40):
			for y in range(1,24):
				c = self.background.unmap_rgb(self.surfarray[x][y])
				
				if( c == self.data['player'] ):
					self.player.rect[0] = x * 25
					self.player.rect[1] = y * 25 - 26
				elif( c == self.data['enemy'] ):
					self.skypieces.append(Skypiece(pygame.Rect(x*25,y*25,50,50), [100,150], c))
				elif( c == self.data['ladder'] ):
					piecerect = pygame.Rect(x*25, y*25, 25, 25)
					self.pieces.append( Piece(piecerect, c, 'ladder') )
				elif( c == self.data['platform'] ):
					piecerect = pygame.Rect(x*25, y*25, 25, 25)
					self.pieces.append( Piece(piecerect, c, 'platform') )
					
	def logic_player_collision(self, delta):
		# Gravity
		if(not self.player.ladder):
			self.player.velocity[1] = self.player.velocity[1] + 1 + 1500 * delta
			
		self.player.logic(delta)
		
		self.player.ladder = False
		
		for piece in self.pieces:
			if(piece.name == 'platform'):
				if(piece.rect.colliderect(self.player.bottom)):
					self.player.rect[1] = self.player.rect[1] - 1
					self.player.velocity[1] = 0
					self.player.inair = False
				if(piece.rect.colliderect(self.player.top)):
					self.player.rect[1] = self.player.rect[1] + 1
					self.player.velocity[1] = 0
				if(piece.rect.colliderect(self.player.left)):
					self.player.rect[0] = self.player.rect[0] + 1
				if(piece.rect.colliderect(self.player.right)):
					self.player.rect[0] = self.player.rect[0] - 1
					
			if(piece.name == 'ladder'):
				if(piece.rect.colliderect(self.player.rect)):
					self.player.ladder = True
					if(not piece.rect.colliderect(self.player.bottom)):
						self.player.inair = False
		
	def logic_bullet_collision(self, delta):
		for bullet in self.bullets:
			bullet.logic(delta)
			
			if(self.player.weapon == 1):
				bullet.velocity[1] = bullet.velocity[1] + 1 + 500 * delta
			
			for skypiece in self.skypieces:
				if(skypiece.rect.colliderect(bullet.rect)):
					split = skypiece.split()
					if(split != None):
						self.skypieces = self.skypieces + skypiece.split()
					self.skypieces.remove(skypiece)
					self.bullets.remove(bullet)
					break
			
			# If bullet leaves game world, delete!
			if(not self.world.contains(bullet.rect)):
				self.bullets.remove(bullet)
				break
			
			for piece in self.pieces:
				if(piece.rect.colliderect(bullet.rect) and piece.name == 'platform'):
					self.bullets.remove(bullet)
					break
						
	def logic(self, delta):
		self.logic_player_collision(delta)
		self.logic_bullet_collision(delta)
		
		for skypiece in self.skypieces:
			skypiece.logic(delta)
			
	def input(self, event):
		self.player.input(event)

	def render(self, screen):
		bg_rect = (0,0,1000,600)
		pygame.draw.rect(screen, self.data['background'], bg_rect)

		# Draw Level Pieces
		for piece in self.pieces:
			pygame.draw.rect(screen, piece.color, piece.rect)
				
		# Draw Skypieces
		for skypiece in self.skypieces:
			skypiece.render(screen)
				
		# Draw Player
		self.player.render(screen)

		# Render Projectiles
		for bullet in self.bullets:
			pygame.draw.rect(screen, bullet.color, bullet.rect)