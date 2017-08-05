#My Pong Game
#By: James Curley
#7/10/2017
#print ("Hello World!!" + x)


#Importing Everything
import sys
sys.path.append('./')
from pongengine import PongEngine
from controller import FruitController

#Set size of game window
WIDTH = 800
HEIGHT = 600

#Setting Improtant variabales
myPong = PongEngine( WIDTH, HEIGHT, keyboard)
myController = FruitController()
paddleSpeed = 7

#Importing colors and setting backgoround
import colors
myPong.setBackgroundColor(colors.BLUE)

#Making left player
leftPlayer = myPong.makeLeftPaddle(Actor, "left_paddle")

#Making right player
rightPlayer = myPong.makeRightPaddle(Actor, "right_paddle")

#Making ball
ball = myPong.makeBall(Actor, "ball")


#Setting max score
myPong.maxScore = 10

#Everything below here repeats forever

#Handling score
def handleScore():
	if( (myPong.leftScore >= myPong.maxScore) or (myPong.rightScore >= myPong.maxScore) ):
		myPong.isGameOver = True
		
#Handleing Win Screen
def handleWinScreen():
		if( not myPong.isGameOver ):
			return
		if( (myPong.leftScore - myPong.rightScore) > 0 ):
			myPong.displayWinningScreen(screen, "Left Wins!")
		else:
			myPong.displayWinningScreen(screen, "Right Wins!")

#Printing Score
def printScoreOnScreen():
	ls = "SCORE: {0}".format(myPong.leftScore)
	rs = "SCORE: {0}".format(myPong.rightScore)
	myPong.leftScoreText = myPong.font.render(ls, True, myPong.textColor)
	myPong.rightScoreText = myPong.font.render(rs, True, myPong.textColor)
	screen.blit(myPong.leftScoreText, myPong.leftScoreTextPosition )
	screen.blit(myPong.rightScoreText, myPong.rightScoreTextPosition )

#Drawing the screen
def draw():
	myPong.draw(screen)
	myPong.drawSprite(screen, leftPlayer)
	myPong.drawSprite(screen, rightPlayer)
	myPong.drawSprite(screen, ball)
	printScoreOnScreen()
	handleWinScreen()
	
#Updateing the screen
def update():
	myPong.update(keys)
	
	#Left paddle Movement
	#if( myController.isFruitTouched(0) ):
	if( myPong.is_A_pressed() ):
		myPong.lpDirection = myPong.UP
		myPong.lpSpeed = paddleSpeed
	#elif( myController.isFruitTouched(1) ):
	elif( myPong.is_Z_pressed() ):
		myPong.lpDirection = myPong.DOWN
		myPong.lpSpeed = paddleSpeed
	else:
		myPong.lpSpeed = 0
		
	#Right Paddle Movement	
	if( myPong.is_UP_ARROW_pressed() ):
		myPong.rpDirection = myPong.UP
		myPong.rpSpeed = paddleSpeed
	elif( myPong.is_DOWN_ARROW_pressed() ):
		myPong.rpDirection = myPong.DOWN
		myPong.rpSpeed = paddleSpeed
	else:
		myPong.rpSpeed = 0
		
	#Ball Movement
	myPong.moveBallSprite()
	
	#Ball Bouncing
	myPong.calculateCollisions()
	
	handleScore()
