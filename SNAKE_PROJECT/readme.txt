hey in this project i have basically tried to automate snake game with deep learning
*DESCRIPTION*

*Model Inputs* - 48neighbours,food_distance,snakedirection and_food_angle,right, left and ahead obstacle distances

*Model Output* - one for each right ,left and ahead direction 

*Model Training*-basically i first dry run in all the three directions and assing no to all 3dir based on below criteria-

1-if collision then assign -1 to that direction

2-elif snake gets too close to obstacles then assign -0.8

3-if food distance decreases assign 1 to that direction

3-else assign 0 to that direction

if  any two no are same then i have written a function for  that (check out git repository code fore more details)

*MY EXPERIENCE*

i have implemented a looooootof models and it still can improve by more training and everything is automated so you can 
download project and can just run train.....py file it willl resume from same move  and then copy that model to model_to_test 
directory and run test.....mode.py i have also created a ..logic.py file to test my logic you can run that to see my logic 
