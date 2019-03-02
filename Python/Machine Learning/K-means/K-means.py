import numpy as np
import random
import matplotlib.pyplot as plt


def init_centroids(X, K):
    centroids = np.random.permutation(X)[:K]
    return centroids


def compute_distance(p1, p2):
    n = p1.shape[0]
    dist = []
    for i in range(n):
        dist.append((p1[i]-p2[i])**2)
    dist = sum(dist)/n

    return dist


def find_closeset_centroids(X, init_centroids):
    K = init_centroids.shape[0]
    m = X.shape[0]
    idx = np.arange(m).reshape(m, 1)

    for i in range(m):
        min_dist = None
        for j in range(K):
            dist = compute_distance(X[i, :], init_centroids[j, :])
            if min_dist == None or dist < min_dist:
                min_dist = dist
                idx[i] = j

    return idx


def compute_centroids(X, idx, K):
    m, n = X.shape
    centroids = np.zeros((K, n))
    dividers = np.zeros(K)
    for i in range(m):
        centroids[idx[i, 0], :] += X[i, :]
        dividers[idx[i, 0]] += 1

    for i in range(K):
        if dividers[i] != 0:
            centroids[i, :] /= dividers[i]

    return centroids


m = 250  # number of points
x = [random.uniform(1, 10) for i in range(m)]
y = [random.uniform(1, 10) for i in range(m)]

X = np.array([x, y]).round(2).T
# alternative:
# X = np.random.randn(20,2)
# plt.plot(X[:,0], X[:,1], '.', markersize=10)


K = 5  # number of clusters
centroids = init_centroids(X, K)


# show initial points and centroid
plt.figure(figsize=(10, 6))
plt.plot(X[:, 0], X[:, 1], '.')
plt.plot(centroids[:, 0], centroids[:, 1], '.', marker='$o$', markersize=12, color='red', markeredgewidth=0.01)
plt.show()


plt.figure(figsize=(10, 6))
colors = ['green', 'blue', 'red', 'orange', 'purple', 'yellow', 'magenta']
for i in range(K):
    plt.plot(centroids[i, 0], centroids[i, 1], '.', marker='$o$', markersize=12, color=colors[i], markeredgewidth=0.01)


# compute
iterations = 15
for i in range(iterations):
    print("iteration:", i)
    idx = find_closeset_centroids(X, centroids)
    centroids = compute_centroids(X, idx, K)
    print(centroids, '\n')


# plot results
for i in range(m):
    plt.plot(X[i, 0], X[i, 1], '.', color=colors[idx[i, 0]])
for i in range(K):
    plt.plot(centroids[i, 0], centroids[i, 1], '.', marker='x', markersize=12, color=colors[i], markeredgewidth=2)
plt.show()
