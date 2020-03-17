from vector2 import Vector2
import drawer
import random


class Object:

    def __init__(self, x, y, target_x, target_y):
        self.position = Vector2(x, y)
        self.target = Vector2(target_x, target_y)

        self.last_error = Vector2()
        self.last_vel = Vector2()
        self.integral = Vector2()

        self.P_gain = .5
        self.D_gain = 3
        self.I_gain = .01

        self.velocity = Vector2(x=0, y=0)
        self.max_velocity = 10

        self.acceleration = Vector2(x=0, y=0)
        self.max_acceleration = 2

        self.size = 15
        self.num_of_segments = 50
        self.color = [random.uniform(0, 1), random.uniform(0, 1), 1.0]

    def p_update_velocity(self):
        error = (self.target - self.position) / 120

        self.velocity = self.P_gain * error
        self.velocity.limit_magnitude(self.max_velocity)

        self.position += self.velocity

    def pd_update_velocity(self):
        error = self.get_position_error()
        diff = error - self.last_error

        self.velocity = self.P_gain * error + self.D_gain * diff
        self.velocity.limit_magnitude(self.max_velocity)

        self.position += self.velocity
        self.last_error = error

    def p_update_acceleration(self):
        error = self.get_position_error()
        self.acceleration = self.P_gain * error

        self.velocity.limit_magnitude(self.max_velocity)
        self.acceleration.limit_magnitude(self.max_acceleration)

        self.velocity += self.acceleration
        self.position += self.velocity

    def pd_update_acceleration(self):
        error = self.get_position_error()
        diff = error - self.last_error

        self.acceleration = self.P_gain * error + self.D_gain * diff
        self.acceleration.limit_magnitude(self.max_acceleration)

        self.velocity += self.acceleration
        self.velocity.limit_magnitude(self.max_velocity)

        self.position += self.velocity
        self.last_error = error

    def pid_update_acceleration(self):
        error = self.get_position_error()
        diff = error - self.last_error
        self.integral += error

        self.acceleration = self.P_gain * error + self.I_gain * self.integral + self.D_gain * diff
        self.acceleration.limit_magnitude(self.max_acceleration)

        self.velocity += self.acceleration
        self.velocity.limit_magnitude(self.max_velocity)

        self.position += self.velocity
        self.last_error = error

    def get_position_error(self):
        return (self.target - self.position) / 120

    def draw(self):
        drawer.draw_filled_circle(self.position)
