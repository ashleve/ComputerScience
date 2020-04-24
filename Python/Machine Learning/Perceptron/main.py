import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
from celluloid import Camera
from matplotlib.ticker import FuncFormatter


class Perceptron:

    def __init__(self, num_of_inputs=2, learning_rate=0.1, learning_rate_decay=0.0):
        self.num_of_inputs = num_of_inputs
        self.learning_rate = learning_rate
        self.learning_rate_decay = learning_rate_decay
        self.weights = None
        self.bias = None
        self.init_randomly()

    def init_randomly(self):
        self.weights = np.array([random.uniform(0, 1) for _ in range(self.num_of_inputs)])
        self.bias = random.uniform(0, 1)

    @staticmethod
    def activation_function(value):
        return 0 if value <= 0 else 1

    def predict(self, inputs):
        assert len(inputs) == len(self.weights)
        weighted_sum = sum(self.weights * inputs + self.bias)
        return Perceptron.activation_function(weighted_sum)

    def predict_for_many(self, data_points):
        return np.array([self.predict(point) for point in data_points])

    def execute_learning_epoch(self, train_x, train_y):
        predicted_labels = self.predict_for_many(train_x)
        errors = train_y - predicted_labels
        for error, data_point in zip(list(errors), train_x):
            self.weights += self.learning_rate * error * data_point
            self.bias += self.learning_rate * error


def split_dataset(dataset, ratio=0.8):
    mask = np.random.rand(len(dataset)) < ratio
    train_set = dataset[mask]
    test_set = dataset[~mask]
    return train_set, test_set


def main():
    data = pd.read_csv("data.csv", sep=";")
    train_set, test_set = split_dataset(data)
    print("Train set length:", len(train_set))
    print("Test set length:", len(test_set))

    train_set = train_set.to_numpy()
    test_set = test_set.to_numpy()

    train_x, train_y = train_set[:, 0:2], train_set[:, 2]
    test_x, test_y = test_set[:, 0:2], test_set[:, 2]


    sns.set_style("darkgrid")
    fig = plt.figure()
    camera = Camera(fig)

    num_of_epochs = 100
    learning_rate = 1
    learning_rate_decay = learning_rate / num_of_epochs
    perceptron = Perceptron(learning_rate=learning_rate, learning_rate_decay=learning_rate_decay)
    history = []
    for i in range(num_of_epochs):
        predicted = perceptron.predict_for_many(test_x)
        error = sum(np.abs(predicted - test_y)) / len(test_set) * 100
        history.append(100.00 - error)
        print("Epoch:", i)
        print("Error: {:.2f}%".format(error))
        print("Learning rate: {:.2f}".format(perceptron.learning_rate))
        print()

        # This will create a video visualizing learning
        df = pd.DataFrame({"x": test_x[:, 0], "y": test_x[:, 1], "label": predicted})
        sns.scatterplot(x="x", y="y", data=df, hue="label", legend=False, size=1)
        plt.title(
            "Predictions of single perceptron on test set",
            loc='left',
            fontsize=16,
            fontweight=0,
            color='orange'
        )
        plt.text(-1, 0.8,
                 "Epoch: {}   \n".format(i) +
                 "Error: {:.2f}%".format(error),
                 fontsize=14,
                 color="black",
                 bbox=dict(facecolor='red', alpha=1))
        # plot line
        x = [-1, 1]
        y = [0.5*(-1)-0.2, 0.5*1-0.2]   # the line coefficients are hardcoded
        plt.plot(x, y, '-', color="red")
        camera.snap()

        # print(perceptron.weights)
        perceptron.execute_learning_epoch(train_x, train_y)
        perceptron.learning_rate *= 1 - perceptron.learning_rate_decay  # adaptywny wspolczynnik uczenia!

    animation = camera.animate()
    animation.save('perceptron_learning_visualization.mp4', writer='ffmpeg', fps=1, dpi=500)

    plt.close()
    fig, ax = plt.subplots()
    ax.plot(history)
    plt.title("The learning of single perceptron on 8000 data points")
    plt.ylabel("Test set accuracy")
    plt.xlabel("Epoch")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda acc, _: '{:.0%}'.format(acc/100)))
    plt.savefig("test_set_accuracy_plot.png")
    plt.show()


if __name__ == "__main__":
    main()
