import placement
import numpy as np
import pickle

# repeat: number of times to run placement
# n : nubmer of routers
# density: 2-d matrix of device placement
# dimensions: 2-tuple which has size of room (meters)
# metric: desired number to optimize
# one_d: boolean, whether or not to place in one dimension
def optimal_placement(repeat, density, dimensions, n, metric, one_d):
    return min([placement.placement(density, dimensions, n, metric, one_d)
        for i in range(repeat)], key=lambda x: x.fun)

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
print(a)

print(optimal_placement(50, a, (4, 100), 2, placement.throughput, one_d=False))

# put list of distributions here:
test_distributions = []
# in the interest of time, the running of results can be shortened by removing
# one of the things we are interested in (for example, removing power from the
# list of metrics
results = [[[[optimal_placement(50, a, (4, 100), routers, metric,
    one_d) for a in test_distributions] for routers in range(2, 5)] for metric
    in [placement.throughput, placement.power]] for one_d in [True, False]]

with open('results.dat', 'wb') as f:
    pickle.dump(results, f)

# with open('results.dat', 'rb') as f:
#   loaded_results = pickle.load(f)
