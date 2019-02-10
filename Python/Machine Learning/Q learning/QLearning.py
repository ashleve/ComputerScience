import Game
from threading import Thread
import time


discount = 0.1

# create states collection:
states = []
for i in range(Game.x):
    for j in range(Game.y):
        states.append((i, j))

# create Q dict:
Q = {}
for state in states:
    # create new dict of actions each iteration:
    temp = {}
    for action in Game.actions:
        temp[action] = 0.1
    # temp = {'up': 0.1, 'down': 0.1, 'left': 0.1, 'right': 0.1}
    # assign actions values to states:
    Q[state] = temp

for (x, y, color, value) in Game.specials:  # w sumie to nie wiem co to daje
    for action in Game.actions:
        Q[(x, y)][action] = value


def do_action(action):
    r = -Game.score

    if action == "up":
        Game.move_up(1)
    elif action == "down":
        Game.move_down(1)
    elif action == "left":
        Game.move_left(1)
    elif action == "right":
        Game.move_right(1)
    else:
        return

    r += Game.score
    return r


def maxQ(pos):
    max_value = None
    action = None
    for action_temp, value in Q[pos].items():
        if max_value is None or value > max_value:
            max_value = value
            action = action_temp

    return max_value, action


def updateQ(pos, action, Bellman_value):
    Q[pos][action] = Bellman_value
    print(Bellman_value)


def run():
    global discount

    time.sleep(1)
    while True:
        pos1 = Game.player
        max_value, action = maxQ(pos1)

        r = do_action(action)
        action_temp = action

        pos2 = Game.player
        max_value, action = maxQ(pos2)

        updateQ(pos1, action_temp, r + discount * max_value)

        # modify to change tempo
        time.sleep(0.05)


# creating thread for run()
Thread(target=run).start()

Game.start_game()
