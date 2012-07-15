import pygame

from particle import *

class Player:
	def __init__(self, parent):
		self.parent = parent

		self.rect = pygame.Rect(0,0,25,50)
		self.lastdrawloc = self.rect.copy()
		
		self.left = pygame.Rect(0,1,1,48)
		self.right = pygame.Rect(23,1,1,48)
		self.top = pygame.Rect(1,0,23,2)
		self.bottom = pygame.Rect(1,49,23,2)
		
		self.lastrect = self.rect.copy()
		self.color = pygame.Color(40,40,40,0)
		self.velocity = [0,0]

		self.rightdown = False
		self.leftdown = False
		self.updown = False
		self.downdown = False
		self.inair = False
		self.ladder = False
		self.head_above_ladder = False
		
		self.weapon = 1

	def input(self, event):
		if(event.type == pygame.KEYDOWN):
			if(event.key == pygame.K_RIGHT):
				self.rightdown = True
			elif(event.key == pygame.K_LEFT):
				self.leftdown = True	
			if(event.key == pygame.K_UP and not self.inair):
				self.velocity[1] = -400
				self.inair = True
			if(event.key == pygame.K_UP):
				self.updown = True
			if(event.key == pygame.K_DOWN):
				self.downdown = True

		elif(event.type == pygame.KEYUP):
			if(event.key == pygame.K_RIGHT):
				self.rightdown = False
			elif(event.key ==pygame.K_LEFT):
				self.leftdown = False	
			if(event.key == pygame.K_SPACE):
				bulletpos = pygame.Rect(self.rect)
				bulletpos[0] = bulletpos[0]+bulletpos[2]/2
				bulletpos[1] = bulletpos[1]+bulletpos[3]/2
				
				if(self.weapon == 1):
					self.parent.bullets = self.parent.bullets + [Bullet(bulletpos)]
				if(self.weapon == 2):
					for bullet in ShotgunSpray(bulletpos):
						self.parent.bullets.append(bullet)
					
			if(event.key == pygame.K_UP):
				self.updown = False
			if(event.key == pygame.K_DOWN):
				self.downdown = False
				
	def logic(self, delta):	
		self.lastrect = self.rect.copy()
		
		if(self.rightdown):
			self.rect[0] = self.rect[0] + 1 + 200 * delta
		if(self.leftdown):
			self.rect[0] = self.rect[0] - 200 * delta
			
		if(self.updown and self.ladder):
			self.rect[1] = self.rect[1] - 200 * delta 
		if(self.downdown and self.ladder):
			self.rect[1] = self.rect[1] + 1 + 200 * delta

		if(not self.ladder):
			self.rect[1] = self.rect[1] + self.velocity[1] * delta
		
		# Prevent player from leaving game area
		world = pygame.Rect(0,0,1000,600)
		if(not world.contains(self.rect)):
			self.rect = self.lastrect.copy()
		
		self.left[0] = self.rect[0]
		self.left[1] = self.rect[1] + 1
		self.right[0] = self.rect[0]+24
		self.right[1] = self.rect[1] + 1
		self.top[0] = self.rect[0] + 1
		self.top[1] = self.rect[1]
		self.bottom[0] = self.rect[0] + 1
		self.bottom[1] = self.rect[1] + self.rect[3] - 1


	def render(self, screen):
		drawrect = self.rect.copy()
		if(abs(self.rect[0] - self.lastdrawloc[0]) > 1):
			drawrect[0] = self.rect[0]
			self.lastdrawloc[0] = self.rect[0]
		if(abs(self.rect[1] - self.lastdrawloc[1]) > 1):
			drawrect[1] = self.rect[1]
			self.lastdrawloc[1] = self.rect[1]
			
		if(drawrect == self.rect):
			drawrect = self.lastdrawloc.copy()
			
		drawrect[0] = drawrect[0] - 1
		drawrect[1] = drawrect[1] - 1
		drawrect[2] = drawrect[2] + 2
		drawrect[3] = drawrect[3] + 3
		pygame.draw.rect(screen, (50,50,50,0), drawrect)
