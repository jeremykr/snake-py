# Python 3.5.0
from msvcrt import getch, kbhit
from copy import copy
import os, sys, time, random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

logo = bcolors.OKGREEN + \
'   _____ _   _  _   _  _  ________ \n' + \
'  / ____| \ | |(_)_(_)| |/ /  ____|\n' + \
' | (___ |  \| |  / \  | \' /| |__   \n' + \
'  \___ \| . ` | / _ \ |  < |  __|  \n' + \
'  ____) | |\  |/ ___ \| . \| |____ \n' + \
' |_____/|_| \_/_/   \_\_|\_\______|\n' + bcolors.ENDC

death_message = bcolors.FAIL + \
" _____  ______       _______ _    _ \n" + \
"|  __ \|  ____|   /\|__   __| |  | |\n" + \
"| |  | | |__     /  \  | |  | |__| |\n" + \
"| |  | |  __|   / /\ \ | |  |  __  |\n" + \
"| |__| | |____ / ____ \| |  | |  | |\n" + \
"|_____/|______/_/    \_\_|  |_|  |_|\n" + bcolors.ENDC
 
goodbye_message = bcolors.WARNING + \
'   _____  ____   ____  _____  ______     ________ \n' + \
'  / ____|/ __ \ / __ \|  __ \|  _ \ \   / /  ____|\n' + \
' | |  __| |  | | |  | | |  | | |_) \ \_/ /| |__   \n' + \
' | | |_ | |  | | |  | | |  | |  _ < \   / |  __|  \n' + \
' | |__| | |__| | |__| | |__| | |_) | | |  | |____ \n' + \
'  \_____|\____/ \____/|_____/|____/  |_|  |______|\n' + bcolors.ENDC

KEY_ESCAPE = 27
KEY_A = 97
KEY_W = 119
KEY_S = 115
KEY_D = 100

grid_size = 20

seconds_per_frame = 0.03

DEBUG = ""

#=====================UTILS=======================

def subtract_tuples(t1, t2):
	x = t1[0] - t2[0]
	y = t1[1] - t2[1]
	return (x, y)
	
def add_tuples(t1, t2):
	x = t1[0] + t2[0]
	y = t1[1] + t2[1]
	return (x, y)
	
# Compare current score to high score. If current score is greater, save it.
# Return high score.
def process_score(current_score):
	high_score = 0
	with open("./snake_scores.txt", "r") as f:
		try:
			high_score = int([line for line in f][0])
		except:
			print("Could not read high score.")
			pass
	
	if current_score > high_score:
		with open("./snake_scores.txt", "w") as f:
			f.write(str(current_score))
			high_score = current_score
			
	return high_score

#========================CLASSES====================

class SnakeSegment:
	def __init__(self, position):
		self.position = position

class Snake:	
	def __init__(self, direction, position):
		self.direction = direction
		body = [SnakeSegment(position)]
		self.body = body
		self.next_segment = SnakeSegment(subtract_tuples(self.body[0].position, self.direction))
		
	def update(self):
		self.next_segment = copy(self.body[-1])
		head = SnakeSegment(add_tuples(snake.body[0].position, self.direction))
		if len(snake.body) > 1:
			snake.body = [head] + snake.body[:-1]
		else:
			snake.body = [head]
		
	def add_segment(self):
		self.body.append(SnakeSegment(self.next_segment.position))
		
class Crumb:
	def __init__(self, position):
		self.position = position
		
		
#====================GAME FUNCTIONS====================

# Returns True if the game can still continue, False if not.
def update(snake, crumb, key):
		
	if key == KEY_W and snake.direction != (0, 1):
		snake.direction = (0, -1)
	elif key == KEY_A and snake.direction != (1, 0):
		snake.direction = (-1, 0)
	elif key == KEY_S and snake.direction != (0, -1):
		snake.direction = (0, 1)
	elif key == KEY_D and snake.direction != (-1, 0):
		snake.direction = (1, 0)
	
	snake.update()	
	
	head = snake.body[0]
	
	# Check if snake eats itself
	if head.position in list(map(lambda s: s.position, snake.body[1:])):
		return False
	# Check if snake goes out of bounds
	elif head.position[0] > grid_size - 1 or \
		head.position[1] > grid_size - 1 or \
		head.position[0] < 0 or \
		head.position[1] < 0:
		return False
	
	# Check if snake eats crumb
	if head.position == crumb.position:
		# Reset crumb
		crumb.position = (rand.randrange(grid_size), rand.randrange(grid_size))
		while crumb.position in list(map(lambda s: s.position, snake.body)):
			crumb.position = (rand.randrange(grid_size), rand.randrange(grid_size))
		# Add segment to snake
		snake.add_segment()
	
	return True
		
	
def draw(snake, crumb):
	border_colour = bcolors.OKBLUE
	snake_colour = bcolors.BOLD
	crumb_colour = bcolors.HEADER
	os.system("cls")
	screen = logo
	screen += "WASD or die\nPress ESC to wuss out\n"
	border = border_colour + ("+" + ("-"*grid_size*2 + "-") + "+\n") + bcolors.ENDC
	screen += border
	for row in range(0, grid_size):
		screen += border_colour + "| " + bcolors.ENDC
		for col in range(0, grid_size):
			if (col, row) in list(map(lambda s: s.position, snake.body)):
				if (col, row) == snake.body[0].position:
					screen += snake_colour + "o" + bcolors.ENDC
				else:
					screen += snake_colour + "·" + bcolors.ENDC
			elif (col, row) == crumb.position:
				screen += crumb_colour + "x" + bcolors.ENDC
			else:
				screen += " "
			screen += " "
		screen += border_colour + "|\n" + bcolors.ENDC
	screen += border
	print(screen)
	print("Score: " + str(len(snake.body) - 1))

#===================MAIN LOOP======================

snake = Snake((0, 1), (grid_size/2, 1))

rand = random.Random()
crumb = Crumb((rand.randrange(grid_size), rand.randrange(grid_size)))

while True:
	key = None
	if kbhit():
		key = ord(getch().lower())
	if key == KEY_ESCAPE:
		os.system("cls")
		print(goodbye_message)
		print("Final score: " + str(len(snake.body) - 1))
		print("High score: " + str(process_score(len(snake.body) - 1)))
		sys.exit()
	if not update(snake, crumb, key):
		os.system("cls")
		print(death_message)
		print("Final score: " + str(len(snake.body) - 1))
		print("High score: " + str(process_score(len(snake.body) - 1)))
		sys.exit()
	draw(snake, crumb)
	print(DEBUG)
	time.sleep(seconds_per_frame)