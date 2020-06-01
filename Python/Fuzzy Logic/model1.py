import numpy as np
from skfuzzy import control as ctrl
import pandas as pd


distance = ctrl.Antecedent(np.arange(0, 101, 1), 'distance')
angle = ctrl.Antecedent(np.arange(10, 80, 1), 'angle')

velocity = ctrl.Consequent(np.arange(0, 50, 1), 'velocity')

distance.automf(3)
angle.automf(3)
velocity.automf(3)

distance.view()
angle.view()
velocity.view()

rules = [
    ctrl.Rule(distance['good'], velocity['good']),
    ctrl.Rule(distance['average'] & angle['poor'], velocity['good']),
    ctrl.Rule(distance['average'] & angle['average'], velocity['average']),
    ctrl.Rule(distance['average'] & angle['good'], velocity['good']),
    ctrl.Rule(distance['poor'] & angle['poor'], velocity['average']),
    ctrl.Rule(distance['poor'] & angle['average'], velocity['poor']),
    ctrl.Rule(distance['poor'] & angle['good'], velocity['average']),
]

velocity_ctrl = ctrl.ControlSystem(rules)
velocity_sim = ctrl.ControlSystemSimulation(velocity_ctrl)


def test(data):
    d = data["d"]
    a = data["a"]
    v1 = data["v1"]

    # Comparing fuzzy predictions with real values (calculated from equation) for 'd' and 'a' only
    err_sum = 0
    for d_value, a_value, v1_value in zip(d, a, v1):
        a_value_normalized = round(a_value / (3.1415 / 2) * 90)  # convert radians to angle
        velocity_sim.input['distance'] = d_value
        velocity_sim.input['angle'] = a_value_normalized
        velocity_sim.compute()
        v1_predicted = velocity_sim.output['velocity']
        # print(d_value, a_value_normalized, v1_value, v1_predicted)
        err = round(abs(v1_value - v1_predicted), 2)
        # print("error: ", err)
        err_sum += err

    print("Error sum for {} data points: {:.2f}".format(len(d), err_sum))
    print("On average, fuzzy model was wrong by: {:.2f} m/s".format(err_sum / len(d)))


test(pd.read_csv("data_randomized.csv"))
