from matplotlib.image import imread
import matplotlib.pyplot as plt

X = imread('mandrill-small.tiff')

import random
import numpy as np

def rgbKmeans(K, X):
    # preprecessing
    sizex = len(X)
    sizey = len(X[0])
    c = np.zeros((sizex, sizey), np.int)
    u = np.zeros((K, 3), np.int)
    
    # initialize cluster centroids randomly
    interval = range(sizex * sizey - 1)
    samples = random.sample(interval, K)
    for i in range(K):
        x = samples[i] / sizey
        y = samples[i] % sizey
        u[i] = X[x][y]
    
    # repeat until convergence
    measure = 1
    pre = 100
    after = 0
    while (pre - after > measure) | (after - pre > measure):
        # step 1
        for i in range(sizex):
            for j in range(sizey):
                minBias = 999999999999
                argmin = 0
                for k in range(K):
                    dist = 0
                    for l in range(3):
                        dist = dist + (X[i, j, l] - u[k][l]) ** 2
                    if dist < minBias:
                        minBias = dist
                        argmin = k
                c[i, j] = argmin
        # step 2
        for k in range(K):
            numerator = [0] * 3
            denominator = 0
            for i in range(sizex):
                for j in range(sizey):
                    if c[i, j] == k:
                        for l in range(3):
                            numerator[l] = numerator[l] + X[i, j, l]
                        denominator = denominator + 1
            u[k] = [n / float(denominator) for n in numerator]
        # step 3
        pre = after
        after = J(c, u, X)
        print after
    return [c, u]
def J(c, u, X):
    sizex = len(X)
    sizey = len(X[0])
    sums = 0
    for i in range(sizex):
        for j in range(sizey):
            for k in range(3):
                sums = sums + ((X[i, j, k] - u[c[i, j], k]) ** 2)
    return sums

[c, u] = rgbKmeans(16, X)

# Plot the result image
sizex = len(X)
sizey = len(X[0])
X_2 = np.zeros((sizex, sizey, 3), np.int)
for i in range(sizex):
    for j in range(sizey):
        X_2[i, j] = u[c[i, j]]
plt.imshow(X_2)
plt.show()
