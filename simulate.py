import placement
import arrays
import numpy as np
import pickle

# repeat: number of times to run placement
# n : number of routers
# density: 2-d matrix of device placement
# dimensions: 2-tuple which has size of room (meters)
# metric: desired number to optimize
# one_d: boolean, whether or not to place in one dimension
def optimal_placement(repeat, density, dimensions, n, metric, one_d):
    return min([placement.placement(density, dimensions, n, metric, one_d)
        for i in range(repeat)], key=lambda x: x.fun)

#samp_dist = np.array([[1, 1, 0],
#    [0, 0, 0],
#    [0, 0, 0],
#    [0, 0, 0],
#    [0, 0, 0],
#    [1, 1, 1],
#    [0, 0, 0],
#    [0, 0, 0],
#    [0, 0, 0],
#    [0, 0, 0]])

#a = np.random.randint(2, size=(5,10)).astype('uint8')
#a[0] =  8
#print(a)
#
#print(optimal_placement(50, a, (4, 100), 2, placement.throughput, one_d=False))

# in the interest of time, the running of results can be shortened by removing
# one of the things we are interested in (for example, removing power from the
# list of metrics
def simulate(repeat, test_distributions):
    return [[[[optimal_placement(repeat, a, arrays.s, routers, metric,
        one_d) for a in test_distributions] for routers in range(2, 5)] for metric
        in [placement.throughput, placement.power]] for one_d in [True, False]]

print('starting random clusters...')
random_clusters_results = simulate(10, arrays.random_clusters)
print('starting future results...')
future_results = simulate(10, arrays.future)
print('starting office hours...')
office_hours_results = simulate(10, arrays.office_hours)

with open('results.dat', 'wb') as f:
    pickle.dump((random_clusters_results, future_results, office_hours_results), f)

# fixed router positions...
fixed_positions = []
# the routers are fixed along the side of a wall
#fixed_results = [[[[metric(pos, a, (4, 100), True)] for pos in positions] for a in test_distributions] 
#    for metric in [placement.throughput, placement.power]]


# with open('results.dat', 'rb') as f:
#   loaded_results = pickle.load(f)
