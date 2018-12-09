import placement
import arrays
import numpy as np
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('path')
parser.add_argument('repeat', type=int)
args = vars(parser.parse_args())

path = args['path']
repeat = args['repeat']

print('starting random clusters...')
random_clusters_results = placement.simulate(repeat, arrays.random_clusters)
print('starting future results...')
future_results = placement.simulate(repeat, arrays.future)
print('starting office hours...')
office_hours_results = placement.simulate(repeat, arrays.office_hours)

with open(path, 'wb') as f:
    pickle.dump((random_clusters_results, future_results, office_hours_results), f)

# fixed router positions...
fixed_positions = []
# the routers are fixed along the side of a wall
#fixed_results = [[[[metric(pos, a, (4, 100), True)] for pos in positions] for a in test_distributions] 
#    for metric in [placement.throughput, placement.power]]


# with open('results.dat', 'rb') as f:
#   loaded_results = pickle.load(f)
