from gpiozero import Button
from time import sleep

class FruitController:

	fruit0 = Button(17, bounce_time=0.01)
	fruit1 = Button(27)
	fruit2 = Button(22)
	fruit3 = Button(23)
	fruit4 = Button(24)

	def isFruitTouched( self, pad ):
		if( pad == 0):
			return( self.fruit0.is_pressed )
		if( pad == 1):
			return( self.fruit1.is_pressed )
		if( pad == 2):
			return( self.fruit2.is_pressed )
		if( pad == 3):
			return( self.fruit3.is_pressed )
		if( pad == 4):
			return( self.fruit4.is_pressed )

	

