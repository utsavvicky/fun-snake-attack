import pygame, sys, random
from pygame.locals import *

pygame.init()
FPS=20
fpsClock=pygame.time.Clock()
scr_width = 610
scr_height = 480
screen = pygame.display.set_mode((scr_width,scr_height))
n_blocks = 1
origin = [40,40]
eaten = 1

class snake:
	'Defines the snake'
	color = (0,250,0)
	width = 5
	height = 5
	x = 0
	y = 0

class food:
	'Food and parameters'
	color = (250,0,0)
	width = 5
	height = 5
	x = 80
	y = 80

snake1 = [snake() for _ in xrange(200)]
food1 = food()

def init_origin():
	for i in xrange(n_blocks):
		snake1[i].x = origin[0] - (5*i)
		snake1[i].y = origin[1]
	place_food()
	eaten = 0

def place_food():
	
	food1.x = random.randrange(0, scr_width, 5)
        food1.y = random.randrange(0, scr_height, 5)
	#pygame.draw.rect(screen, food1.color, ((food1.x, food1.y), (food1.width, food1.height)))


def follow():
	prev_x = snake1[0].x
	prev_y = snake1[0].y

	for i in range(1, n_blocks):
		prex=snake1[i].x
		prey=snake1[i].y
                snake1[i].x = prev_x
                snake1[i].y = prev_y
		prev_x = prex
		prev_y = prey

		#snake1[i].x = snake1[i-1].x
                #snake1[i].y = snake1[i-1].y


def move_right(cur_dir):
	
	if cur_dir != "LEFT":
		follow()
		snake1[0].x += snake1[0].width			


def move_left(cur_dir):

        if cur_dir != "RIGHT":
		follow()
                snake1[0].x -= snake1[0].width

def move_up(cur_dir):

        if cur_dir != "DOWN":
		follow()
                snake1[0].y -= snake1[0].height
               # follow()

def move_down(cur_dir):

        if cur_dir != "UP":
		follow()
                snake1[0].y += snake1[0].height
                #follow()


def draw():

	global eaten,n_blocks

	BLACK = [0,0,0]

	screen.fill(BLACK)

	for i in xrange(n_blocks):
		pygame.draw.rect(screen,snake1[i].color,((snake1[i].x,snake1[i].y),(snake1[i].width,snake1[i].height)))

	eaten = snake1[0].x == food1.x and snake1[0].y == food1.y

	if eaten:
		place_food()
		eaten = 0
		n_blocks += 1
		snake1[n_blocks-1].x=snake1[n_blocks-2].x
		snake1[n_blocks-1].y=snake1[n_blocks-2].y

	pygame.draw.rect(screen,food1.color,((food1.x, food1.y), (food1.width, food1.height)))

	pygame.display.update()

	fpsClock.tick(FPS)


def run():
	p_right = 0
	p_left = 0
	p_up = 0
	p_down = 0
	
	cur_dir = "RIGHT"

	init_origin()

	while True:

		draw()

		for event in pygame.event.get():
			if event.type ==pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == K_DOWN:
					p_down=1
					cur_dir = "DOWN"
				elif event.key == K_UP:
					p_up=1
					cur_dir = "UP"
				elif event.key == K_LEFT:
					p_left=1
					cur_dir = "LEFT"
				elif event.key == K_RIGHT:
					p_right=1
					cur_dir = "RIGHT"

			if event.type == pygame.KEYUP:
				if event.key == K_DOWN:
					p_down=0
                                elif event.key == K_UP:
                                        p_up=0
                                elif event.key == K_LEFT:
                                        p_left=0
                                elif event.key == K_RIGHT:
                                        p_right=0


		if p_left:
			move_left(cur_dir)
		elif p_right:
			move_right(cur_dir)
		elif p_up:
			move_up(cur_dir)
		elif p_down:
			move_down(cur_dir)



run()
