import keras
from keras.layers import Dense

 
#Model class do all the task we just need to call its attributes
class MODEL:
	#init will set the no of layers and sets its name so that during loading we know which model we are talking about  
	def __init__(self,I,H,O): 
		self.I = I
		self.H = H
		self.O = O
		self.name = f'model_[{I}][{H}][{O}]'
		
	#save will save the model as during creation in init we already setted its name
	def save(self):
		model_json=self.model.to_json()
		with open(f'MODELS_TRAINED/{self.name}.json','w') as save_model:
			save_model.write(model_json)
		self.model.save_weights(f'MODELS_TRAINED/{self.name}.h5')
		print('saved successfully')

	#load will load the respective model if exist as we already know its names else create this model 
	def load(self):
		try:
			with open(f'MODELS_TRAINED/{self.name}.json','r') as load:
				model_json=load.read()
			model=keras.models.model_from_json(model_json)
			model.load_weights(f'MODELS_TRAINED/{self.name}.h5') 
			model.compile(loss='mean_squared_error',optimizer='adam',metrics=['accuracy'])
			self.model = model
			print("loaded successfully")
		except:
			model = keras.models.Sequential()	
			model.add(Dense( self.I , activation = 'relu' ))
			for i in self.H:
				model.add(Dense( i , activation = 'relu' ))
			model.add(Dense( self.O , activation = 'linear' ))
			model.compile(loss='mean_squared_error',optimizer='adam',metrics=['accuracy'])
			self.model = model
			print("created successfully")
