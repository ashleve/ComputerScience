import pygame
import numpy as np
from math import sqrt


class Boid():
    position = None
    velocity = None
    acceleration = 0
    BLACK = (0, 0, 0)

    def __init__(self, x, y):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.zeros(2, dtype=float)


    def show(self, gameDisplay):
        pygame.draw.circle(gameDisplay, self.BLACK, self.position.astype(int), 5, 2)


    def rand_velocity(self):
    	self.velocity = np.random.uniform(-10, 10, 2)


    def move(self):
        self.position += self.velocity.astype(int)
        self.velocity += self.acceleration


    def vector_length(self, b):
    	return sqrt(sum(np.power(b.position - self.position, 2)))


    def find_friends(self, boids, radius):
    	friends = []
    	for b in boids:
    		vec_length = self.vector_length(b)
    		if vec_length < radius and vec_length != 0:
    			friends.append(b)
    	return friends


