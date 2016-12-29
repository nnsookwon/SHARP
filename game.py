import pygame
from random import randint
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

	def update(self):
		self.move()

	def move(self):
		newPos = self.rect.move((self.dx, self.dy))
		for sprite in allsprites: #prevent sprite collision
			if sprite is not self and \
				newPos.colliderect(sprite.rect):
				return
		if self.area.contains(newPos) and \
			field.collidepoint(newPos.bottomright):
			self.rect = newPos

class Goalie(pygame.sprite.Sprite):

	def __init__(self, image, pos, min_y, max_y, step):
		pygame.sprite.Sprite.__init__(self) #Sprite initializer
		self.image = image
		self.area = pygame.display.get_surface().get_rect()
		self.rect = self.image.get_rect()
		self.rect.topleft = pos #(x_pos, y_pos)
		self.dx = 0
		self.dy = step
		self.max_y = max_y
		self.min_y = min_y
		self.step = step

	def update(self):
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

	def update(self):
		self.move()
		if self.isShot:
			self.speed *= 0.95

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
				#bounce off collision
				if self.isShot:
					if newPos.right - self.dx <= sprite.rect.left or \
						newPos.left - self.dx >= sprite.rect.right:
						self.angle = math.pi - self.angle
						#self.speed = 0
					if newPos.bottom - self.dy <= sprite.rect.top or \
						newPos.top - self.dy >= sprite.rect.bottom:
						self.angle *= -1
					self.speed *= 0.75
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


pygame.init()

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

GOAL_WIDTH = 70 	
GOAL_HEIGHT = 200

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 80

BALL_WIDTH = 20
BALL_HEIGHT = 20

FIELD_WIDTH = DISPLAY_WIDTH - GOAL_WIDTH
FIELD_HEIGHT = DISPLAY_HEIGHT - 2*(PLAYER_HEIGHT - BALL_HEIGHT)

PENALTY_BOX_WIDTH = FIELD_WIDTH/2
PENALTY_BOX_HEIGHT = FIELD_HEIGHT - 100

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

#screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("SHARP")
screen.fill(GREEN)

field = pygame.Rect( 0, PLAYER_HEIGHT - BALL_HEIGHT, \
					 FIELD_WIDTH, \
 					 FIELD_HEIGHT)

penalty_box = pygame.Rect( (DISPLAY_WIDTH - PENALTY_BOX_WIDTH - GOAL_WIDTH), \
						   (DISPLAY_HEIGHT - PENALTY_BOX_HEIGHT)/2, \
						    PENALTY_BOX_WIDTH, PENALTY_BOX_HEIGHT)

player_img = pygame.image.load('player.png').convert()
player_img.set_colorkey(WHITE)
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
player = Player(player_img, (50,50), 10)

ball_img = pygame.image.load('ball.png').convert()
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))
ball = Ball(ball_img, (200,200), field)

goal = pygame.Rect(  DISPLAY_WIDTH - GOAL_WIDTH, \
			  		(DISPLAY_HEIGHT - GOAL_HEIGHT)/2, \
			  		 GOAL_WIDTH, GOAL_HEIGHT )

goalie_img = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
goalie_img.fill(BLUE)
goalie = Goalie(goalie_img, (FIELD_WIDTH - PLAYER_WIDTH, field.centery), \
				goal.top - 50, goal.bottom + 50, 5)

"""
goal_img = pygame.Surface((GOAL_WIDTH, GOAL_HEIGHT))
goal_img.fill(BLUE)
goal = pygame.sprite.Sprite()
goal.image = goal_img
goal.rect = goal.image.get_rect()
goal.rect.topleft = ( DISPLAY_WIDTH - GOAL_WIDTH, \
			  (DISPLAY_HEIGHT - GOAL_HEIGHT)/2) 
"""

pygame.display.update()

gameIsRunning = True

clock = pygame.time.Clock()

allsprites = pygame.sprite.RenderPlain((player, ball, goalie))

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
					break
				if event.key == pygame.K_a:
					player.dx = -player.step
				if event.key == pygame.K_d:
					player.dx = player.step
				if event.key == pygame.K_w:
					player.dy = -player.step    
				if event.key == pygame.K_s:
					player.dy = player.step
				

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
					player.hasBall:
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
	   
		allsprites.update()

		if ball.rect.top >= player.rect.centery and \
			ball.rect.bottom - 10 <= player.rect.bottom and \
			ball.rect.left - 10 <= player.rect.right and \
			ball.rect.left + 10 >= player.rect.right:
			#ball must be positioned to the right of player, 
			#and in the bottom half portion of the player
			if not player.hasBall:
				player.hasBall = True
				ball.isShot = False
				ball.speed = 0
				ball.angle = 0

		drawField()
		allsprites.draw(screen)
		if player.hasBall:
			(ball_x, ball_y) = ball.rect.midright
			#draw aiming arrow for shooting direction
			pygame.draw.line(screen, RED, (ball_x, ball_y), \
			 (ball_x + 50*math.cos(ball.angle), ball_y + 50*math.sin(ball.angle)), 4)

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






