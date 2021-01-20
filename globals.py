import salabim as sim

# Debugging
VERBOSE_ALL = 1
VERBOSE_BASE = 0
VERBOSE_CONSUMERS = 0
VERBOSE_SUPPLIERS = 0

# DDG
DDG_ARRIVAL_DIST = sim.Uniform(60, 110)
DDG_N_CONSUMED = sim.Uniform(20)


# TAKEs
TAKE_ARRIVAL_DIST = sim.Uniform(700, 1000)
TAKE_N_SUPPLIED = 8 * 36

# ERTs
NUM_FAST_ERT = 3
NUM_SLOW_ERT = 3

FAST_ERT_RELOAD_TIME = 55
SLOW_ERT_RELOAD_TIME = 20
