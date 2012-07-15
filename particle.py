import pygame
import random

class Particle:
	def __init__(self, rect, velocity, color, ttd=300):
		self.rect = rect
		self.velocity = velocity
		self.color = color
		self.time_alive = 0
		self.ttd = ttd
		self.alive = True
		
	def logic(self, delta):
		self.rect[0] = self.rect[0] + (self.velocity[0] * delta)
		self.rect[1] = self.rect[1] + (self.velocity[1] * delta)
		self.time_alive = self.time_alive + delta

def RainParticle():
	particle_rect = pygame.Rect(random.randint(0,1000), 0, 20, 20)
	particle_color = pygame.Color(0, 0, random.randint(100,150), 100)
	particle_ttd = random.randint(600,1200)
	particle = Particle(particle_rect, (0, random.randint(150,350)), particle_color, particle_ttd)
	return particle

def Bullet(origin):
	particle_rect = pygame.Rect(origin[0], origin[1], 10, 10)
	particle_velocity = [0,-400]
	gray = random.randint(100,200)	
	particle_color = pygame.Color(gray,gray,gray,0)
	particle_ttd = 1000
	particle = Particle(particle_rect, particle_velocity, particle_color, particle_ttd)

	return particle

def ShotgunSpray(origin):
	particles = []
	for i in range(0,2):
		bullet = Bullet(origin)
		bullet.rect[0] = bullet.rect[0] + random.randint(-8,8)
		bullet.color = pygame.Color(30,100,150,0)
		bullet.velocity[0] = random.randint(-250,250)
		particles.append(bullet)
		
	return particles
		