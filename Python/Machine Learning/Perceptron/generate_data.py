import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


NUM_OF_DATA_POINTS = 10000
MAX_X_RANGE = 1
MIN_X_RANGE = -1
MAX_Y_RANGE = 1
MIN_Y_RANGE = -1

A = 0.5
B = -0.2


def calculate_linear_function(x):
    return A * x + B


X = []
Y = []
LABELS = []
for i in range(NUM_OF_DATA_POINTS):
    x = random.uniform(MIN_X_RANGE, MAX_X_RANGE)
    y = random.uniform(MIN_Y_RANGE, MAX_Y_RANGE)
    label = 0 if calculate_linear_function(x) < y else 1
    X.append(x)
    Y.append(y)
    LABELS.append(label)


df = pd.DataFrame()
df["x"] = X
df["y"] = Y
df["label"] = LABELS

print(df)

# plot points
sns.set_style("darkgrid")
sns.scatterplot(x="x", y="y", data=df, hue="label")

# plot line
x = [-1, 1]
y = [calculate_linear_function(-1), calculate_linear_function(1)]
plt.plot(x, y, '-', color="red")

plt.show()

df.to_csv("data.csv", sep=';', index=False)
