import numpy as np
import pygame
import sys
import os
import keras
from SNAKE import snake
from FOOD import FOOD
		

def gameOver():
	pygame.quit()
	sys.exit()



#frame = input("Enter frame rate(for speed)\n(Enter 'F' for full speed)\n(You may start with a frame rate of 5fps upto its max possible) : ")
frame = 'F'


try:
	files = os.listdir('MODEL_TO_TEST/')
	for file in files:
		if file.endswith(".json"):
			json = file
		if file.endswith(".h5"):
			h5 = file

	with open('MODEL_TO_TEST//'+json,'r') as load:
		model_json=load.read()
	model=keras.models.model_from_json(model_json)
	model.load_weights( 'MODEL_TO_TEST//' + h5 ) 
	model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
	print("model loaded successfully")
except:
	print('model not found!')
	sys.exit()


pygame.init()
window = pygame.display.set_mode((600,600))
pygame.display.set_caption("Snake_Game")
fps = pygame.time.Clock()
snake=snake()
food=FOOD([snake])


while True:
	window.fill((0,0,0))
	shx,shy = snake.snake_head[0],snake.snake_head[1]
	fx,fy = food.food_position[0] , food.food_position[1]
	pygame.draw.rect(window,(10,10,10),(shx-45,shy-45,90,90))

	for i in range(0,601,15):
		pygame.draw.line(window,(30,30,30),(i,0),(i,600))
		pygame.draw.line(window,(30,30,30),(0,i),(600,i))


	pygame.draw.line(window,(60,0,0),(shx,shy),(fx,fy),3)

	dx = { 'R':600 , 'L':0 , 'U':shx , "D":shx }[snake.snake_direction]
	dy = { 'R':shy , 'L':shy , 'U':0 , "D":600 }[snake.snake_direction]
	pygame.draw.line(window,(60,0,0),(shx,shy),(dx,dy),3)

	food_position=food.food_position
	pygame.draw.circle(window,(0,225,0),(fx,fy),10)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameOver()
	mod_inp = np.array(snake.get_input_for_model(food)).reshape(1,-1)
	sec = {'R':0,'L':np.pi,'D':3/2*np.pi,'U':np.pi/2}
	strt = sec[ snake.snake_direction ]
	stp =strt +  ( -mod_inp[0][0]*np.pi)
	#print(strt*180/np.pi,stp*180/np.pi,mod_inp[0][0]*180/np.pi)
	if strt > stp:
		lll = stp
		stp = strt
		strt = lll

	pygame.draw.arc(window,(0,60,0),[shx-30,shy-30,70,70],strt,stp,3)
	prd_dir = model.predict( mod_inp )
	mod_prd_dir = snake.relative_to_actual( ['R','L','A'][np.argmax(prd_dir[0])] )
	snake.changeDirTo( mod_prd_dir )
	if snake.move(food):
		snake.snake_score = snake.snake_score + 10
		food.generate_food([snake])
	for pos in snake.snake_body:
		pygame.draw.circle(window,(0,0,225),(pos[0],pos[1]),8)

	
	pygame.draw.circle(window,(225,0,0),(shx,shy),10)
	
	
	

	if snake.check_collison():
		snake.restart_snake()
	pygame.display.set_caption("WoW Snake | Testing | Score: " + str(snake.snake_score))
	pygame.display.flip()
	if frame == 'F':
		fps.tick()
	else:
		fps.tick(int(frame))