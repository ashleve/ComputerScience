import numpy as np
from skfuzzy import control as ctrl
import pandas as pd


distance = ctrl.Antecedent(np.arange(0, 101, 1), 'distance')
angle = ctrl.Antecedent(np.arange(10, 80, 1), 'angle')
k_drag = ctrl.Antecedent(np.arange(0, 0.11, 0.01), 'k_drag')
mass = ctrl.Antecedent(np.arange(0, 11, 1), 'mass')

velocity = ctrl.Consequent(np.arange(0, 50, 1), 'velocity')

distance.automf(3)
angle.automf(3)
k_drag.automf(3)
mass.automf(3)
velocity.automf(3)

distance.view()
angle.view()
k_drag.view()
mass.view()
velocity.view()

rules = [
    ctrl.Rule(distance['good'], velocity['good']),

    ctrl.Rule(distance['average'] & angle['poor'], velocity['good']),
    ctrl.Rule(distance['average'] & angle['average'] & (mass['poor'] | mass['average']) & k_drag['good'], velocity['good']),
    ctrl.Rule(distance['average'] & angle['average'] & mass['good'] & k_drag['good'], velocity['average']),
    ctrl.Rule(distance['average'] & angle['good'], velocity['good']),

    ctrl.Rule(distance['poor'] & angle['poor'], velocity['average']),
    ctrl.Rule(distance['poor'] & angle['average'] & (mass['poor'] | mass['average']) & k_drag['good'],velocity['average']),
    ctrl.Rule(distance['poor'] & angle['average'] & mass['good'] & k_drag['good'], velocity['poor']),
    ctrl.Rule(distance['poor'] & angle['good'], velocity['average']),
]

velocity_ctrl = ctrl.ControlSystem(rules)
velocity_sim = ctrl.ControlSystemSimulation(velocity_ctrl)


def test(data):
    d = data["d"]
    a = data["a"]
    k = data["k"]
    m = data["m"]
    v2 = data["v2"]

    # Comparing fuzzy predictions with real values (calculated from equation) for 'd', 'a', 'k', 'm'
    err_sum = 0
    for d_value, a_value, k_value, m_value, v2_value in zip(d, a, k, m, v2):
        a_value_normalized = round(a_value / (3.1415 / 2) * 90)  # convert radians to angle
        velocity_sim.input['distance'] = d_value
        velocity_sim.input['angle'] = a_value_normalized
        velocity_sim.input['k_drag'] = k_value
        velocity_sim.input['mass'] = m_value
        velocity_sim.compute()
        v1_predicted = velocity_sim.output['velocity']
        err = round(abs(v2_value - v1_predicted), 2)
        err_sum += err

    print("Error sum for {} data points: {:.2f}".format(len(d), err_sum))
    print("On average, fuzzy model was wrong by: {:.2f} m/s".format(err_sum / len(d)))


test(pd.read_csv("data_randomized.csv"))
