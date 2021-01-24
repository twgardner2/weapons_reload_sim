# Resources, queues, etc.

import salabim as sim
from globals import *


fast_ERT = sim.Resource('fast_ERT', capacity=NUM_FAST_ERT)
fast_ERT.reload_time = FAST_ERT_RELOAD_TIME
slow_ERT = sim.Resource('slow_ERT', capacity=NUM_SLOW_ERT)
slow_ERT.reload_time = SLOW_ERT_RELOAD_TIME
