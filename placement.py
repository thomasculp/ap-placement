import numpy as np
import itertools
import scipy.optimize


# density: 2-dimensional matrix which contains number of devices in a cell which
#   has size (dimensions[0] / density.shape[0], dimensions[1] / density.shape[1])
# dimensions: 2-tuple which has size of room (in meters)
# n: number of 
# metric: desired number to maximize
def placement(density, dimensions, n, metric):
    guess = np.random.rand(2*n)
    bnds = [(0., 1.) for i in range(2*n)]
    print(guess)
    print(bnds)
    return scipy.optimize.minimize(fun=metric, x0=guess, args=(density, dimensions),
            bounds=bnds, method='TNC', options={'eps': 3*min(1./density.shape[0], 1./density.shape[1])})
# 'L-BFGS-B'

# assuming each router has the same amount of throughput, compute average
# throughput given positions of routers, density map, and dimensions.
# for partitioning, nearest router will be used
def throughput(positions, density, dimensions):
    # processing positions
    print(positions)
    positions = np.array([hard_sig(x) for x in positions]).reshape((len(positions)//2, 2))
    #positions = positions.reshape((len(positions)//2, 2))
    positions[:, 0] *= density.shape[0]
    positions[:, 1] *= density.shape[1]
    positions = positions.astype(int)
    print(positions)
    # creating a grid with position labels (distance from origin). offsetting by
    # half a unit to prevent log(0) issues.
    mesh = np.stack(np.mgrid[0:density.shape[0], 0:density.shape[1]], axis=-1).astype('float64')
    mesh[:, :, 0] += 0.5
    mesh[:, :, 1] += 0.5
    # the power that each antenna in the grid would receive from each router
    power = [0 for i in range(positions.shape[0])]
    for i, p in enumerate(positions):
        # computing distance by subtracting off the position of the router and taking
        # the norm
        dist = mesh - np.array([[p for i in range(density.shape[1])] for j in range(density.shape[0])])
        dist[:, :, 0] *= dimensions[0] / density.shape[0]
        dist[:, :, 1] *= dimensions[1] / density.shape[1]
        power[i] = np.log10(norm(dist))
    # taking the maximum over all the computed powers to get power received
    power = np.array(power)
    counts = np.zeros(len(positions))
    assignment = np.zeros(density.shape).astype(int)
    for i in range(power.shape[1]):
        for j in range(power.shape[2]):
            assignment[i,j] = np.argmax(power[:,i,j])
            counts[assignment[i,j]] += density[i,j]
    # creating an array of
    bandwidths = 1 / counts
    all_antennas_bandwidth = [[] for i in range(density.shape[0] * density.shape[1])]
    for i, x in np.ndenumerate(density):
        all_antennas_bandwidth[i[0] * density.shape[1] + i[1]] = np.full(x, bandwidths[assignment[i]])
    return -np.median(list(itertools.chain.from_iterable(all_antennas_bandwidth)))

# assuming each router and antenna has the same amount of power and directivity,
# compute average power given positions of routers, density map, and dimensions.
def power(positions, density, dimensions):
    # processing positions
    print(positions)
    positions = np.array([hard_sig(x) for x in positions]).reshape((len(positions)//2, 2))
    #positions = positions.reshape((len(positions)//2, 2))
    positions[:, 0] *= density.shape[0]
    positions[:, 1] *= density.shape[1]
    positions = positions.astype(int)
    print(positions)
    # creating a grid with position labels (distance from origin). offsetting by
    # half a unit to prevent log(0) issues.
    mesh = np.stack(np.mgrid[0:density.shape[0], 0:density.shape[1]], axis=-1).astype('float64')
    mesh[:, :, 0] += 0.5
    mesh[:, :, 1] += 0.5
    # the power that each antenna in the grid would receive from each router
    power = [0 for i in range(positions.shape[0])]
    for i, p in enumerate(positions):
        # computing distance by subtracting off the position of the router and taking
        # the norm
        dist = mesh - np.array([[p for i in range(density.shape[1])] for j in range(density.shape[0])])
        dist[:, :, 0] *= dimensions[0] / density.shape[0]
        dist[:, :, 1] *= dimensions[1] / density.shape[1]
        power[i] = np.log10(norm(dist))
    # taking the maximum over all the computed powers to get power received
    max_power = power[0]
    for i in range(1, len(power)):
        max_power = np.maximum(max_power, power[i])
    # creating an array of
    all_antennas_power = [[] for i in range(density.shape[0] * density.shape[1])]
    for i, x in np.ndenumerate(density):
        all_antennas_power[i[0] * density.shape[1] + i[1]] = np.full(x, max_power[i])
    return -np.median(list(itertools.chain.from_iterable(all_antennas_power)))


    #for  index, x in np.ndenumerate(density):

def hard_sig(x):
    if x > 1.:
        return 1.
    elif x < 0:
        return 0.
    else:
        return x


def norm(x):
    x2 = x ** 2
    return np.sqrt(x2[:, :, 0] + x2[:, :, 1])

# sample distribution:
samp_dist = np.array([[1, 1, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [1, 1, 1],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]])

a = np.random.randint(2, size=(5,10)).astype('uint8')
a[0] =  8
print(placement(a, (4, 100), 2, throughput))
