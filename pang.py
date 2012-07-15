#!/usr/bin/python

from menu import *
from level import *

def main():
	random.seed()
	pygame.init()
	screen = pygame.display.set_mode((1000,600))
	
	gamestates = { 'menu' : MenuSelection(),
                   'level': Level(4) }

	currentstate = gamestates['menu']
	
	timekeeper = pygame.time.Clock()

	while True:
		timekeeper.tick()
		if(currentstate.nextstate):
			currentstate = gamestates[currentstate.nextstate]

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
				
			currentstate.input(event)
		
		delta = float(timekeeper.get_time())/ float(1000)

		if(delta > .03):
			delta = .03

		currentstate.logic(delta)
		currentstate.render(screen)

		pygame.display.flip()
				
if __name__ == "__main__":
	main()
