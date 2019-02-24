import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns



def plot_data_with_seaborn(X, y):
	DF = pd.DataFrame({'X':X, 'y':y})
	sns.set(style="darkgrid")
	sns.lmplot('X', 'y', data=DF, fit_reg=False, height=7, aspect=1.5)
	# plt.show()	


def compute_cost(X, y, theta):
	J = 0
	m = len(y)
	J = sum(np.power(np.dot(X, theta) - y, 2))/(2*m)
	return J


def gradientDescent(X, y, theta, alpha, num_iters):
	m = len(y)
	J_hist = np.zeros(num_iters)
	for i in range(num_iters):
		dot = np.dot(X, theta)	# multiplication result
		theta[0] = theta[0] - alpha*sum(dot - y)/m
		theta[1] = theta[1] - alpha*sum(np.multiply(dot - y, X[:,1].reshape(m,1)))/m

		J_hist[i] = compute_cost(X, y, theta)

	# print(J_hist)
	return theta



data = np.loadtxt("ex1data1.txt", delimiter=",", dtype="float")
X = data[:,0]
y = data[:,1]
m = len(X)	# number of training examples

# plot_data_with_seaborn(X,y)

# plt.figure(figsize=(10,6))
# plt.plot(X, y, ".")
# plt.show()


X = np.array([np.ones(m), X])
X = X.transpose()
y = y.reshape(m,1)


theta = np.array([[0],[0]], dtype=float)
J = compute_cost(X, y, theta)
print("Cost computed with theta [0, 0]:", J)

theta = np.array([[-1],[2]], dtype=float)
J = compute_cost(X, y, theta)
print("Cost computed with theta [-1, 2]:", J)


iterations = 1500
alpha = 0.01

print("\nRunning Gradient Descent ...\n")
theta = gradientDescent(X, y, theta, alpha, iterations);
print("Theta found by gradient descent:\n", theta)


line_y = np.dot(X,theta).reshape(m)
plt.figure(figsize=(10,6))
plt.plot(X[:,1], line_y)
plt.plot(X[:,1], y.reshape(m), ".")
plt.xlim(xmin=5, xmax=22)
plt.show()
