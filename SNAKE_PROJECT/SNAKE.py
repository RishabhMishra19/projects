import numpy as np

class snake:
	def __init__(self):
		x,y=np.random.randint(4,35)*15,np.random.randint(4,35)*15
		self.snake_head=[x,y]
		self.snake_body=[[x-i,y] for i in range(15,16,15)]
		self.snake_direction=['R','L','U','D'][np.random.randint(4)]
		self.snake_score=0
		


	def restart_snake(self):
		x,y=np.random.randint(4,35)*15,np.random.randint(4,35)*15
		self.snake_head=[x,y]
		self.snake_body=[[x-i,y] for i in range(15,16,15)]
		self.snake_direction=['R','L','U','D'][np.random.randint(4)]
		self.snake_score=0


	def move(self,food):
		self.snake_body.insert(0,self.snake_head[:])
		if self.snake_direction=='R':
			self.snake_head[0]+=15
		if self.snake_direction=='L':
			self.snake_head[0]-=15
		if self.snake_direction=='U':
			self.snake_head[1]-=15
		if self.snake_direction=='D':
			self.snake_head[1]+=15
		
		if  self.snake_head!=food.food_position:
			self.snake_body.pop()
			return 0
		else:
			return 1

	def changeDirTo(self,dir):
		if dir=="R" and not self.snake_direction=="L":
			self.snake_direction="R"

		if dir=="L" and not self.snake_direction=="R":
			self.snake_direction="L"

		if dir=="U" and not self.snake_direction=="D":
			self.snake_direction="U"

		if dir=="D" and not self.snake_direction=="U":
			self.snake_direction="D"

	def check_collison(self):
		if self.snake_head[0]<15 or self.snake_head[0]>585 or self.snake_head[1]<15 or self.snake_head[1]>585:
			return 1
		for body_part in self.snake_body:
			if body_part==self.snake_head:
				return 1
		return 0

	#now lets make my_logic
	def relative_to_actual(self,k):
		a=np.array(['R','L','A'])# 'R'-right relative to snakes moving direction,'L'-left relative to snakes moving direction and "A"-ahead means its own moving direction
		i = np.where(a == k)[0][0]
		if self.snake_direction=='R':
			actual_dir=['D','U','R'][i]
		elif self.snake_direction=='L':
			actual_dir=['U','D','L'][i]
		elif self.snake_direction=='U':
			actual_dir=['R','L','U'][i]
		else:
			actual_dir=['L','R','D'][i]
		return actual_dir

	#this function will calculate food distance from snake's head and angle between snake's direction and a default direction and 
	def get_food_angle_and_distance(self,food):
		def angle(p1,p2):
			x = p2[0] - p1[0]
			y = p2[1] - p1[1]#because y is opposite (downward)
			anngle_ = np.arctan2(y,x)
			if anngle_<0:
				anngle_ += 2*np.pi
			return anngle_

		[shx,shy] = self.snake_head
		[fx,fy] = food
		af = angle([shx,shy],[fx,fy])
		sec = {'R':0,'L':np.pi,'U':3/2*np.pi,'D':np.pi/2}
		ad = sec[ self.snake_direction ]
		af = af - ad
		ad = ad - ad
		if af <-np.pi:
			af = 2*np.pi + af
		angle = af/(np.pi)#to normalize
		food_distance = np.linalg.norm( np.array([fx-shx,fy-shy]) )/(570*np.sqrt(2))#to normalize we dive by max possible distance
		return angle,food_distance
	

	#second is distance from wall
	def get_wall_obstacle_distance(self):
		[shx,shy] = self.snake_head
		#we will calculate relativedistance from wall according to its currrent direction
		return_dict = dict(
							R = [ 600 - shy , shy - 0 , 600 - shx ],
							L = [ shy - 0 , 600 - shy , shx - 0 ],
							U = [ 600 - shx , shx - 0 , shy - 0 ],
							D = [ shx - 0 , 600 - shx , 600 - shy ]
							)
		return np.array( return_dict[self.snake_direction] )/570# we did division to normalize

	#third is distance from its own body
	#this will calculate obstacle distance in three snake's right,snake's left and snake's ahead direction
	#obstacles are of two types first its own body and second walls of the ground
	def get_body_obstacle_distance(self):
		[x,y] = self.snake_head

		x_body , y_body = np.array(self.snake_body)[:,0] , np.array(self.snake_body)[:,1]#x and y coordinates of the whole body

		x_body_obstacles , y_body_obstacles = [[x-570,y]] , [[x,y-570]]

		#checking if any snake's bodypart is present in plus (passing through snake's head) or not
		x_indexes , y_indexes = np.where(x_body == x)[0] , np.where(y_body == y)[0]

		y_obstacles , x_obstacles = np.array(self.snake_body)[x_indexes] , np.array(self.snake_body)[y_indexes]

		if len(y_obstacles) > 0 : y_body_obstacles.extend( y_obstacles )
		if len(x_obstacles) > 0 : x_body_obstacles.extend( x_obstacles )

		y_body_obstacles.append([x,y+570])
		x_body_obstacles.append([x+570,y])

		y_body_obstacles = np.array( y_body_obstacles )
		x_body_obstacles = np.array( x_body_obstacles )

		y_body_obstacles[:,1] = sorted( y_body_obstacles[:,1] )
		x_body_obstacles[:,0] = sorted( x_body_obstacles[:,0] )
		
		#next task is to seperate snake's rigth,left,up and down body obstacles,these will be already sorted(ascending) so later we wont need to do extra for finding nearest obstacle
		right_indexes = np.where( x_body_obstacles[:,0] >= x )[0]
		left_indexes = np.where( x_body_obstacles[:,0] < x )[0]
		down_indexes = np.where( y_body_obstacles[:,1] >= y )[0]
		up_indexes = np.where( y_body_obstacles[:,1] < y )[0]

		#next task is to seperate right,left and ahead body_obstacles
		if self.snake_direction == 'R':
			right_obstacle = y_body_obstacles[ down_indexes ][0] # as in sorted coordinates first will be closest
			left_obstacle = y_body_obstacles[ up_indexes ][-1] # last will be closest
			ahead_obstacle = x_body_obstacles[ right_indexes ][0] # first wil be closest

		elif self.snake_direction == 'L':
			right_obstacle = y_body_obstacles[ up_indexes ][-1] # as in sorted coordinates last will be closest
			left_obstacle = y_body_obstacles[ down_indexes ][0] # first will be closest
			ahead_obstacle = x_body_obstacles[ left_indexes ][-1] # last will be closest

		elif self.snake_direction == 'U':
			right_obstacle = x_body_obstacles[ right_indexes ][0] # as in sorted coordinates first will be closest
			left_obstacle = x_body_obstacles[ left_indexes ][-1] # last will be closest
			ahead_obstacle = y_body_obstacles[ up_indexes ][-1] # last will be closest
		else:
			right_obstacle = x_body_obstacles[ left_indexes ][-1] # as in sorted coordinates last will be closest
			left_obstacle = x_body_obstacles[ right_indexes ][0] # first will be closest
			ahead_obstacle = y_body_obstacles[ down_indexes ][0] # first will be closest

		#now we got the nearest body obstacle coordinate in all three right,left and ahead directions next we we will find distance between them and snake head and returns them
		sh = np.array([x,y])
		right_body = np.linalg.norm( right_obstacle - sh )/570#we divide by 570 (max possible distance between body and head) to normalize it
		left_body = np.linalg.norm( left_obstacle - sh )/570
		ahead_body = np.linalg.norm( ahead_obstacle - sh )/570

		return right_body,left_body,ahead_body 

	
	def cal_food_wall_dis(self,food):
		[fx,fy] = food.food_position
		l,r,u,d = fx-0 , 600-fx , fy-0 , 600-fy
		return min([l,r,u,d])

	#this is my main logic
	def my_logic(self,food):
		[shx,shy] = self.snake_head
		body = [i for i in self.snake_body]
		direction = self.snake_direction
		_,fd = self.get_food_angle_and_distance(food.food_position)
		br,bl,ba = self.get_body_obstacle_distance()
		wr,wl,wa = self.get_wall_obstacle_distance()

		wd = wr + wl + wa
		bd = br + bl + ba		
		
		#Task 2 : for move one by one in all three direction and store score,food,body,wall distance and  collision status
		collisions = []
		scores = []
		fds = []
		bds = []
		wds = []
		oa = []
		dir_ = ['R','L','A']
		for d in dir_:
			self.snake_direction = self.relative_to_actual(d)#set snakes direction to that direction
			if self.move(food):# then we move and if it s 1(means food taken) thne score increases then assign scores = 1 else 0
				scores.append(1)
			else:#if score not increases then we check collision
				scores.append(0)
			if self.check_collison():#if collision then append 1 else 0
				collisions.append(1)
			else:
				collisions.append(0)
			_,cfd = self.get_food_angle_and_distance(food.food_position)
			fds.append(cfd - fd)
			cbr,cbl,cba = self.get_body_obstacle_distance()
			bds.append((cbr + cbl + cba) - bd)
			cwr,cwl,cwa = self.get_wall_obstacle_distance()
			wds.append((cwr + cwl + cwa) - wd)
			cfwd = self.cal_food_wall_dis(food)
			if (cba*570 < 30 or cbr*570 < 30 or cbl*570 < 30 or cwa*585 < 30 or cwr*585 < 30 or cwl*585 < 30)  and not cfwd <=15:
				oa.append(1)
			else:
				oa.append(0)
			#now reset snakes attributes back to its normal position which changes due to dry run
			self.snake_head = [shx,shy] 
			self.snake_body = [i for i in body] 
			self.snake_direction = direction 

		#Task 3 : based on these observations we will obtain whether this direction right or not
		right_direction = []
		for i in range(3):
			if collisions[i]:#if collision then completely wrong direction means -1
				right_direction.append(-1)
			elif oa[i] :
				right_direction.append(-0.8)
			elif fds[i] < 0 :
				right_direction.append(1)
			else:
				right_direction.append(0)
		right_direction = self.deal_with_same( right_direction,bds,wds )
		inn = np.argmax(right_direction)
		
		return self.relative_to_actual(['R','L','A'][inn]),np.array(right_direction).reshape(1,-1)

			#this funvtion is for dealing with same right direction  no which we get from my_predict
	#if two are same then will increase the one where bd increases more else according to  where wds more increases
	def deal_with_same(self,rd,bds,wds):
		one = np.where(np.array(rd) == 1)[0]
		if len(one)>1:
			first = one[0]
			second = one[1]
			if bds[first] > bds[second]:
				rd[second] -= 0.25
			elif bds[first] < bds[second]:
				rd[first] -= 0.25
			elif wds[first] > wds[second]:
				rd[second] -= 0.25
			else:
				rd[first] -= 0.25
		else:
			zero = np.where(np.array(rd) == 0)[0]
			if len(zero)>1:
				first = zero[0]
				second = zero[1]
				if bds[first] > bds[second]:
					rd[second] -= 0.25
				elif bds[first] < bds[second]:
					rd[first] -= 0.25
				elif wds[first] > wds[second]:
					rd[second] -= 0.25
				else:
					rd[first] -= 0.25
		other_than_minus_one = np.where(np.array(rd) == -0.8)[0]
		if len(other_than_minus_one)>1:
			first = other_than_minus_one[0]
			second = other_than_minus_one[1]
			if bds[first] > bds[second]  or wds[first] > wds[second]:
				rd[first] += 0.25
			elif bds[first] < bds[second]  or wds[first] < wds[second]:
				rd[second] += 0.25
		return rd


	#this returns input for model basically (-3,+3) range from its head relative to its direction and food distance and food angle relative to direction
	#we give input relative to direction so output also will be relative to direction
	def get_input_for_model(self,food):

		fa,fd = self.get_food_angle_and_distance(food.food_position)
		[shx,shy] = self.snake_head
		[fx,fy] = food.food_position
		dir_ = self.snake_direction
		br,bl,ba = self.get_body_obstacle_distance()
		wr,wl,wa = self.get_wall_obstacle_distance()

		k = [fa,fd,br,bl,ba,wr,wl,wa]

		if dir_ == 'R':
			for i in range(shx+45,shx-46,-15):
				for j in range(shy-45,shy+46,15):
					if i == shx and j == shy:
						pass
					elif [i,j] in self.snake_body:
						k.append(-1)
					elif i == fx and j == fy:
						k.append(1)
					else:
						k.append(0)

		elif dir_ == 'U':
			for j in range(shy-45,shy+46,15):
				for i in range(shx-45,shx+46,15):
					if i == shx and j == shy:
						pass
					elif [i,j] in self.snake_body:
						k.append(-1)
					elif i == fx and j == fy:
						k.append(1)
					else:
						k.append(0)

		elif dir_ == 'L':
			for i in range(shx-45,shx+46,15):
				for j in range(shy+45,shy-46,-15):
					if i == shx and j == shy:
						pass
					elif [i,j] in self.snake_body:
						k.append(-1)
					elif i == fx and j == fy:
						k.append(1)
					else:
						k.append(0)

		elif dir_ == 'D':
			for j in range(shy+45,shy-46,-15):
				for i in range(shx+45,shx-46,-15):
					if i == shx and j == shy:
						pass
					elif [i,j] in self.snake_body:
						k.append(-1)
					elif i == fx and j == fy:
						k.append(1)
					else:
						k.append(0)

		return k




 