import pygame
from Boid import Boid
import numpy as np
from random import randint
import math


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
(x, y) = (800, 600)

pygame.init()
gameDisplay = pygame.display.set_mode((x, y))
clock = pygame.time.Clock()

num_of_boids = 100
boids = [Boid(randint(0, x), randint(0, y)) for i in range(num_of_boids)]

max_velocity = 5
cohesion_radius = 100
alignment_radius = 40

for b in boids:
	b.rand_velocity()


def cohesion(b):
	vec = np.zeros(2)
	friends = b.find_friends(boids, cohesion_radius)
	if len(friends) != 0:
		for f in friends:
			vec += f.position
		vec = vec / len(friends)
		vec -= b.position
		vec -= b.velocity
	return vec



def alignment(b):
	vec = np.zeros(2)
	friends = b.find_friends(boids, alignment_radius)
	for f in friends:
		vec += f.velocity
	if len(friends) > 0:
		vec /= len(friends)
		vec -= b.velocity
	return vec




def limit_velocity(b):
	v_lim = max_velocity
	vec_length = math.sqrt(b.velocity[0]**2 + b.velocity[1]**2)
	if vec_length > v_lim:
		b.velocity = b.velocity / vec_length * v_lim


def boundaries(b):
	vec = np.zeros(2)
	if b.position[0] > x:
		# vec[0] -= 10
		b.position[0] = b.position[0] - x
	elif b.position[0] < 0:
		# vec[0] += 10
		b.position[0] = b.position[0] + x
	if b.position[1] > y:
		# vec[1] -= 10
		b.position[1] = b.position[1] - y
	elif b.position[1] < 0:
		# vec[1] += 10
		b.position[1] = b.position[1] + y
	return vec


def move_boids():
	v1 = np.zeros(2)
	v2 = np.zeros(2)
	v3 = np.zeros(2)
	v4 = np.zeros(2)
	for b in boids:
		b.acceleration = cohesion(b)
		# v1 = cohesion(b)
		v2 = boundaries(b)
		# b.acceleration = alignment(b)
		limit_velocity(b)
		# b.velocity += v1 + v2 + v3 + v4
		b.move()


def display_boids():
	for b in boids:
		b.show(gameDisplay)



while True:
	gameDisplay.fill(WHITE)
	clock.tick(60)

	move_boids()
	display_boids()
	
	pygame.display.update()
