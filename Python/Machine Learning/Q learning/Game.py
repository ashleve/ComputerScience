from tkinter import *

master = Tk()
Width = 100
(x, y) = (5, 5)

board = Canvas(master, width=x * Width, height=y * Width)

player = (0, 0)
player_size = (0.2 * Width, 0.8 * Width)
actions = ["up", "down", "left", "right"]

# object = (x, y, color, reward)
enemy = (4, 2, "red", -10)
objective = (4, 4, "green", +1)
specials = [enemy, objective]
walls = [(2, 2), (3, 4), (2, 3)]

score = 1
walk_penalty = -0.07

restart = False


def render_grid():
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill="white", width=1)
    board.create_oval(enemy[0] * Width + 20, enemy[1] * Width + 20, (enemy[0] + 1) * Width - 20, (enemy[1] + 1) * Width - 20, fill=enemy[2], width=0.5)
    board.create_rectangle(objective[0] * Width + 10, objective[1] * Width + 10, (objective[0] + 1) * Width - 10, (objective[1] + 1) * Width - 10, fill=objective[2], width=0.5)
    for wall in walls:
        board.create_rectangle(wall[0] * Width, wall[1] * Width, (wall[0] + 1) * Width, (wall[1] + 1) * Width, fill="black", width=0.5)


render_grid()


def move_player(dx, dy):
    global player, score, restart  # nie wiem czemu deklaracje ale inaczej nie działa

    if restart is True:
        restart_game()

    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_penalty
    if new_x >= 0 and new_x < x and new_y >= 0 and new_y < y and (new_x, new_y) not in walls:
        board.coords("player", new_x * Width + player_size[0], new_y * Width + player_size[0], new_x * Width + player_size[1], new_y * Width + player_size[1])
        player = (new_x, new_y)

    if player == (enemy[0], enemy[1]):
        score += enemy[3]
        restart = True
        print("Failure! Your score is: ", "%0.2f" % score)

    if player == (objective[0], objective[1]):
        score += objective[3]
        restart = True
        print("Success! Your score is: ", "%0.2f" % score)


def restart_game():
    global player, score, restart

    player = (0, 0)
    score = 1
    restart = False
    board.coords("player", player_size[0], player_size[0], player_size[1], player_size[1])


def move_up(event):
    move_player(0, -1)


def move_down(event):
    move_player(0, 1)


def move_right(event):
    move_player(1, 0)


def move_left(event):
    move_player(-1, 0)


master.bind("<w>", move_up)
master.bind("<s>", move_down)
master.bind("<a>", move_left)
master.bind("<d>", move_right)

board.create_rectangle(player[0] * Width + player_size[0], player[1] * Width + player_size[0],
                       player[0] * Width + player_size[1], player[1] * Width + player_size[1], fill="orange", width=5, tag="player")

board.grid(row=0, column=0)


def start_game():
    master.mainloop()


# master.mainloop()
