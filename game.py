import pygame
from random import randint
import time
import math

class GameObject(pygame.sprite.Sprite):
	#any object for the game with img, pos, and/or movement

	def __init__(self, image, pos, step):
		pygame.sprite.Sprite.__init__(self) #Sprite initializer
		self.image = image
		self.area = pygame.display.get_surface().get_rect()
		self.rect = self.image.get_rect()
		self.rect.topleft = pos #(x_pos, y_pos)
		self.dx = 0
		self.dy = 0
		self.step = step

	def update(self):
		self.move()

	def move(self):
		newPos = self.rect.move((self.dx, self.dy))
		for sprite in allsprites: #prevent sprite collision
			if sprite is not self and \
				sprite is not goal and \
				newPos.colliderect(sprite.rect):
				return
		if self.area.contains(newPos):
			self.rect = newPos

def randomPos(x_min, x_max, y_min, y_max):
	return (randint(x_min, x_max), randint(y_min, y_max))



pygame.init()

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

GOAL_WIDTH = 75
GOAL_HEIGHT = 200

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("SHARP")
screen.fill(WHITE)

player_img = pygame.image.load('player.png').convert()
player_img.set_colorkey(WHITE)
player_img = pygame.transform.scale(player_img, (50,80))
player = GameObject(player_img, (50,50), 10)
player.hasBall = False

ball_img = pygame.image.load('ball.png').convert()
ball_img = pygame.transform.scale(ball_img, (20,20))
ball = GameObject(ball_img, (200,200), player.step)

goal_img = pygame.Surface((GOAL_WIDTH, GOAL_HEIGHT))
goal_img.fill(BLUE)
goal = GameObject(goal_img, 
	((DISPLAY_WIDTH - GOAL_WIDTH), (DISPLAY_HEIGHT - GOAL_HEIGHT)/2), 0)


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

            #mouse changes angle
            if event.type == pygame.MOUSEMOTION:
                posx, posy = pygame.mouse.get_pos()
                playerX = 50+player.dx
                playerY = 50+player.dx
                aimx = -1*(playerY-posy)
                aimy = playerX - posx
                angle = math.atan2(float(aimx), float(aimy))
                player.image = pygame.transform.rotate(player.image, angle)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameExit = False
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
                	#shoot straight for now
                	#implement angles/direction later
                	ball.dy = 0
                	ball.dx = 15
                	ball.move() #to "break" away from player
                	
            elif event.type == pygame.KEYUP:
            	if event.key == pygame.K_a or \
            		event.key == pygame.K_d:
            		player.dx = 0
            	if event.key == pygame.K_w or \
            		event.key == pygame.K_s:
            		player.dy = 0  
            elif event.type == pygame.QUIT:
                gameExit = False
                break
                
            if gameExit:
                pygame.quit()
                sys.exit()
        
        if player.hasBall: #ball moves player
        	ball.dx = player.dx
        	ball.dy = player.dy        
       
        allsprites.update()

        if ball.rect.top >= player.rect.centery and \
        	ball.rect.bottom <= player.rect.bottom and \
        	ball.rect.left - 10 <= player.rect.right and \
        	ball.rect.left + 10 >= player.rect.right:
        	#ball must be positioned to the right of player, 
        	#and in the bottom half portion of the player
        	player.hasBall = True

        screen.fill(WHITE)
        allsprites.draw(screen)
        pygame.display.update()

        if(goal.rect.contains(ball.rect)):
        	time.sleep(2) #2 second delay
        	ball.dx = 0
        	ball.dy = 0
        	while True: #repeat if new ball position overlaps Player
        		ball.rect.topleft = randomPos(100, DISPLAY_WIDTH/2,
        								  	100, DISPLAY_HEIGHT-20)
        		if not ball.rect.colliderect(player.rect):
        			break


        clock.tick(30) #fps
except SystemExit:
    pygame.quit()	






