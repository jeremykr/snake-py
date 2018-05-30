# Python 3.5.0
from msvcrt import getch, kbhit
from copy import copy
import os, sys, time, random
from bcolors import *
from messages import *
from utils import *
from snake import *
from crumb import *

KEY_ESCAPE = 27
KEY_A = 97
KEY_W = 119
KEY_S = 115
KEY_D = 100

DEBUG = ""

class Game:
    def __init__(self):
        self.grid_size = 20
        self.seconds_per_frame = 0.03
        self.snake = Snake((0, 1), (self.grid_size/2, 1))
        self.rand = random.Random()
        self.crumb = Crumb((self.rand.randrange(self.grid_size), self.rand.randrange(self.grid_size)))
        self.key_pressed = None
        
    def _update(self):
        key = self.key_pressed
        snake = self.snake
        grid_size = self.grid_size
        crumb = self.crumb
        rand = self.rand

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

    def _draw(self):
        snake = self.snake
        grid_size = self.grid_size
        crumb = self.crumb

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
                    screen += snake_colour + "o" + bcolors.ENDC
                elif (col, row) == crumb.position:
                    screen += crumb_colour + "x" + bcolors.ENDC
                else:
                    screen += " "
                screen += " "
            screen += border_colour + "|\n" + bcolors.ENDC
        screen += border
        print(screen)
        print("Score: " + str(len(snake.body) - 1))

    def run(self):
        while True:
            if kbhit():
                self.key_pressed = ord(getch().lower())
            if self.key_pressed == KEY_ESCAPE:
                os.system("cls")
                print(goodbye_message)
                print("Final score: " + str(len(self.snake.body) - 1))
                print("High score: " + str(process_score(len(self.snake.body) - 1)))
                sys.exit()
            if not self._update():
                os.system("cls")
                print(death_message)
                print("Final score: " + str(len(self.snake.body) - 1))
                print("High score: " + str(process_score(len(self.snake.body) - 1)))
                sys.exit()
            self._draw()
            print(DEBUG)
            time.sleep(self.seconds_per_frame)
