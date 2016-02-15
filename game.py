import pygame,random,sys,os
from pygame.locals import *

pygame.init()

# speed of the game
FPS=13.0
fpsClock=pygame.time.Clock()

scr_width = 610
scr_height = 480
screen = pygame.display.set_mode((scr_width,scr_height))

# initial state of the snake
n_blocks = 5
n_blocks1 = 5
origin = [50,50]
origin1 = [scr_width-50,50]
eaten = 1
eaten1 = 1
score = 0
score1 = 0
t = -1

class pause_scr_item(pygame.font.Font):
        def __init__(self, text, font=None, font_size=48, font_color=(255, 255, 255), (pos_x, pos_y)=(0, 0)):
                pygame.font.Font.__init__(self, font, font_size)
                self.text = text
                self.font_size = font_size
                self.font_color = font_color
                self.label = self.render(self.text, 1, self.font_color)
                self.width = self.label.get_rect().width
                self.height = self.label.get_rect().height
                self.dimensions = (self.width, self.height)
                self.pos_x = pos_x
                self.pos_y = pos_y
                self.position = pos_x, pos_y

        def set_position(self, x, y):
                self.position = (x, y)
                self.pos_x = x
                self.pos_y = y

        def set_font_color(self, rgb_tuple):
                self.font_color = rgb_tuple
                self.label = self.render(self.text, 1, self.font_color)

        def is_mouse_selection(self, (posx, posy)):
                if (posx >= self.pos_x and posx <= self.pos_x + self.width) and (posy >= self.pos_y and posy <= self.pos_y + self.height):
                        return True
                return False

class Background(pygame.sprite.Sprite):
        def __init__(self, image_file, location):
                pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
                self.image = pygame.image.load(image_file)
                self.rect = self.image.get_rect()
                self.rect.left, self.rect.top = location

class snake_block:
	'Defines the snake'
	color = [255,255,255]
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
snake=[]
snake1=[]
food = food_block()


# initializing for a new game
def init():
	global t, snake, food, eaten, score, FPS, n_blocks, origin, snake1, eaten1, score1, n_blocks1, origin1

	hs = open("hs.txt","w")
	hs.write("0")
	hs.close()

	snake = [snake_block() for _ in xrange(200)]
	
	snake1 = [snake_block() for _ in xrange(200)]
	
	food = food_block()

	n_blocks = 5
	n_blocks1 = 5
	score = 0
	score1 = 0
	t = -1
	origin[0] += n_blocks*5

	for i in xrange(n_blocks):
		snake[i].x = origin[0] - (snake[i].width*i)
		snake[i].y = origin[1]
		snake[i].color = [0,250,0]

	origin1[0] += n_blocks1*5

	for i in xrange(n_blocks1):
		snake1[i].x = origin1[0] - (snake1[i].width*i)
		snake1[i].y = origin1[1]
		snake1[i].color = [0,0,220]
		
	place_food()
	eaten = 0
	eaten1 = 0

	FPS=13.0
	

# function to randomly place food
def place_food():
	food.x = random.randrange(0, scr_width, 5)
	food.y = 200
        #food.y = random.randrange(45, scr_height, 5)


# function to move the snake blocks by following the head block
def follow(snake, n_blocks):
	prev_x = snake[0].x
	prev_y = snake[0].y

	for i in range(1, n_blocks):
		prex=snake[i].x
		prey=snake[i].y
                snake[i].x = prev_x
                snake[i].y = prev_y
		prev_x = prex
		prev_y = prey


def move_right(snake,cur_dir,n_blocks):
	
	if cur_dir != "LEFT":
		follow(snake,n_blocks)
		snake[0].x = (snake[0].x+snake[0].width)%(scr_width+5)
	else:	move_left(snake, cur_dir,n_blocks)

def move_left(snake,cur_dir,n_blocks):

        if cur_dir != "RIGHT":
		follow(snake,n_blocks)
                snake[0].x = (snake[0].x-snake[0].width+scr_width+5)%(scr_width+5)
	else:	move_right(snake, cur_dir,n_blocks)

def move_up(snake,cur_dir,n_blocks):

        if cur_dir != "DOWN":
		follow(snake,n_blocks)
                snake[0].y = (snake[0].y-snake[0].height+scr_height+5)%(scr_height+5)
        else:	move_down(snake, cur_dir,n_blocks)

def move_down(snake,cur_dir,n_blocks):
	
        if cur_dir != "UP":
		follow(snake,n_blocks)
                snake[0].y = (snake[0].y+snake[0].height)%(scr_height+5)
	else:	move_up(snake, cur_dir,n_blocks)

def game_over(snake,n_blocks,mode):
	global t

	hs = open("hs.txt","r")
        hscore = (int)(hs.read())
        hs.close()

	if score > hscore:
		hs = open("hs.txt","w")
		hs.write((str)(score))
		hs.close()

	if n_blocks <=2 :	return
	
	if mode == "multi":
		for i in xrange(1,n_blocks):
			if snake[0].x == snake[i].x and snake[0].y == snake[i].y:
				t = FPS*10
				snake[0].x = -1
				for _ in xrange(n_blocks):
					snake[_].color = (0,0,0)
				break

	else:
		for i in xrange(1,n_blocks):
			if snake[0].x == snake[i].x and snake[0].y == snake[i].y:
				display_game_over_screen(mode)
		

def display_game_over_screen(mode):

	global hscore

	hs = open("hs.txt","r")
	hscore = (int)(hs.read())
	hs.close()

	gover_font = pygame.font.SysFont(None, 48)
	other_font = pygame.font.SysFont(None, 40)

	gameover = gover_font.render("Gameover!", True, (255,255,255))

	BackGround = Background("./s.jpg", [0,0])
	
	if mode == "multi":
		scored2 = other_font.render("Score: %d"%score1, True, (0,0,255))
	        scored2_pos = [(scr_width/2) - (scored2.get_rect().width / 2), (scr_height / 2) + (scored2.get_rect().height)/2 + 6]

	scored= other_font.render("Score: %d"%score, True,(0,255,0))
	play_again = other_font.render("Play Again?", True, (255,255,255))
	quit = other_font.render("Quit", True, (255,255,255))
	high_score = other_font.render("High Score: %d"%hscore, True, (255,255,255))

	gameover_pos = [(scr_width / 2) - (gameover.get_rect().width / 2), (scr_height / 2) - (5*gameover.get_rect().height)/2]
	high_score_pos = [(scr_width / 2) - (high_score.get_rect().width / 2), (scr_height/2) - (3*high_score.get_rect().height)/2 + 2]
	scored_pos = [(scr_width / 2) - (scored.get_rect().width / 2), (scr_height / 2) - (scored.get_rect().height)/2 + 4]
	play_again_pos = [(scr_width / 2) - (play_again.get_rect().width / 2), (scr_height / 2) + (3*play_again.get_rect().height)/2 + 8]
	quit_pos = [(scr_width / 2) - (quit.get_rect().width / 2), (scr_height / 2) + (5*quit.get_rect().height)/2 + 10]

	loop = True

	while loop:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()

				if pos[0] >= play_again_pos[0] and pos[0] <= play_again_pos[0] + play_again.get_rect().width and pos[1] >= play_again_pos[1] and pos[1] <= play_again_pos[1] + play_again.get_rect().height:	run(mode)

				if pos[0] >= quit_pos[0] and pos[0] <= quit_pos[0] + quit.get_rect().width and pos[1] >= quit_pos[1] and pos[1] <= quit_pos[1] + quit.get_rect().height:
					pygame.quit()
					sys.exit()
		
		screen.fill((0,0,0))

		screen.blit(BackGround.image, BackGround.rect)
		screen.blit(gameover, gameover_pos)
		screen.blit(high_score, high_score_pos)
		screen.blit(scored, scored_pos)	

		if mode=="multi":
			screen.blit(scored2, scored2_pos)
	
		screen.blit(play_again, play_again_pos)
		screen.blit(quit, quit_pos)

		pygame.display.flip()

def score_toolbar(mode):
	t_height = 40
	t_width = scr_width
	global t
	font = pygame.font.SysFont(None, t_height/2)
	score_txt = font.render("S1: %d"%score, True, (0,255,0))
	
	score_txt_pos = [10, t_height/2 - score_txt.get_rect().height/2]
	
	screen.blit(score_txt, score_txt_pos)

	if mode=="multi":
		score1_txt = font.render("S2: %d"%score1, True, (0,0,255))

		score1_txt_pos = [t_width-50, t_height/2 - score1_txt.get_rect().height/2]

		time_txt = font.render("Time Left: %0.2f"%(t/FPS), True,(255,255,255))

		time_position = [(t_width/2)-time_txt.get_rect().width/2, t_height/2 - time_txt.get_rect().height/2]

		screen.blit(score1_txt, score1_txt_pos)
		if t >= 0 :
			screen.blit(time_txt, time_position)


def draw(mode):

	global snake, snake1, eaten, n_blocks, FPS, score, eaten1, n_blocks1, score1

	BLACK = [0,0,0]
	WHITE = [255,255,255]
	GREEN = [0,250,0]
	BLUE = [0,0,220]

	screen.fill(BLACK)
	
	score_toolbar(mode)

	for i in xrange(n_blocks):
		pygame.draw.rect(screen,snake[i].color,(((snake[i].x%(scr_width+5)),(snake[i].y%(scr_height+5))),(snake[i].width,snake[i].height)))
	eaten = snake[0].x == food.x and snake[0].y == food.y

	if eaten:
		place_food()
		eaten = 0
		eaten1=0
		n_blocks += 1
		snake[n_blocks-1].x=snake[n_blocks-2].x			# adding new block when food is consumed at the last block position
		snake[n_blocks-1].y=snake[n_blocks-2].y
		snake[n_blocks-1].color = GREEN
		FPS += 0.75						# increasing speed after every food consumption
		score += 10

	if mode=="multi":
		for i in xrange(n_blocks1):
			pygame.draw.rect(screen,snake1[i].color,(((snake1[i].x%(scr_width+5)),(snake1[i].y%(scr_height+5))),(snake1[i].width,snake1[i].height)))
		eaten1 = snake1[0].x == food.x and snake1[0].y == food.y

		if eaten1:
			place_food()
			eaten1 = 0
			eaten=0
			n_blocks1 += 1
			snake1[n_blocks1-1].x=snake1[n_blocks1-2].x                 # adding new block when food is consumed at the last block position
			snake1[n_blocks1-1].y=snake1[n_blocks1-2].y
			snake1[n_blocks1-1].color = BLUE
			FPS += 0.75                                              # increasing speed after every food consumption
			score1 += 10

 

	pygame.draw.rect(screen,food.color,((food.x, food.y), (food.width, food.height)))

	pygame.display.update()

	fpsClock.tick(FPS)

# pause the game
def pause():

	loop = True

	items_arr = ['Resume', 'New Game', 'Quit']

	items = []

	BackGround = Background("./s.jpg", [0,0])

	for index,item in enumerate(items_arr):
		menu_item = pause_scr_item(item)

		t_h = len(items_arr) * menu_item.height
		pos_x = (scr_width / 2) - (menu_item.width / 2)

		pos_y = (scr_height / 2) - (t_h / 2) + ((index * 2) + index * menu_item.height)

		menu_item.set_position(pos_x, pos_y)
		items.append(menu_item)

	screen.fill([0,0,0])

	while loop:
		
		pygame.time.Clock().tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				for item in items:
					if item.is_mouse_selection(pos):
						loop = False
						if item.text == "Quit":
							pygame.quit()
							sys.exit()
						if item.text == "New Game":
							pygame.quit()
							os.system("python main.py")
							sys.exit()
							

		screen.fill([0,0,0])

		screen.blit(BackGround.image, BackGround.rect)
		
		for item in items:
			if item.is_mouse_selection(pygame.mouse.get_pos()):
				item.set_font_color((255,255,255))
				item.set_bold(True)
			else:	
				item.set_font_color((255,255,255))
				item.set_bold(False)

			screen.blit(item.label, item.position)
				


		pygame.display.flip()		

def run(mode):
	p_right = 0
	p_left = 0
	p_up = 0
	p_down = 0
	
	p1_right = 0
        p1_left = 0
        p1_up = 0
        p1_down = 0


	cur_dir = "RIGHT"
	prev_dir = ""

	cur_dir1 = "RIGHT"
        prev_dir1 = ""

	global t

	main_loop = True

	init()

	while main_loop:
		
		draw(mode)
		
		pygame.image.save(screen, "s.jpg")
		
		if t==-1:
			game_over(snake,n_blocks,mode)
			game_over(snake1,n_blocks1,mode)

		if t > 0:
			t-=1
		elif t!=-1:
			display_game_over_screen(mode)

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
				elif event.key == K_s and cur_dir1 != "UP":
                                        p1_down=1
                                        prev_dir1 = cur_dir1
                                        cur_dir1 = "DOWN"
                                        p1_left=0
                                        p1_right=0
                                        p1_up=0
                                elif event.key == K_w and cur_dir1 != "DOWN":
                                        p1_up=1
                                        prev_dir1 = cur_dir1
                                        cur_dir1 = "UP"
                                        p1_down=0
                                        p1_left=0
                                        p1_right=0
                                elif event.key == K_a and cur_dir1 != "RIGHT":
                                        p1_left=1
                                        prev_dir1 = cur_dir1
                                        cur_dir1 = "LEFT"
                                        p1_right=0
                                        p1_up=0
                                        p1_down=0
                                elif event.key == K_d and cur_dir1 != "LEFT":
                                        p1_right=1
                                        prev_dir1 = cur_dir1
                                        cur_dir1 = "RIGHT"
                                        p1_up=0
                                        p1_left=0
                                        p1_down=0

				elif event.key == K_ESCAPE:
					pause()
		if p_left:
			move_left(snake, prev_dir,n_blocks)
		elif p_right:
			move_right(snake, prev_dir,n_blocks)
		elif p_up:
			move_up(snake, prev_dir,n_blocks)
		elif p_down:
			move_down(snake, prev_dir,n_blocks)

		if p1_left:
                        move_left(snake1, prev_dir1,n_blocks1)
                elif p1_right:
                        move_right(snake1, prev_dir1,n_blocks1)
                elif p1_up:
                        move_up(snake1, prev_dir1,n_blocks1)
                elif p1_down:
                        move_down(snake1, prev_dir1,n_blocks1)


#-----------------------------------------------------------------------
def move_min_horizontal(cur_dir, prev_dir):

	if food.x>snake[0].x:
		print cur_dir
		if  (food.x - snake[0].x) < (scr_width - food.x) + snake[0].x and cur_dir!="LEFT":
			prev_dir = cur_dir
			cur_dir = "RIGHT"
			move_right(snake, prev_dir, n_blocks)

		elif cur_dir!="RIGHT":
			prev_dir = cur_dir
			cur_dir = "LEFT"
			move_left(snake, prev_dir, n_blocks)

		else:
			prev_dir = cur_dir
			cur_dir="DOWN"
			move_down(snake, prev_dir, n_blocks)


	else:
		print cur_dir
		if  (-food.x + snake[0].x) < (scr_width + food.x) - snake[0].x and cur_dir!="RIGHT":
			prev_dir = cur_dir
			cur_dir = "LEFT"
			move_left(snake, prev_dir, n_blocks)

		elif cur_dir!="LEFT":
			prev_dir = cur_dir
			cur_dir = "RIGHT"
			move_right(snake, prev_dir, n_blocks)

		else:
			prev_dir = cur_dir
			cur_dir = "DOWN"
			move_down(snake, prev_dir, n_blocks)

	return [cur_dir, prev_dir]


def move_min_vertical(cur_dir, prev_dir):
	
	if food.y>snake[0].y:
		if  (food.y - snake[0].y) < (scr_height - food.y) + snake[0].y and cur_dir!="UP":
			prev_dir = cur_dir
			cur_dir = "DOWN"
			move_down(snake, prev_dir, n_blocks)

		elif cur_dir!="UP" and cur_dir!="DOWN":
			prev_dir = cur_dir
			cur_dir = "UP"
			move_up(snake,prev_dir, n_blocks)

		else:
			prev_dir = cur_dir
			cur_dir = "RIGHT"
			move_right(snake, prev_dir, n_blocks)


	else:
		if  (-food.y + snake[0].y) < (scr_height + food.y) - snake[0].y and cur_dir!="DOWN":
			prev_dir = cur_dir
			cur_dir = "UP"
			move_up(snake,prev_dir, n_blocks)

		elif cur_dir!="UP" and cur_dir!="DOWN":
			prev_dir = cur_dir
			cur_dir = "DOWN"
			move_down(snake, prev_dir, n_blocks)

		else:
			prev_dir = cur_dir
			cur_dir = "RIGHT"
			move_right(snake, prev_dir, n_blocks)

	return [cur_dir, prev_dir]



def cpu_player():
	p_right = 0
	p_left = 0
	p_up = 0
	p_down = 0

	cur_dir = ""
	prev_dir = ""

	global t

	main_loop = True

	init()

	while main_loop:
		
		draw("")
		
		pygame.image.save(screen, "s.jpg")
		
		if t==-1:
			print cur_dir
			game_over(snake,n_blocks,"")

		if t > 0:
			t-=1
		elif t!=-1:
			display_game_over_screen("")


		for event in pygame.event.get():
			if event.type ==pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					pause()

		print food.x, food.y
		print snake[0].x, snake[0].y
		print "-----------"

		if food.y == snake[0].y or food.x != snake[0].x:
			cur_dir, prev_dir = move_min_horizontal(cur_dir, prev_dir)
		else:
			cur_dir, prev_dir = move_min_vertical(cur_dir, prev_dir)	
