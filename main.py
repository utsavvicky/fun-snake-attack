import pygame, sys, random
from pygame.locals import *

pygame.init()

# speed of the game
FPS=13.0
fpsClock=pygame.time.Clock()

scr_width = 610
scr_height = 480
screen = pygame.display.set_mode((scr_width,scr_height))

# initial state of the snake
n_blocks = 1
origin = [40,40]
eaten = 1

class snake_block:
	'Defines the snake'
	color = (0,250,0)
	width = 5
	height = 5
	x = 0
	y = 0

class food_block:
	'Food and parameters'
	color = (250,0,0)
	width = 5
	height = 5
	x = 80
	y = 80

#initializing snake with 200 snake blocks
snake = [snake_block() for _ in xrange(200)]
food = food_block()

# initializing the first n blocks of the snake at their position and the food's position
def init_origin():
	for i in xrange(n_blocks):
		snake[i].x = origin[0] - (snake[i].width*i)
		snake[i].y = origin[1]
	place_food()
	eaten = 0


# function to randomly place food
def place_food():
	food.x = random.randrange(0, scr_width, 5)
        food.y = random.randrange(0, scr_height, 5)


# function to move the snake blocks by following the head block
def follow():
	prev_x = snake[0].x
	prev_y = snake[0].y

	for i in range(1, n_blocks):
		prex=snake[i].x
		prey=snake[i].y
                snake[i].x = prev_x
                snake[i].y = prev_y
		prev_x = prex
		prev_y = prey


def move_right(cur_dir):
	
	if cur_dir != "LEFT":
		follow()
		snake[0].x = (snake[0].x+snake[0].width)%(scr_width+5)
	else:	move_left(cur_dir)

def move_left(cur_dir):

        if cur_dir != "RIGHT":
		follow()
                snake[0].x = (snake[0].x-snake[0].width+scr_width+5)%(scr_width+5)
	else:	move_right(cur_dir)

def move_up(cur_dir):

        if cur_dir != "DOWN":
		follow()
                snake[0].y = (snake[0].y-snake[0].height+scr_height+5)%(scr_height+5)
        else:	move_down(cur_dir)

def move_down(cur_dir):
	
        if cur_dir != "UP":
		follow()
                snake[0].y = (snake[0].y+snake[0].height)%(scr_height+5)
	else:	move_up(cur_dir)


def draw():

	global eaten, n_blocks, FPS

	BLACK = [0,0,0]

	screen.fill(BLACK)

	for i in xrange(n_blocks):
		pygame.draw.rect(screen,snake[i].color,(((snake[i].x%(scr_width+5)),(snake[i].y%(scr_height+5))),(snake[i].width,snake[i].height)))

	eaten = snake[0].x == food.x and snake[0].y == food.y

	if eaten:
		place_food()
		eaten = 0
		n_blocks += 1
		snake[n_blocks-1].x=snake[n_blocks-2].x			# adding new block when food is consumed at the last block position
		snake[n_blocks-1].y=snake[n_blocks-2].y
		FPS += 0.5						# increasing speed after every food consumption

	pygame.draw.rect(screen,food.color,((food.x, food.y), (food.width, food.height)))

	pygame.display.update()

	fpsClock.tick(FPS)


def run():
	p_right = 0
	p_left = 0
	p_up = 0
	p_down = 0
	
	cur_dir = "RIGHT"
	prev_dir = ""

	init_origin()

	while True:

		draw()

		for event in pygame.event.get():
			if event.type ==pygame.QUIT:
				pygame.quit()
				sys.exit()
			
			if event.type == pygame.KEYDOWN:
				if event.key == K_DOWN and cur_dir != "UP":
					p_down=1
					prev_dir = cur_dir
					cur_dir = "DOWN"
					p_left=0
					p_right=0
					p_up=0
				elif event.key == K_UP and cur_dir != "DOWN":
					p_up=1
					prev_dir = cur_dir
					cur_dir = "UP"
					p_down=0
					p_left=0
					p_right=0
				elif event.key == K_LEFT and cur_dir != "RIGHT":
					p_left=1
					prev_dir = cur_dir
					cur_dir = "LEFT"
					p_right=0
					p_up=0
					p_down=0
				elif event.key == K_RIGHT and cur_dir != "LEFT":
					p_right=1
					prev_dir = cur_dir
					cur_dir = "RIGHT"
					p_up=0
					p_left=0
					p_down=0
				# TODO If ESC key is pressed, display pause screen
		if p_left:
			move_left(prev_dir)
		elif p_right:
			move_right(prev_dir)
		elif p_up:
			move_up(prev_dir)
		elif p_down:
			move_down(prev_dir)



run()
