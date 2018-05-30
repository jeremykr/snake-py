from snake_segment import *
from utils import *
from copy import copy

class Snake:
	def __init__(self, direction, position):
		self.direction = direction
		body = [SnakeSegment(position)]
		self.body = body
		self.next_segment = SnakeSegment(subtract_tuples(self.body[0].position, self.direction))
		
	def update(self):
		self.next_segment = copy(self.body[-1])
		head = SnakeSegment(add_tuples(self.body[0].position, self.direction))
		if len(self.body) > 1:
			self.body = [head] + self.body[:-1]
		else:
			self.body = [head]
		
	def add_segment(self):
		self.body.append(SnakeSegment(self.next_segment.position))