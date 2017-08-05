#For reflection calculations, this library may be useful:
#https://github.com/ezag/pyeuclid

import os
import pygame
import random
from gpiozero import LED


class PongEngine:

	windowW=0	#The width and height of the game window
	windowH=0
	
	keyboard = ""
	keys = ""

	graphicExtension = ".png"
	paddleEnglish = 1
	gameSpeed = 4 #Ball Speed
	stopSpeed = 0
	UP = -1
	DOWN = 1
	backgroundColor = (255,255,255)
	textColor = (128,128,128)
	font = None
	leftScoreText = ""
	rightScoreText = ""
	leftScoreTextPosition = (0,0)
	rightScoreTextPosition = (0,0)
	winText = ""
	winTextPosition = (0,0)
	
	leftScore  = 0
	rightScore = 0
	maxScore = 5
	isGameOver = False

	backgroundMapImageName = "background_map" + graphicExtension
	backgroundMapSprite = False
	bmX = 0
	bmY = 0
	bmW = 0
	bmH = 0
	bmSpeed = 0
	bmDirection = -1

	
	leftPaddleImageName = "left_paddle" + graphicExtension
	leftPaddleSprite = False
	lpX = 0
	lpY = 0
	lpW = 0
	lpH = 0
	lpSpeed = 0
	lpDirection = -1

	rightPaddleImageName = "right_paddle" + graphicExtension
	rightPaddleSprite = False
	rpX = 0
	rpY = 0
	rpW = 0
	rpH = 0
	rpSpeed = gameSpeed + 1
	rpDirection = -1
	
	ballImageName = "ball" + graphicExtension
	ballSprite = False
	bX = 0
	bY = 0
	bW = 0
	bH = 0
	bSpeed = gameSpeed + 1
	bYDirection = -1
	bXDirection = -1
	bSlope = -1
	#bYIntercept = 0
	

	def __init__(self, w, h, keyboard):
		self.windowW = w
		self.windowH = h
		self.keyboard = keyboard
		#print(pygame.font.get_fonts())
		self.font = pygame.font.SysFont(None, 36)
		textWidth = self.font.size("SCORE: 0")[0]
		self.leftScoreTextPosition = ((self.windowW/2) - ((self.windowW/4) + textWidth/2), 20)
		self.rightScoreTextPosition = ((self.windowW/2) + ((self.windowW/4) - textWidth/2), 20)
		self.leftScoreText = self.font.render("SCORE: 0", True, self.textColor)
		self.rightScoreText = self.font.render("SCORE: 0", True, self.textColor)

		self.lpX = 30
		self.lpY = self.windowH / 2
		self.rpX = self.windowW-30
		self.rpY = self.windowH / 2
		self.bY = self.windowH / 2
		self.bX = self.windowW / 2
		self.bYIntercept = self.windowH / 2
		self.restartRound()

	def setBackgroundColor(self,color):
		self.backgroundColor = color

	
	def setTextColor( self, c ):
		self.textColor = c
		#Currently not working because of access to screen variable
		#self.printScoreOnScreen()	#Needed so the screen text changes text immediatly
		
	def setFont( self, f ):
		self.font = pygame.font.SysFont( f, 72)

	def setBackground(self, anActorClass, imageFileName = False ):
		if( imageFileName ):
			self.backgroundMapImageName = imageFileName

		if( os.path.exists("./images/" + self.backgroundMapImageName + self.graphicExtension) ):
			self.backgroundMapSprite = anActorClass(self.backgroundMapImageName)
			self.backgroundMapSprite.topleft = self.bmX,self.bmY
			self.bmH = self.backgroundMapSprite.midtop[1] - self.backgroundMapSprite.midbottom[1]
			self.bmW = self.backgroundMapSprite.midright[0] - self.backgroundMapSprite.midleft[0]

		else:
			print("There is a problem with the name of the image file for your 'Background Map'")
		
		return( self.backgroundMapSprite )		
		
	def makeLeftPaddle( self, anActorClass, imageFileName = False ):
		if( imageFileName ):
			self.leftPaddleImageName = imageFileName

		if( os.path.exists("./images/" + self.leftPaddleImageName + self.graphicExtension) ):
			self.leftPaddleSprite = anActorClass(self.leftPaddleImageName)
			self.leftPaddleSprite.center = self.lpX,self.rpY
			self.lpH = self.leftPaddleSprite.midtop[1] - self.leftPaddleSprite.midbottom[1]
			self.lpW = self.leftPaddleSprite.midright[0] - self.leftPaddleSprite.midleft[0]

		else:
			print("There is a problem with the name of the image file for your 'Left Paddle'")
		
		return( self.leftPaddleSprite )

	def makeRightPaddle( self, anActorClass, imageFileName = False ):
		if( imageFileName ):
			self.rightPaddleImageName = imageFileName
		
		if( os.path.exists("./images/" + self.rightPaddleImageName + self.graphicExtension	) ):
			self.rightPaddleSprite = anActorClass(self.rightPaddleImageName)
			self.rightPaddleSprite.center = self.rpX,self.rpY
			self.rpH = self.rightPaddleSprite.midtop[1] - self.rightPaddleSprite.midbottom[1]
			self.rpW = self.rightPaddleSprite.midright[0] - self.rightPaddleSprite.midleft[0]
		
		else:
			print("There is a problem with the name of the image file for your 'Right Paddle'")

		return( self.rightPaddleSprite )

	def makeBall( self, anActorClass, imageFileName = False ):
		if( imageFileName ):
			self.ballImageName = imageFileName	
		
		if( os.path.exists("./images/" + self.ballImageName  + self.graphicExtension) ):
			self.ballSprite = anActorClass(self.ballImageName)
			self.ballSprite.center = self.bX,self.bY
			self.bH = self.ballSprite.midtop[1] - self.ballSprite.midbottom[1]
			self.bW = self.ballSprite.midright[0] - self.ballSprite.midleft[0]
		
		else:
			print("There is a problem with the name of the image file for your 'Ball'")

		return( self.ballSprite )

	def moveLeftPaddleSprite(self):
		if( (self.lpY > 0 - self.lpH/2) and (self.lpY < self.windowH + self.lpH/2) ):
			self.lpY = self.lpY + (self.lpSpeed * self.lpDirection)
		else:
			self.lpDirection = self.lpDirection * -1
			self.lpY = self.lpY + (self.lpSpeed * self.lpDirection)
			 
		self.leftPaddleSprite.center = self.lpX, self.lpY

	def moveRightPaddleSprite(self):
		if( (self.rpY > 0 - self.rpH/2) and (self.rpY < self.windowH + self.rpH/2) ):
			self.rpY = self.rpY + (self.rpSpeed * self.rpDirection)
		else:
			self.rpDirection = self.rpDirection * -1
			self.rpY = self.rpY + (self.rpSpeed * self.rpDirection)
			 
		self.rightPaddleSprite.center = self.rpX, self.rpY

	def moveBallSprite(self):
		# The ball's Y component - see if it is above the bottom and below the top of the window
		if( (self.bY > 0 - self.bH/2) and (self.bY < self.windowH + self.bH/2) ):
			self.bY = self.bY + self.bSlope  * ( self.bYDirection)
			#self.bY = self.bY + self.bSlope  * (self.bSpeed * self.bYDirection)

		else:
			self.bYDirection = self.bYDirection * -1
			self.bY = self.bY + self.bSlope * (self.bSpeed * self.bYDirection)
			 
		self.ballSprite.center = self.bX, self.bY
		# The ball's X component
		if( (self.bX - self.bW/2 > 0) and (self.bX < self.windowW - self.bW/2) ):
			# Still in play, so keep going
			self.bX = self.bX + (self.bSpeed * self.bXDirection)

		else:
			# A goal has been made, so keep score and restart next round
			if( self.bXDirection < 0 ):
				self.rightScore += 1
				#print("Goal for right!")
				#self.printScoreOnScreen()
				self.restartRound();
			else:
				self.leftScore += 1
				#print("Goal for left!")
				#self.printScoreOnScreen()
				self.restartRound();
				
			self.bXDirection = self.bXDirection * -1
			self.bX = self.bX + (self.bSpeed * self.bXDirection)
					
		self.ballSprite.center = self.bX, self.bY

#	def printScoreOnScreen(self, screen):
#		ls = "SCORE: {0}".format(self.leftScore)
#		rs = "SCORE: {0}".format(self.rightScore)
#		self.leftScoreText = self.font.render(ls, True, self.textColor)
#		self.rightScoreText = self.font.render(rs, True, self.textColor)
#		screen.blit(self.leftScoreText, self.leftScoreTextPosition )
#		screen.blit(self.rightScoreText, self.rightScoreTextPosition )

	def restartRound(self):
		#Position Ball
		self.bX = self.windowW / 2
		self.bY = self.windowH / 2
		# Get some random numbers to spice things up a bit
		r1 = random.random()
		#print(r1)
		if( r1 < 0.5 ):
			self.bYDirection = -1
		else:
			self.bYDirection = 1
		r2 = random.random()
		#print(r2)
		if( r2 < 0.5 ):
			self.bXDirection = -1
		else:
			self.bXDirection = 1
		
		self.bSlope += r2
		#print(self.bSlope)
		#print("---------------")

	def displayWinningScreen(self, screen, winMsg):
		if( self.backgroundMapSprite ):
			self.backgroundMapSprite.draw()

		textWidth = self.font.size( winMsg )[0]
		self.winTextPosition = ( (self.windowW/2-textWidth/2) , self.windowH/2 )		
		self.winText = self.font.render(winMsg, True, self.textColor)
		screen.blit(self.winText, self.winTextPosition )
		#print(winMsg)
		#print(self.isGameOver)

	def isBallYandPaddleYInCommon( self, paddle ):
		paddleTopY = paddle.midtop[1]
		paddleBottomY = paddle.midbottom[1]
		ballTopY = self.ballSprite.midtop[1]
		ballBottomY = self.ballSprite.midbottom[1]
		
		#if( paddleTopY < ballBottomY ):
		#	print("Paddle Top > Ball Bottom");
		
		if( ( paddleTopY < ballBottomY ) and ( paddleBottomY > ballTopY ) ):
			#print("Y in Common! with left")
			return(True)
		else:
			return( False )

	def ballAndLeftPaddleFaceCollide(self):
		#Only when ball going left (direction < 0) and paddle have Y in common

		if( (self.bXDirection < 0) and ( self.isBallYandPaddleYInCommon( self.leftPaddleSprite ) )):
			#Detect when ball hits inside face of left paddle and introduce a little wobble
			insideFaceOfLeftPaddleX = (self.lpX + self.lpW/2)
			leftSideOfBallX = (self.bX - self.bW/2)
			if( ( insideFaceOfLeftPaddleX > leftSideOfBallX )): 
				self.bXDirection = self.bXDirection * -1
				self.bX = self.bX + (self.bSpeed * self.bXDirection)
				self.ballSprite.center = self.bX, self.bY
				# Put a little 'English' on the ball by adjusting slope, only if paddle is moving
				if(self.lpSpeed != self.stopSpeed):
					if( self.lpDirection < 0 ):
						if( self.bSlope < 0 ):
							print("LP English1")
							self.bSlope = self.bSlope + self.paddleEnglish
						else:
							print("LP English2")
							self.bSlope = self.bSlope - self.paddleEnglish
					else:
						if( self.bSlope > 0 ):
							print("LP English3")
							self.bSlope = self.bSlope - self.paddleEnglish
						else:
							print("LP English4")
							self.bSlope = self.bSlope + self.paddleEnglish

	def ballAndRightPaddleFaceCollide(self):
		#Detect when ball hits inside face of right paddle and introduce a little wobble
		if( (self.bXDirection > 0) and ( self.isBallYandPaddleYInCommon( self.rightPaddleSprite ) )):
			insideFaceOfRightPaddleX = (self.rpX - self.rpW/2)
			rightSideOfBallX = (self.bX + self.bW/2)
			# We have a collision
			if( ( rightSideOfBallX > insideFaceOfRightPaddleX )): 
				self.bXDirection = self.bXDirection * -1
				self.bX = self.bX + (self.bSpeed * self.bXDirection)
				self.ballSprite.center = self.bX, self.bY
				# Put a little 'English' on the ball by adjusting slope, only if paddle is moving
				if(self.rpSpeed != self.stopSpeed):
					if( self.rpDirection < 0 ):
						if( self.bSlope < 0 ):
							print("RP English1")
							self.bSlope = self.bSlope + self.paddleEnglish
						else:
							print("RP English2")
							self.bSlope = self.bSlope - self.paddleEnglish
							
					else:
						if( self.bSlope > 0 ):
							print("RP English3")
							self.bSlope = self.bSlope + self.paddleEnglish
						else:
							print("RP English4")
							self.bSlope = self.bSlope + self.paddleEnglish 
					 
	def calculateCollisions(self):
		# Simple Math solution - need to implement 2D Vectors and reflection
		#ballPaddleFaceCollide( self.ballSprite, self.rightPaddleSprite, "R" )
		if(self.ballSprite):
			if( self.leftPaddleSprite ):
				self.ballAndLeftPaddleFaceCollide( )
			if( self.rightPaddleSprite ):
				self.ballAndRightPaddleFaceCollide( )

		
	def is_A_pressed(self):
		if( self.keyboard[self.keys.A] ):
			return(True)
		else:
			return(False)

	def is_Z_pressed(self):
		if( self.keyboard[self.keys.Z] ):
			return(True)
		else:
			return(False)

	def is_UP_ARROW_pressed(self):
		if( self.keyboard[self.keys.UP] ):
			return(True)
		else:
			return(False)

	def is_DOWN_ARROW_pressed(self):
		if( self.keyboard[self.keys.DOWN] ):
			return(True)
		else:
			return(False)


	def getUserInput(self):
		#Left Paddle
		if( self.keyboard[self.keys.A] ):
			self.lpDirection = -1
			self.lpSpeed = self.gameSpeed
		elif( self.keyboard[self.keys.Z] ):
			self.lpDirection = 1
			self.lpSpeed = self.gameSpeed
		else:
			self.lpSpeed = self.stopSpeed
		#Right Paddle two player mode
		if( self.keyboard[self.keys.UP] ):
			self.rpDirection = -1
			self.rpSpeed = self.gameSpeed
		elif( self.keyboard[self.keys.DOWN] ):
			self.rpDirection = 1
			self.rpSpeed = self.gameSpeed
		else:
			self.rpSpeed = self.stopSpeed

	def drawSprite(self, screen, sprite):
		if( not self.isGameOver ):
			if( sprite ):
				sprite.draw()
	
	def draw(self, screen):
		screen.clear()
		screen.fill(self.backgroundColor)
		if( not self.isGameOver ):
			if( self.backgroundMapSprite ):
				self.backgroundMapSprite.draw()
			#if( self.leftPaddleSprite ):
			#	self.leftPaddleSprite.draw()
			#if( self.rightPaddleSprite ):
			#	self.rightPaddleSprite.draw()
			#if( self.ballSprite ):
			#	self.ballSprite.draw()

			#self.printScoreOnScreen(screen)
		else:
			pass
			#The game has ended, so show a new screen.
			#if( (self.leftScore - self.rightScore) > 0 ):
			#	self.displayWinningScreen(screen, "Left Wins!")
			#else:
			#	self.displayWinningScreen(screen, "Right Wins!")
			

	def update(self, keys):
		#pass
		self.keys = keys
		#self.getUserInput()
		if( not self.isGameOver ): 
			if( self.leftPaddleSprite ):
				self.moveLeftPaddleSprite()
			if(self.rightPaddleSprite):
				self.moveRightPaddleSprite() 
			#if(self.ballSprite):
			#	self.moveBallSprite()         # Also calculates score
			#self.calculateCollisions()
			# Check for Winning Condition, and show win screen, if appropriate
			#if( (self.leftScore >= self.maxScore) or (self.rightScore >= self.maxScore) ):
			#	self.isGameOver = True

		
