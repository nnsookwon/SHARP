import pygame
from random import randint
import menu
import time
import math

class Player(pygame.sprite.Sprite):

	def __init__(self, image, pos, step):
		pygame.sprite.Sprite.__init__(self) #Sprite initializer
		self.image = image
		self.area = pygame.display.get_surface().get_rect()
		self.rect = self.image.get_rect()
		self.rect.topleft = pos #(x_pos, y_pos)
		self.dx = 0
		self.dy = 0
		self.step = step
		self.hasBall = False
		self.facingRight = True

	def flip(self):
		self.facingRight = not self.facingRight
		self.image = pygame.transform.flip(self.image, True, False)

	def update(self):
		self.move()

	def move(self):
		newPos = self.rect.move((self.dx, self.dy))
		for sprite in allsprites: #prevent sprite collision
			if sprite is not self and \
			newPos.colliderect(sprite.rect):
			#	if self.hasBall and sprite is ball:
			#		continue
				return
		if self.area.contains(newPos) and \
		field.contains(newPos):
			self.rect = newPos

class Opponent(pygame.sprite.Sprite):

	def __init__(self, image, pos, isMoving = False,
				range_y=0, step=0):
		"""
		Default Opponent is a static defender.
		Specify isMoving=True and the min/max y position 
		for Opponent to move up and down (e.g. a goalie)
		"""

		pygame.sprite.Sprite.__init__(self) #Sprite initializer
		self.image = image
		self.area = pygame.display.get_surface().get_rect()
		self.rect = self.image.get_rect()
		self.rect.center = pos #(x_pos, y_pos)
		self.dx = 0
		self.dy = step
		self.isMoving = isMoving
		self.max_y = pos[1] + range_y
		self.min_y = pos[1] - range_y
		self.step = step

	def update(self):
		if self.isMoving:
			self.move()

	def move(self):
		newPos = self.rect.move((self.dx, self.dy))
		for sprite in allsprites: #prevent sprite collision
			if sprite is not self and \
				newPos.colliderect(sprite.rect):
				return
		self.rect = newPos
		if self.rect.bottom > self.max_y or \
			self.rect.top < self.min_y:
			#change direction
			self.dy *= -1
		
class Ball(pygame.sprite.Sprite):
	
	def __init__(self, image, pos, field):
		pygame.sprite.Sprite.__init__(self) #Sprite initializer
		self.image = image
		self.area = field #rect
		self.rect = self.image.get_rect()
		self.rect.topleft = pos #(x_pos, y_pos)
		self.dx = 0
		self.dy = 0
		self.speed = 0
		self.angle = 0
		self.isShot = False

	def reset(self):
		self.dx = 0
		self.dy = 0
		self.speed = 0
		self.angle = 0

	def update(self):
		self.move()
		if self.isShot:
			self.speed *= 0.95

	def setPosition(self, x_center, y_center):
		newPos = self.rect.copy()
		newPos.centery = y_center
		newPos.centerx = x_center
		for sprite in allsprites:
			if sprite is not self and sprite is not player and \
			newPos.colliderect(sprite.rect):
				return
		if self.area.contains(newPos):
			self.rect = newPos

	def move(self):
		if self.isShot:
			self.dx = self.speed * math.cos(self.angle)
			self.dy = self.speed * math.sin(self.angle)
			
			if self.angle % math.pi != 0 and (math.fabs(self.dx) < 2 or math.fabs(self.dy) < 2):
				self.dx = self.dy = 0
				self.isShot = False
				self.speed = 0
				return
		newPos = self.rect.move((self.dx, self.dy))
		
		for sprite in allsprites: #prevent sprite collision
			if sprite is not self and \
			newPos.colliderect(sprite.rect):
				#player.hasBall = False
				if not self.isShot:
					self.reset()
				#bounce off collision
				if self.isShot:
					if newPos.right - self.dx <= sprite.rect.left or \
						newPos.left - self.dx >= sprite.rect.right:
						self.angle = math.pi - self.angle
					if newPos.bottom - self.dy <= sprite.rect.top or \
						newPos.top - self.dy >= sprite.rect.bottom:
						self.angle *= -1
					self.speed *= 0.70
				return
					
		if self.area.contains(newPos) or \
			(goal.collidepoint(newPos.bottomright) and \
			goal.collidepoint(newPos.topright) and \
			not player.hasBall):
			#Player can NOT "walk" ball into goal
			self.rect = newPos
		else:
			if self.isShot:
				#bounce off collision
				if newPos.right >= self.area.right or \
					newPos.left <= self.area.left:
					self.angle = math.pi - self.angle
					#self.speed = 0
				if newPos.bottom >= self.area.bottom or \
					newPos.top <= self.area.top:
					self.angle *= -1
				self.speed *= 0.75

def randomPos(x_min, x_max, y_min, y_max):
	return (randint(x_min, x_max), randint(y_min, y_max))

def drawField():
	screen.fill(GREEN)
	pygame.draw.rect(screen, BLUE, goal, 3)
	pygame.draw.rect(screen, BLACK, field, 1)
	pygame.draw.rect(screen, BLACK, penalty_box, 1 )

def addOpponent(x, y, isMoving=False, range_y=0, step=0):
	opponent = Opponent(opponent_img, (x, y), isMoving, 
		range_y, step)
	allsprites.add(opponent)
	opponentsprites.add(opponent)

def initLevel(levelChoice):
	level = levelChoice + 1; #0 index in list 
	if level <= 1:
		return
	
	if level >= 2:
		addOpponent(FIELD_WIDTH - PLAYER_WIDTH, field.centery, 
				True, GOAL_HEIGHT/2 + 20, 5)
	if level == 3:
		addOpponent(300, DISPLAY_HEIGHT/2)
		addOpponent(510, DISPLAY_HEIGHT/2 + 150)
		addOpponent(510, DISPLAY_HEIGHT/2 - 150)
		addOpponent(700, DISPLAY_HEIGHT/2)
	if level == 4:
		addOpponent(300, DISPLAY_HEIGHT/2, True, 200, 3)
		addOpponent(510, DISPLAY_HEIGHT/2 + 150)
		addOpponent(510, DISPLAY_HEIGHT/2 - 150)
		addOpponent(700, DISPLAY_HEIGHT/2, True, 200, 7)


pygame.init()

DISPLAY_WIDTH = 1080
DISPLAY_HEIGHT = 640

GOAL_WIDTH = 70 	
GOAL_HEIGHT = 200

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 50

BALL_WIDTH = 30
BALL_HEIGHT = 30

FIELD_WIDTH = DISPLAY_WIDTH - GOAL_WIDTH
FIELD_HEIGHT = DISPLAY_HEIGHT - 2*(PLAYER_HEIGHT - BALL_HEIGHT)

PENALTY_BOX_WIDTH = FIELD_WIDTH/2
PENALTY_BOX_HEIGHT = FIELD_HEIGHT - 100

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

MENU_OPTIONS = ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Quit']

#FOR FULLSCREEN
#screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("SHARP")

gameIsRunning = True

field = pygame.Rect( 0, PLAYER_HEIGHT - BALL_HEIGHT, \
					 FIELD_WIDTH, \
 					 FIELD_HEIGHT)

penalty_box = pygame.Rect( (DISPLAY_WIDTH - PENALTY_BOX_WIDTH - GOAL_WIDTH), \
						   (DISPLAY_HEIGHT - PENALTY_BOX_HEIGHT)/2, \
						    PENALTY_BOX_WIDTH, PENALTY_BOX_HEIGHT)

player_img = pygame.image.load('player.png').convert_alpha()
#player_img.set_colorkey(WHITE)
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
player = Player(player_img, (50,50), 10)

ball_img = pygame.image.load('ball.png').convert_alpha()
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))
ball = Ball(ball_img, (150,200), field)

goal = pygame.Rect(  DISPLAY_WIDTH - GOAL_WIDTH, \
			  		(DISPLAY_HEIGHT - GOAL_HEIGHT)/2, \
			  		 GOAL_WIDTH, GOAL_HEIGHT )

opponent_img = pygame.image.load('opponent.png').convert_alpha()
opponent_img = pygame.transform.scale(opponent_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
opponent_img  = pygame.transform.flip(opponent_img, True, False)


opponentsprites = pygame.sprite.Group()
allsprites = pygame.sprite.Group((player, ball))


pygame.display.update()
clock = pygame.time.Clock()

def mainMenu():
	global gameIsRunning

	screen.fill(BLUE)
	menu_choice = menu.menu(screen, MENU_OPTIONS, DISPLAY_WIDTH/2 - 80,
	DISPLAY_HEIGHT/2 - 150,None,64,0.9,GREEN,RED)

	if menu_choice == len(MENU_OPTIONS)-1:
		gameIsRunning = False

	initLevel(menu_choice)

def playGame():	
	global player, ball, opponentsprites, allsprites, gameIsRunning

	gameIsRunning = True
	player = Player(player_img, (50,50), 10)
	ball = Ball(ball_img, (150,200), field)
	opponentsprites = pygame.sprite.Group()
	allsprites = pygame.sprite.Group((player, ball))
	mainMenu()

	screen.fill(GREEN)

	try:
		while gameIsRunning:

			keys_pressed = pygame.key.get_pressed()
			if keys_pressed[pygame.K_SPACE] and \
				player.hasBall:
				#hold spacebar to build up power and kick further
				#implement later to correspond to force sensor feedback
				ball.speed += 1
				print ball.speed
				if ball.speed > 50:
					ball.speed = 50 
					print "max speed"
		
			for event in pygame.event.get():
				#controlling with keys
				#w,a,s,d keys = movement
				#space bar = shoot
				#mouse = direction/angle
				
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						gameIsRunning = False
						playGame()
						break
					if event.key == pygame.K_a:
						player.dx = -player.step
					if event.key == pygame.K_d:
						player.dx = player.step
					if event.key == pygame.K_w:
						player.dy = -player.step    
					if event.key == pygame.K_s:
						player.dy = player.step
					if event.key == pygame.K_LSHIFT:
						player.flip()


					"""
					*************AIMING WITH ARROWS**************
					*********INCREMENTS OF 30 DEGREES************
					"""
					if event.key == pygame.K_UP:
						ball.angle = ball.angle - math.pi/6
						ball.angle = -math.pi/2 if ball.angle < -math.pi/2 \
									else ball.angle
						#"reversed" because top y-position is 0, so positive is downwards
					if event.key == pygame.K_DOWN:
						ball.angle = ball.angle + math.pi/6
						ball.angle = math.pi/2 if ball.angle > math.pi/2 \
									else ball.angle
						
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_a or \
						event.key == pygame.K_d:
						player.dx = 0
					if event.key == pygame.K_w or \
						event.key == pygame.K_s:
						player.dy = 0
					if event.key == pygame.K_SPACE and \
						player.hasBall and player.facingRight:
						if penalty_box.collidepoint(player.rect.bottomleft):
							#player within penalty box and can shoot
							player.hasBall = False		
							ball.isShot = True			
							print ball.speed #for debugging purposes
							ball.move() #to "break" away from player 
						else:
							ball.speed = 0
						"""
						***********AIMING WITH MOUSE****************
						**********FREE RANGE OF SHOOTING************

						#if ball is shot, direction points towards mouse			
						mouseX, mouseY = pygame.mouse.get_pos()
						playerX, playerY = player.rect.bottomright
						aimX = mouseX - playerX
						aimY = mouseY - playerY
						ball.angle = math.atan2(float(aimY), float(aimX))
						#player.image = pygame.transform.rotate(player.image, angle)
						"""

							
				elif event.type == pygame.QUIT:
					gameIsRunning = False
					break
					
				if not gameIsRunning:
					pygame.quit()
					sys.exit()
			
			if player.hasBall: #ball moves with player
				ball.dx = player.dx
				ball.dy = player.dy        
		   
		   	ball.update()
		   	player.update()
			opponentsprites.update()

			#if player.hasBall:
			#	ball.setPosition(player.rect.right + BALL_WIDTH/3*2, player.rect.centery)

		
			if math.fabs(ball.rect.centery - player.rect.centery) <= 10 and \
			(player.facingRight and \
			 math.fabs(ball.rect.left - player.rect.right) <= 20 or \
			 not player.facingRight and \
			 math.fabs(ball.rect.right - player.rect.left) <= 20):
				if not player.hasBall:
					player.hasBall = True
					ball.isShot = False
					ball.reset()
			else:
				player.hasBall = False
				if not ball.isShot:
					ball.reset()


			drawField()
			if player.hasBall and player.facingRight:
				#ball.rect.bottomleft = player.rect.bottomright
				(ball_x, ball_y) = ball.rect.midright
				#draw aiming arrow for shooting direction
				pygame.draw.line(screen, RED, (ball_x, ball_y), \
				 (ball_x + 50*math.cos(ball.angle), ball_y + 50*math.sin(ball.angle)), 4)

			
			allsprites.draw(screen)

			pygame.display.update()

			#check if ball landed in goal or
			#if ball cross goal line
			if not player.hasBall and \
				(goal.contains(ball.rect) or \
			   	(ball.speed < 1 and \
			   	goal.collidepoint(ball.rect.bottomright) and \
				goal.collidepoint(ball.rect.topright))):
				time.sleep(2) #2 second delay
				player.hasBall = False
				ball.dx = 0
				ball.dy = 0
				ball.speed = 0
				while True: 
					#repeat if new ball position overlaps Player
					#new position in left half of the screen
					ball.rect.topleft = randomPos(100, (FIELD_WIDTH)/2, 
												PLAYER_HEIGHT - BALL_HEIGHT, 
												DISPLAY_HEIGHT - PLAYER_HEIGHT)
					if not ball.rect.colliderect(player.rect):
						break


			clock.tick(30) #fps

	except SystemExit:
		pygame.quit()   

if __name__ == '__main__':
	playGame()






