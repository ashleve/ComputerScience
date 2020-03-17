import pyglet
from object import Object


bounds = [1000, 750]
game_window = pyglet.window.Window(*bounds)
fps_display = pyglet.window.FPSDisplay(game_window)


main_label = pyglet.text.Label(
    text="Control Systems",
    x=bounds[0]/2, y=bounds[1]-25,
    anchor_x='center'
)


object_one = Object(bounds[0]//7, bounds[1]//2 - 200, bounds[0]//7, bounds[1]//2)
object_two = Object(bounds[0]//7*2, bounds[1]//2 - 200, bounds[0]//7*2, bounds[1]//2)
object_three = Object(bounds[0]//7*3, bounds[1]//2 - 200, bounds[0]//7*3, bounds[1]//2)
object_four = Object(bounds[0]//7*4, bounds[1]//2 - 200, bounds[0]//7*4, bounds[1]//2)
object_five = Object(bounds[0]//7*5, bounds[1]//2 - 200, bounds[0]//7*5, bounds[1]//2)
object_six = Object(bounds[0]//7*6, bounds[1]//2 - 200, bounds[0]//7*6, bounds[1]//2)


@game_window.event
def on_draw():
    pyglet.gl.glClearColor(0.0, 0.0, 0.1, 1.0)
    game_window.clear()
    pyglet.gl.glLoadIdentity()

    main_label.draw()
    fps_display.draw()

    object_one.draw()
    object_two.draw()
    object_three.draw()
    object_four.draw()
    object_five.draw()
    object_six.draw()


def update(_):
    object_one.p_update_velocity()
    object_two.pd_update_velocity()
    object_three.p_update_acceleration()
    object_four.pd_update_acceleration()
    object_five.pid_update_acceleration()
    # object_six


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/120)   # 110 fps
    pyglet.app.run()
