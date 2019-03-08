import pygame
import random
from math import sqrt


class Boid():
    position = None
    velocity = None

    def __init__(self, x, y):
        self.position = [x, y]
        self.velocity = [0, 0]

    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def show(self):
        pygame.draw.circle(gameDisplay, BLACK, self.position, 5, 2)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
angle = 0
x = 800
y = 600
pygame.init()
gameDisplay = pygame.display.set_mode((x, y))

clock = pygame.time.Clock()

boids = [Boid(random.randint(0, x), random.randint(0, y)) for i in range(100)]





def display_birds():
    for boid in boids:
        boid.show()
        # pygame.draw.circle(gameDisplay, BLACK, boid, 4, 2)


def vector_length(a, b):
	d = sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
	return d


def rule1(boid):
	vector = [0, 0]
	for b in boids:
		if b != boid:
			vector[0] += b.position[0]
			vector[1] += b.position[1]
	vector[0] /= (len(boids)-1)
	vector[1] /= (len(boids)-1)
	vector[0] = int((vector[0] - boid.position[0]) / 100)
	vector[1] = int((vector[1] - boid.position[1]) / 100)
	return vector


def rule2(boid):	#????
	vector = [0, 0]
	for b in boids:
		if b != boid and vector_length(boid.position, b.position) < 10:
			vector[0] -= (b.position[0] - boid.position[0])
			vector[1] -= (b.position[1] - boid.position[1])
	return vector


def rule3(boid):
	vector = [0, 0]
	for b in boids:
		if b != boid:
			vector[0] += b.velocity[0]
			vector[1] += b.velocity[1]
	vector[0] /= (len(boids) - 1)
	vector[1] /= (len(boids) - 1)
	vector[0] = int((vector[0] - boid.velocity[0]) / 8)
	vector[1] = int((vector[1] - boid.velocity[1]) / 8)
	return vector


def bound_position(boid):
	vector = [0, 0]

	if boid.position[0] < 0:
		vector[0] = 30
	elif boid.position[0] > x:
		vector[0] = -30
	if boid.position[1] < 0:
		vector[1] = 30
	elif boid.position[1] > y:
		vector[1] = -30
	return vector


def limit_velocity(boid):
	v_lim = 10
	vector = [0, 0]
	vec_length = sqrt(boid.velocity[0]**2 + boid.velocity[1]**2)
	if vec_length > v_lim:
		boid.velocity[0] = int(boid.velocity[0] / vec_length * v_lim)
		boid.velocity[1] = int(boid.velocity[1] / vec_length * v_lim)
	return vector



def move_birds():
	for b in boids:
		v1 = rule1(b)
		v2 = rule2(b)
		v3 = rule3(b)
		v4 = bound_position(b)
		v5 = limit_velocity(b)

		b.velocity[0] += v1[0] + v2[0] + v3[0] + v4[0] + v5[0]
		b.velocity[1] += v1[1] + v2[1] + v3[1] + v4[1] + v5[1]
		b.move()


loop = True
while loop:
	clock.tick(60)
	gameDisplay.fill(WHITE)
	display_birds()
	pygame.display.update()
	move_birds()




    # for event in pygame.event.get():
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_SPACE:
    #             pygame.quit()
    #             loop = False








# print("leo")
