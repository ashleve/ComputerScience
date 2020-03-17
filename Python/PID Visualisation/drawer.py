import math
from pyglet.gl import (
    glPushMatrix, glPopMatrix, glBegin, glEnd, glColor3f,
    glVertex2f, glTranslatef, glRotatef, glColor3ub,
    GL_LINE_LOOP, GL_TRIANGLES, GL_TRIANGLE_FAN)


def draw_circle(position, size=20, num_of_segments=30):
    glBegin(GL_LINE_LOOP)
    for i in range(num_of_segments):
        theta = 2.0 * 3.1415926 * i / num_of_segments
        cx = size * math.cos(theta)
        cy = size * math.sin(theta)
        glVertex2f(position.x + cx, position.y + cy)
    glEnd()


def draw_filled_circle(position, size=20, num_of_segments=30, color=None):
    if color is None:
        glColor3ub(255, 0, 0)
    else:
        glColor3f(*color)

    twice_pi = 2.0 * 3.141596
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(position.x, position.y)
    for i in range(num_of_segments + 1):
        glVertex2f(
            (position.x + (size * math.cos(i * twice_pi / num_of_segments))),
            (position.y + (size * math.sin(i * twice_pi / num_of_segments)))
        )
    glEnd()


def draw_triangle(position, velocity, size=20, color=None):
    glPushMatrix()
    glTranslatef(position.x, position.y, 0.0)

    glRotatef(math.degrees(math.atan2(velocity.x, velocity.y)), 0.0, 0.0, -1.0)

    glBegin(GL_TRIANGLES)

    if color is None:
        glColor3ub(255, 0, 0)
    else:
        glColor3f(*color)

    glVertex2f(size, 0.0)
    glVertex2f(-size, 0.0)
    glVertex2f(0.0, size * 3.0)

    glEnd()
    glPopMatrix()
