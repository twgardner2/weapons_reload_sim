import salabim as sim

### Simulation Controls ########################################################
TRACE = 1
SIM_LENGTH = 1000
SIM_SPEED = 8
ANIMATE = 1

### Debugging ##################################################################
VERBOSE_ALL = 1
VERBOSE_BASE = 1
VERBOSE_CONSUMERS = 0
VERBOSE_SUPPLIERS = 1


### Consumers ##################################################################
# defining CONSUMER_GENERATION_DIST overrides CONSUMER_GENERATION_TIMES
# CONSUMER_GENERATION_DIST = sim.IntUniform(60, 110)
CONSUMER_GENERATION_DIST = sim.Normal(100, 20)
# CONSUMER_GENERATION_DIST = None
# CONSUMER_GENERATION_TIMES = [3, 33, 333, 3333]
CONSUMER_GENERATION_TIMES = list(range(1, 300, 50))
# CONSUMER_N_CONSUMED_DIST = sim.IntUniform(8, 96)
CONSUMER_N_CONSUMED_DIST = sim.IntUniform(25, 25)


### Suppliers: #################################################################
# defining SUPPLIER_GENERATION_DIST overrides SUPPLIER_GENERATION_TIMES
SUPPLIER_GENERATION_DIST = sim.IntUniform(1200, 2000)
# SUPPLIER_GENERATION_DIST = None
SUPPLIER_GENERATION_TIMES = list(range(500, 5000, 500))

SUPPLIER_N_SUPPLIED = 1000
TAKE_N_SUPPLIED = 100
C5_N_SUPPLIED = 18
C17_N_SUPPLIED = 8
C130_N_SUPPLIED = 2

SUPPLIER_UNLOAD_RATE = 4  # resources/hour
### ERTs #######################################################################
# - make reload time be missiles/hour
NUM_FAST_ERT = 3
NUM_SLOW_ERT = 3

FAST_ERT_RELOAD_RATE = 4
SLOW_ERT_RELOAD_RATE = 2
