import salabim as sim

# Simulation Controls
TRACE = 1
SIM_LENGTH = 5000
SIM_SPEED = 250
ANIMATE = 1

# Debugging
VERBOSE_ALL = 0
VERBOSE_BASE = 0
VERBOSE_CONSUMERS = 1
VERBOSE_SUPPLIERS = 0

# DDG
# defining DDG_GENERATION_DIST overrides DDG_GENERATION_TIMES
# DDG_GENERATION_DIST = sim.Uniform(60, 110)
# DDG_GENERATION_DIST = sim.Normal(200, 60)
DDG_GENERATION_DIST = None
# DDG_GENERATION_TIMES = [3, 33, 333, 3333]
DDG_GENERATION_TIMES = list(range(1, 300, 50))
DDG_N_CONSUMED_DIST = sim.Uniform(20, 30)


# TAKEs
# TAKE_ARRIVAL_DIST = sim.Uniform(800, 1000)
TAKE_ARRIVAL_DIST = sim.Normal(800, 200)
TAKE_N_SUPPLIED = 200

# ERTs
NUM_FAST_ERT = 3
NUM_SLOW_ERT = 3

FAST_ERT_RELOAD_TIME = 15
SLOW_ERT_RELOAD_TIME = 30
