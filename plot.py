import pickle
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

data = None
with open('results.dat', 'rb') as f:
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
plt.plot(np.median(clusters_floats[0,1], axis=1), label='clusters median 1d power')
plt.plot(np.median(clusters_floats[1,1], axis=1), label='clusters median 2d power')
plt.plot(np.median(future_floats[0,1], axis=1), label='future median 1d power')
plt.plot(np.median(future_floats[1,1], axis=1), label='future median 2d power')
plt.plot(np.median(office_floats[0,1], axis=1), label='office median 1d power')
plt.plot(np.median(office_floats[1,1], axis=1), label='office median 2d power')
plt.plot([-1.5] * 3, '#d1d3d6', label='2 ROUTERS, fixed placement, office')
plt.plot([-0.1] * 3, '#404449', label='2 Routers, fixed placement, office, WIFI')
plt.xlabel('Number of Routers')
plt.ylabel('Power (arbitrary units)')
plt.xticks(np.arange(3), np.arange(2, 5))
plt.legend()
plt.title("Power vs. Number of AP's")
plt.savefig('power.png')
plt.close()

# plot throughput
plt.plot(np.median(clusters_floats[0,0], axis=1), label='clusters median 1d throughput')
plt.plot(np.median(clusters_floats[1,0], axis=1), label='clusters median 2d throughput')
plt.plot(np.median(future_floats[0,0], axis=1), label='future median 1d throughput')
plt.plot(np.median(future_floats[1,0], axis=1), label='future median 2d throughput')
plt.plot(np.median(office_floats[0,0], axis=1), label='office median 1d throughput')
plt.plot(np.median(office_floats[1,0], axis=1), label='office median 2d throughput')
plt.xticks(np.arange(3), ('2 routers', '3 routers', '4 routers'))
plt.legend(loc=(0.25, 0.1))
plt.title("Throughput vs. Number of AP's")
plt.savefig('throughput.png')
plt.close()
