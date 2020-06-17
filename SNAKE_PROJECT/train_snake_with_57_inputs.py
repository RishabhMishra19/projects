import numpy as np
import pygame
import sys
from SNAKE import snake
from FOOD import FOOD
from MODEL import MODEL



#this is gameover which triggers when we quit the game it will save that model so thta we can resume that in next training session thus we dont need to start everytim from
#zero and we can train our model whenever we want to
def gameOver(model,l,Move):
	with open(f'MOVES/model_{l}.txt','w') as file:
		file.write(str(Move))
	model.save()
	pygame.quit()
	sys.exit()


pygame.init()
window = pygame.display.set_mode((600,600))
pygame.display.set_caption("Snake_Game")
fps = pygame.time.Clock()
snakes=[snake() for i in range(1)]
food=FOOD(snakes)
Model = MODEL(57,[20,10],3)
Model.load()
model = Model.model

#move is responsible for snakes move (for tracking down the count training examples )
LAYERS = '[57][20,10][3]'

try:
	with open(f'MOVES/model_{LAYERS}.txt','r') as file:
		move = int(file.read())
except:
	move = 0



while True:
	move = move + 1
	if move%200 == 0:
		Model.save()
	window.fill((0,0,0))

	for i in range(0,601,15):
		pygame.draw.line(window,(30,30,30),(i,0),(i,600))
		pygame.draw.line(window,(30,30,30),(0,i),(600,i))
	food_position=food.food_position
	pygame.draw.circle(window,(0,225,0),(food_position[0],food_position[1]),10)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameOver(Model,LAYERS,move)

	for snake in snakes:
		my_prd_dir , my_out = snake.my_logic(food)
		mod_inp = np.array(snake.get_input_for_model(food)).reshape(1,-1)
		prd_dir = model.predict( mod_inp )
		mod_prd_dir = snake.relative_to_actual( ['R','L','A'][np.argmax(prd_dir[0])] )
		model.fit(  mod_inp , my_out , verbose = 0 ,epochs = 5 )
		
		snake.changeDirTo( mod_prd_dir )
		if snake.move(food):
			snake.snake_score = snake.snake_score + 10
			food.generate_food(snakes)
		
		for pos in snake.snake_body:
			pygame.draw.circle(window,(0,0,225),(pos[0],pos[1]),8)

		pygame.draw.circle(window,(225,0,0),(snake.snake_head[0],snake.snake_head[1]),10)
		if snake.check_collison():
			snake.restart_snake()
	SCORES = [snake.snake_score for snake in snakes]
	pygame.display.set_caption("WoW Snake | SCORES: " + str(SCORES) + " | MOVE: " + str(move))
	pygame.display.flip()
	fps.tick()
	