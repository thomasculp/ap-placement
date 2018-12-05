import pickle
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# sorry that this is so redundant, if it were really important for this to be
# programatically nice, i'd do it, but it's only 3 separate files...

# unpacking the pickled stuff
with open('clusters_results.dat', 'rb') as f:
    clusters = pickle.load(f)
with open('office_results.dat', 'rb') as f:
    office = pickle.load(f)
with open('future_results.dat', 'rb') as f:
    future = pickle.load(f)

# these guys are going to hold the actual power/throughput
clusters_floats = np.empty(clusters.shape)
office_floats = np.empty(office.shape)
future_floats = np.empty(future.shape)

# storing the actual power/throughput inside them
for i, x in np.ndenumerate(clusters):
    clusters_floats[i] = x.fun
for i, x in np.ndenumerate(office):
    office_floats[i] = x.fun
for i, x in np.ndenumerate(future):
    future_floats[i] = x.fun

# now that we just have data, we are good.

# here's how we can take a median across an axis:
# future_floats[0,0] is a 2d array because the original array was 4d.
# [0,0] means we are looking at one dimensional, throughput. the last 2 indices
# index the number of routers and different population distributions,
# respectively.
# thus, taking this median over axis=1 means we are taking the median over all
# the population distributions, meaning that we will get out 4 numbers in the
# array: median
# for 2 router, median for 3 routers, ..., median for 5 routers
np.median(future_floats[0, 0], axis=1)

# to plot some of this information, use plt:
# the following will create a line which gives the median throughput in the
# scenario for the one dimensional case. the x-axis will essentially be nubmer
# of routers (2, 3, 4, 5)
plt.plot(np.median(future_floats[0,0], axis=1), label='throughput vs. routers')
# this is kinda unnecessary here, but it'll change the x-axis labels
plt.xticks(np.arange(4), ('2 routers', '3 routers', '4 routers', '5 routers'))
# adds a legend (also unnecessary, but when you put on more than one line it'll
# keep track for you if you label your lines with label)
plt.legend()
plt.savefig('plot.png')

# if you want to make another plot, you should use
plt.close()
# that will erase everything on the figure.
