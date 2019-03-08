import numpy as np
import matplotlib.pyplot as plt
import math



def estimate_gaussian(X):
	m = X.shape[0]
	mu = sum(X)/m
	sigma2 = sum((X - mu)**2)/m
	return mu, sigma2


def compute_probability(X, mu, sigma2):
	X = np.exp(-np.power(X-mu,2)/(2*sigma2))/(math.sqrt(2*np.pi)*math.sqrt(sigma2))
	# return np.prod(X)
	return X



data_size = 50
X = np.random.uniform(10, size=data_size)
X = np.append(X,[12,14,13.5,0])
data_size += 4


mu, sigma2 = estimate_gaussian(X)
print("mu:", mu)
print("sigma2:", sigma2, "\n")


prob = compute_probability(X,mu,sigma2)


normal_distribution = np.array([X,prob]).T
# sort it by X column because matplotlib needs to know the order to connect dots correctly
normal_distribution = normal_distribution[normal_distribution[:,0].argsort()]
# print(normal_distribution, '\n')
print("Probability of x=2 is:", round(compute_probability(2,mu,sigma2),4), "%")


plt.plot(normal_distribution[:,0], normal_distribution[:,1], '-')
plt.xlim(xmin=0, xmax=14)
plt.show()