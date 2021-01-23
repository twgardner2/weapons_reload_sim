# Resources, queues, etc.

import salabim as sim
from globals import *

# TLAMs resource is a shadow resource to track total inventory
# TLAMs1 and TLAMs2 will be supplied and consumed, all changes to them will be
# mirrored on TLAM
TLAMs = sim.Resource('TLAMs', 0)
TLAMs1 = sim.Resource('TLAMs1', 0)
TLAMs2 = sim.Resource('TLAMs2', 0)

queue1 = sim.Queue('queue1')  # TLAMs1
queue2 = sim.Queue('queue2')  # TLAMs2

fast_ERT = sim.Resource('fast_ERT', capacity=NUM_FAST_ERT)
fast_ERT.reload_time = FAST_ERT_RELOAD_TIME
slow_ERT = sim.Resource('slow_ERT', capacity=NUM_SLOW_ERT)
slow_ERT.reload_time = SLOW_ERT_RELOAD_TIME
