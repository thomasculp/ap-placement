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
