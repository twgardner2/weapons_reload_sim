# Resources, queues, etc.

import salabim as sim

# TLAMs resource is a shadow resource to track total inventory
# TLAMs1 and TLAMs2 will be supplied and consumed, all changes to them will be
# mirrored on TLAM
TLAMs = sim.Resource("TLAMs", 0)
TLAMs1 = sim.Resource("TLAMs", 0)
TLAMs2 = sim.Resource("TLAMs", 0)

queue1 = sim.Queue("queue1")  # TLAMs1
queue2 = sim.Queue("queue2")  # TLAMs2


class Base(sim.Component):
    def __init__(self, config={}):
        sim.Component.__init__(self)
        self.config = config
        print(self.config)

    def process(self):
        while True:
            print(self.config)
            yield self
