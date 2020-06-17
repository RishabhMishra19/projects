import numpy as np
import pygame
import sys
from SNAKE import snake
from FOOD import FOOD
		

def gameOver():
	pygame.quit()
	sys.exit()




#frame = input("Enter frame rate(for speed)\n(Enter 'F' for full speed)\n(You may start with a frame rate of 5fps upto its max possible) : ")
frame = 5
"""print('Use UP,DOWN,RIGHT and LEFT arroy keys to play')
if input("Enter 'Y' to continue else any other key : ") == 'Y':
	pass
else:
	print('Thanks for playing!!')
	sys.exit()"""
pygame.init()
window = pygame.display.set_mode((600,600))
pygame.display.set_caption("Snake_Game")
fps = pygame.time.Clock()
snake=snake()
food=FOOD([snake])



while True:
	window.fill((0,0,0))

	for i in range(0,601,15):
		pygame.draw.line(window,(30,30,30),(i,0),(i,600))
		pygame.draw.line(window,(30,30,30),(0,i),(600,i))
	food_position=food.food_position
	pygame.draw.circle(window,(0,225,0),(food_position[0],food_position[1]),10)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameOver()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				snake.changeDirTo("R")

			if event.key == pygame.K_LEFT:
				snake.changeDirTo("L")

			if event.key == pygame.K_UP:
				snake.changeDirTo("U")

			if event.key == pygame.K_DOWN:
				snake.changeDirTo("D")

	if snake.move(food):
		snake.snake_score += 10
		food.generate_food([snake])
	

	for pos in snake.snake_body:
		pygame.draw.circle(window,(0,0,225),(pos[0],pos[1]),8)

	pygame.draw.circle(window,(225,0,0),(snake.snake_head[0],snake.snake_head[1]),10)
	snake.check_collison()
	pygame.display.set_caption("WoW Snake | Score: " + str(snake.snake_score))
	pygame.display.flip()
	if frame == 'F':
		fps.tick()
	else:
		fps.tick(int(frame))