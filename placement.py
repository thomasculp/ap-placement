import numpy as np
import itertools
import scipy.optimize


# density: 2-dimensional matrix which contains number of devices in a cell which
#   has size (dimensions[0] / density.shape[0], dimensions[1] / density.shape[1])
# dimensions: 2-tuple which has size of room (in meters)
# n: number of 
# metric: desired number to maximize
def placement(density, dimensions, n, metric, one_d=False):
    if not one_d:
        n = 2 * n
    # guess for where the routers should be placed (random)
    guess = np.random.rand(n)
    # the domain is the unit box in R^n
    bnds = [(0., 1.) for i in range(n)]
    print(guess)
    print(bnds)
    # eps is the step size the algorithm takes to estimate the jacobian. it needs to
    # take a step at least the size of the grid length in order to see any
    # change (any smaller and steps will be within the same box on the grid)
    # the method for optimization was picked arbitrarily...
    return scipy.optimize.minimize(fun=metric, x0=guess, args=(density, dimensions, one_d),
            bounds=bnds, method='TNC', options={'eps': 2*min(1./density.shape[0], 1./density.shape[1])})
# 'L-BFGS-B'

# assuming each router has the same amount of throughput, compute average
# throughput given positions of routers, density map, and dimensions.
# for partitioning, nearest router will be used
def throughput(positions, density, dimensions, one_d):
    # processing positions
    print(positions)
    # putting the input through a rectifier to get valid numbers in (0, 1). in the
    # case of one dimension, converting the one number to a coordinate along the
    # perimeter of the room. for two dimensions, doing the expected thing...
    if one_d:
        positions = np.array([to_coords(x, density.shape) for x in [hard_sig(x) for x in positions]])
    else:
        positions = np.array([hard_sig(x) for x in positions]).reshape((len(positions)//2, 2))
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
    # for each position in the density array, computing which router gives the
    # most power. this determines which router that position will get data from.
    # adding the density to counts so that average throughput for all devices
    # connected to the router can be computed later.
    # assignment keeps track of which position in the density grid gets which router
    power = np.array(power)
    counts = np.zeros(len(positions))
    assignment = np.zeros(density.shape).astype(int)
    for i in range(power.shape[1]):
        for j in range(power.shape[2]):
            assignment[i,j] = np.argmax(power[:,i,j])
            counts[assignment[i,j]] += density[i,j]
    # the total throughput to each router is just normalized to 1, so taking the
    # reciprocal of counts gives the percentage of throughput each
    # device connected to that router receives
    bandwidths = 1 / counts
    # this process puts the throuput each device in the grid receives into an array
    # and then takes the median of that array.
    all_antennas_bandwidth = [[] for i in range(density.shape[0] * density.shape[1])]
    for i, x in np.ndenumerate(density):
        all_antennas_bandwidth[i[0] * density.shape[1] + i[1]] = np.full(x, bandwidths[assignment[i]])
    # the result is negated so that scipy.optimize.minimize will find the maximum
    return -np.median(list(itertools.chain.from_iterable(all_antennas_bandwidth)))


# assuming each router and antenna has the same amount of power and directivity,
# compute average power given positions of routers, density map, and dimensions.
def power(positions, density, dimensions, one_d):
    # processing positions
    print(positions)
    # putting the input through a rectifier to get valid numbers in (0, 1). in the
    # case of one dimension, converting the one number to a coordinate along the
    # perimeter of the room. for two dimensions, doing the expected thing...
    if one_d:
        positions = np.array([to_coords(x, density.shape) for x in [hard_sig(x) for x in positions]])
    else:
        positions = np.array([hard_sig(x) for x in positions]).reshape((len(positions)//2, 2))
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
    # this process puts the throuput each device in the grid receives into an array
    # and then takes the median of that array.
    all_antennas_power = [[] for i in range(density.shape[0] * density.shape[1])]
    for i, x in np.ndenumerate(density):
        all_antennas_power[i[0] * density.shape[1] + i[1]] = np.full(x, max_power[i])
    # the result is negated so that scipy.optimize.minimize will find the maximum
    return -np.median(list(itertools.chain.from_iterable(all_antennas_power)))


# the identity function for 0 < x < 1. otherwise this is saturated at 0 or 1
# 1                                 -----------------------
#                                 /
#                               /
#                             /
#                           /
# 0 -----------------------
#                         0       1
def hard_sig(x):
    if x > 1.:
        return 1.
    elif x < 0:
        return 0.
    else:
        return x

# computing the distance from the origin
def norm(x):
    x2 = x ** 2
    return np.sqrt(x2[:, :, 0] + x2[:, :, 1])


# converting a one-dimensional coordinate to a two dimensional coordinate along
# the perimeter of the density grid.
# u has already been normalized: u \in (0, 1)
def to_coords(u, shape):
    p = 2 * (shape[0] + shape[1])
    length = u * p
    if length < shape[0]:
        return [int(length), 0]
    elif length < shape[0] + shape[1]:
        return [shape[0] - 1, int(length - shape[0])]
    elif length < 2 * shape[0] + shape[1]:
        return [int(shape[0] - (length - shape[0] - shape[1])), shape[1] - 1]
    else:
        return [0, int(p - length)]


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
print(placement(a, (4, 100), 2, throughput, one_d=True))
