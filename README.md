# Some background on the structure of the code

`placement.py` is a module containing code that will place routers in optimal
locations according to the metrics `throughput` and `power`. The key method in
this module is `placement` which takes a 2D matrix which describes device
population, the size of the room, the number of routers to be placed, which
metric to be optimized, whether the routers should be placed on the perimeter of
the room or anywhere on the grid, and placed routers which will not be moved
(this last argument was useful for another idea, but was ultimately abandoned. See
the note on `placement_2` below. The
default argument is used for the results presented in the paper).

`placement` is run by `optimal_placement` which just runs `placement`
`repeat`-many times and takes the results which maximizes the metric.
`optimal_placement` is run by `simulate` which just uses `optimal_placement`
over different configurations (different number of routers, 2D vs. 1D placement,
different population scenarios, and the different metrics).

Any other functions below the functions described just supports the above
functions in some capacity.

(`simulate_2` and `placement_2` were just different ideas to get an optimal
placement. It was found that `placement` worked better, so these functions
are really just vestiges now which don't affect anything, but are left in the
code to illustrate a different approach to the problem. `simulate_2.py` can be
ignored as well).

# Population scenarios

`arrays.py` contains the population scenarios used in the code. These are just
some ideas on possible population densities. These can be changed by just
changing what is fed into `placement` or one of the higher-level methods which
calls it, like `simulate`. This advice holds for introducing new metrics or
other ways of looking at the problem of router placement.

# Running the code

`simulate.py` is run as

`simulate.py path repeat`

where `path` is the file that the data from the simulations will be saved to and `repeat` is the number of times that a local maximum will be found for a
given simulated population (repeating more will probably yield a better result
as a global maximum is more likely to be found).

The output is a file which is a pickled array (using Python's `pickle`). The
structure of the array can be understood by just looking at the `plot.py`
plotting routine. It doesn't need to be understood in order to see results,
though. To see the results generated from running `simulate.py`, run

`plot.py path`

where `path` is the output file from `simulate.py`. You will get images named
`power.png` and `throughput.png`, samples of which are included.

