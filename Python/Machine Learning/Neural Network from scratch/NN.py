import numpy as np
import scipy.io


def sigmoid(data):
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            data[i][j] = 1 / (1+np.exp(-data[i][j]))
    return data


def nn_cost_function(nn_params, input_layer_size, hidden_layer_size, num_labels, X, y, lamb):
    m = X.shape[0]

    Theta1 = nn_params[0]
    Theta2 = nn_params[1]

    # Feed forward
    zeros = np.ones(m)[:, np.newaxis]
    hidden_layer_z = np.dot(np.concatenate((zeros, X), axis=1), np.transpose(Theta1))
    hidden_layer_a = np.concatenate((zeros, sigmoid(hidden_layer_z)), axis=1)
    output_layer = sigmoid(np.dot(hidden_layer_a, np.transpose(Theta2)))

    # Transform vertical vector y to logical array (for example [7] becomes [0,0,0,0,0,0,0,1,0,0])
    y_logical = np.zeros((m, num_labels))
    for i in range(m):
        y_logical[i][y[i]-1] = 1

    # Compute cost
    J = -np.sum(np.multiply(y_logical, np.log(output_layer)) +
                np.multiply((1-y_logical), np.log(1-output_layer))) / m

    return J


mat = scipy.io.loadmat('ex4data1.mat')
X = mat['X']
y = mat['y']
m = X.shape[0]

weights = scipy.io.loadmat('ex4weights.mat')
Theta1 = weights['Theta1']
Theta2 = weights['Theta2']
# print(Theta2)
# nn_params = np.array([Theta1.reshape(Theta1.size,order='F'), Theta2.reshape(Theta2.size,order='F')])
# print(nn_params[1].shape)

nn_params = [Theta1, Theta2]

lamb = 0  # lambda
input_layer_size = X.shape[1]
hidden_layer_size = 25
num_labels = 10

J = nn_cost_function(
    nn_params,
    input_layer_size,
    hidden_layer_size,
    num_labels,
    X, y, lamb
)

print("Computed Cost for initial Thetas:", J)
