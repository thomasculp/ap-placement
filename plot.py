import pickle
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('path')
args = vars(parser.parse_args())

path = args['path']

data = None
with open(path, 'rb') as f:
    data = pickle.load(f)

# lens(result)=3, stored as tuple of clusters, future, office_hours
clusters, future, office_hours = data

# these variables are going to hold the actual power/throughput
clusters_floats = np.empty(np.array(clusters).shape)
future_floats = np.empty(np.array(future).shape)
office_floats = np.empty(np.array(office_hours).shape)

# storing the actual power/throughput inside them
# the signs on all of the information were flipped to make use of the minimize
# operation. Here it is flipped back
for i, x in np.ndenumerate(clusters):
    clusters_floats[i] = -x.fun
for i, x in np.ndenumerate(future):
    future_floats[i] = -x.fun
for i, x in np.ndenumerate(office_hours):
    office_floats[i] = -x.fun

# plot power
fig = plt.figure(figsize=[7, 7])
ax = plt.subplot(111)

ax.plot(np.median(clusters_floats[0,1], axis=1), label='clusters median 1d power')
ax.plot(np.median(clusters_floats[1,1], axis=1), label='clusters median 2d power')
ax.plot(np.median(future_floats[0,1], axis=1), label='future median 1d power')
ax.plot(np.median(future_floats[1,1], axis=1), label='future median 2d power')
ax.plot(np.median(office_floats[0,1], axis=1), label='office median 1d power')
ax.plot(np.median(office_floats[1,1], axis=1), label='office median 2d power')
ax.plot([-1.5] * 5, '#d1d3d6', label='2 ROUTERS, fixed placement, office')
ax.plot([-0.1] * 5, '#404449', label='2 ROUTERS, fixed placement, office, WIFI')
plt.xlabel('Number of Routers')
plt.ylabel('Power (arbitrary log units)')
plt.xticks(np.arange(5), np.arange(2, 7))
plt.title("Median Power vs. Number of AP's")
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.3,  box.width, box.height * 0.7])
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.125))
plt.savefig('power.png')
plt.close()

# plot throughput
fig = plt.figure(figsize=[7, 7])
ax = plt.subplot(111)

ax.plot(np.median(clusters_floats[0,0], axis=1), label='clusters median 1d throughput')
ax.plot(np.median(clusters_floats[1,0], axis=1), label='clusters median 2d throughput')
ax.plot(np.median(future_floats[0,0], axis=1), label='future median 1d throughput')
ax.plot(np.median(future_floats[1,0], axis=1), label='future median 2d throughput')
ax.plot(np.median(office_floats[0,0], axis=1), label='office median 1d throughput')
ax.plot(np.median(office_floats[1,0], axis=1), label='office median 2d throughput')
ax.plot([0.00109769, 0.00164654, 0.00219539, 0.00274424, 0.00329308], '#d1d3d6', label='fixed placement, office')
ax.plot([0.00010977, 0.00016465, 0.00021954, 0.00027442, 0.00032931], '#404449', label='fixed placement, office, WIFI')
plt.xlabel('Number of Routers')
plt.ylabel('Throughput (arbitrary units)')
plt.xticks(np.arange(5), np.arange(2, 7))
plt.title("Median Throughput vs. Number of AP's")
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.3,  box.width, box.height * 0.7])
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.125))
plt.savefig('throughput.png')
plt.close()
