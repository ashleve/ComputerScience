import math
import random
import pandas as pd


g = 9.81
pi = 3.1415

num_of_data_points = 100

# distance up to 100m
d_range = 100
# angle from 10 to 80 degrees
a_range_start = pi * (10/180)
a_range = pi * (70/180)
# air resistance coefficient up to 0.1
k_range = 0.1
# mass up to 10 kg
m_range = 10


def calculate_d_a(d, a):
    x = d * g / math.sin(2*a)
    x = x if x > 0 else -x
    return round(math.sqrt(x), 2)


def calculate_d_a_k_m(d, a, k, m):
    # what is the equation ???????
    return 0


def main():
    # distance
    distances = [round(i/num_of_data_points*d_range, 2) for i in range(1, num_of_data_points + 1)]
    # angle (radians)
    angles = [round(i/num_of_data_points*a_range + a_range_start, 2) for i in range(1, num_of_data_points + 1)]
    # air resistance coefficient
    k_drags = [round(i/num_of_data_points*k_range, 2) for i in range(1, num_of_data_points + 1)]
    # mass
    masses = [round(i/num_of_data_points*m_range, 2) for i in range(1, num_of_data_points + 1)]

    # velocity for distance and angle only
    v1 = []
    # velocity for distance, angle, air resistance and mass
    v2 = []

    random.shuffle(distances)
    random.shuffle(angles)
    random.shuffle(k_drags)
    random.shuffle(masses)

    for d, a in zip(distances, angles):
        v1.append(calculate_d_a(d=d, a=a))
        # print("d: " + str(d), " a: " + str(a), " v: " + str(v1[-1]))

    for d, a, k, m in zip(distances, angles, k_drags, masses):
        v2.append(calculate_d_a_k_m(d=d, a=a, k=k, m=m))

    df = pd.DataFrame()
    df["d"] = distances
    df["a"] = angles
    df["k"] = k_drags
    df["m"] = masses
    df["v1"] = v1
    df["v2"] = v2
    df.to_csv("data_randomized.csv", index=False)

    print(df)


if __name__ == '__main__':
    main()
