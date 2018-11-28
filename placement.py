import numpy as np
import scipy.optimize


# density: 2-dimensional matrix which contains number of devices in a cell which
#   has size (dimensions[0] / density.shape[0], dimensions[1] / density.shape[1])
# dimensions: 2-tuple which has size of room (in meters)
# n: number of 
# metric: desired number to maximize
def placement(density, dimensions, n, metric):


# assuming each router has the same amount of throughput, compute average
# throughput given positions of routers, density map, and dimensions.
# for partitioning, nearest router will be used
def throughput():
    pass

# assumin each router and antenna has the same amount of power and directivity,
# compute average power given positions of routers, density map, and dimensions.
def power(density, dimensions, positions):
    mesh = np.stack(np.mgrid[0:density.shape[0], 0:density.shape[1]], axis=-1)
    mesh[:, :, 0] += 0.5
    mesh[:, :, 1] += 0.5
    (dimensions / density.shape[1])
    for p in positions:
        dist = mesh - np.array([[p for i in range(density.shape[0])] for j in range(density.shape[1])])
        dist[:, :, 0] *= dimensions[0] / density.shape[0]
        dist[:, :, 1] *= dimensions[1] / density.shape[1]
        loglengths = np.log10(norm(dist))

    for  index, x in np.ndenumerate(density):

def norm(x):
    x2 = x ** 2
    return np.sqrt(x2[:, :, 0] + x2[:, :, 1])

