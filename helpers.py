import numpy as np
from math import sqrt


def euclidean_distance(array):
    dist = np.zeros((array.shape[0], array.shape[0]))
    for i in range(array.shape[0]):
        for j in range(array.shape[0]):
            dist[i, j] = sqrt((array[i] - array[j])**2)
    return dist

