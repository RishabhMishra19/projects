import random

#food class do all the work we just need to call its respective attributes 
class FOOD:
	#in takes it takes snakes so that food will not be set on any snake's head or on its body
	def __init__(self,snakes):
		snake_part=[]
		for snake in snakes:
			snake_part.append(snake.snake_head)
			snake_part.extend(snake.snake_body)
		while True:
			self.food_position=[ random.randrange(15,600,15) , random.randrange(15,600,15) ]
			if self.food_position not in snake_part:
				break

	#whenever any snake eats food we need to again generate food (again not on any snake's head or on its body thts why it requires snakes)
	def generate_food(self,snakes):
		snake_part=[]
		for snake in snakes:
			snake_part.append(snake.snake_head)
			snake_part.extend(snake.snake_body)
		while True:
			self.food_position=[ random.randrange(15,600,15) , random.randrange(15,600,15) ]
			if self.food_position not in snake_part:
				break

