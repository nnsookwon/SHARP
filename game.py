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
		

class Ball(pygame.sprite.Sprite):
	
	def __init__(self, image, pos, field):
		pygame.sprite.Sprite.__init__(self) #Sprite initializer
		self.image = image
		self.area = field #rect
		self.rect = self.image.get_rect()
		self.rect.topleft = pos #(x_pos, y_pos)
		self.dx = 0
		self.dy = 0

	def update(self):
		self.move()

	def move(self):
		newPos = self.rect.move((self.dx, self.dy))
		
		for sprite in allsprites: #prevent sprite collision
			if sprite is not self and \
				newPos.colliderect(sprite.rect):
				#collision detected, check if this is allowed
				if player.hasBall:
				#if Player has ball, no sprite can collide.
				#Player can NOT "walk" ball into goal
					return
					
		if self.area.contains(newPos) or \
			(goal.rect.collidepoint(newPos.bottomright) and \
			goal.rect.collidepoint(newPos.topright)):
			self.rect = newPos

def randomPos(x_min, x_max, y_min, y_max):
	return (randint(x_min, x_max), randint(y_min, y_max))

pygame.init()

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

GOAL_WIDTH = 70 	
GOAL_HEIGHT = 200

PENALTY_BOX_WIDTH = 400
PENALTY_BOX_HEIGHT = 400

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 80

BALL_WIDTH = 20
BALL_HEIGHT = 20

FIELD_WIDTH = DISPLAY_WIDTH - GOAL_WIDTH
FIELD_HEIGHT = DISPLAY_HEIGHT - 2*(PLAYER_HEIGHT - BALL_HEIGHT)

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

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
player.hasBall = False

ball_img = pygame.image.load('ball.png').convert()
ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))
ball = Ball(ball_img, (200,200), field)
ball.angle = 0

goal_img = pygame.Surface((GOAL_WIDTH, GOAL_HEIGHT))
goal_img.fill(BLUE)
goal = pygame.sprite.Sprite()
goal.image = goal_img
goal.rect = goal.image.get_rect()
goal.rect.topleft = ( DISPLAY_WIDTH - GOAL_WIDTH, \
			  (DISPLAY_HEIGHT - GOAL_HEIGHT)/2) 


pygame.display.update()

gameExit = False

clock = pygame.time.Clock()

allsprites = pygame.sprite.RenderPlain((player, ball, goal))

try:
	while not gameExit:        
		for event in pygame.event.get():
			#controlling with keys
			#w,a,s,d keys = movement
			#space bar = shoot
			#mouse = direction/angle
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					gameExit = True
					break
				if event.key == pygame.K_a:
					player.dx = -player.step
				if event.key == pygame.K_d:
					player.dx = player.step
				if event.key == pygame.K_w:
					player.dy = -player.step    
				if event.key == pygame.K_s:
					player.dy = player.step
				if event.key == pygame.K_SPACE and \
					player.hasBall:
					player.hasBall = False
					#implement angles/direction later
					
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

					ball.force = 20 #implement later: depending on force sensor
					ball.dy = ball.force * math.sin(ball.angle)
					ball.dx = ball.force * math.cos(ball.angle)
					ball.move() #to "break" away from player

				"""
				*************AIMING WITH ARROWS**************
				*********INCREMENTS OF 30 DEGREES************
				"""
				if event.key == pygame.K_UP:
					ball.angle = ball.angle - math.pi/6
					ball.angle = -math.pi/2 if ball.angle < -math.pi/2 \
								else ball.angle
					#"reversed" because y-position is 0, so positive is downwards
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
			elif event.type == pygame.QUIT:
				gameExit = True
				break
				
			if gameExit:
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
			player.hasBall = True

		screen.fill(GREEN)
		pygame.draw.rect(screen, BLACK, field, 1)
		pygame.draw.rect(screen, BLACK, penalty_box, 1 )
		allsprites.draw(screen)
		pygame.display.update()

		#check if ball landed in goal
		if(goal.rect.contains(ball.rect)):
			time.sleep(2) #2 second delay
			player.hasBall = False
			ball.dx = 0
			ball.dy = 0
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






