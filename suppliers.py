import salabim as sim
from operator import itemgetter
from globals import *


class takeGenerator(sim.Component):
    # def __init__(self, resource, n_supplied=1):
    def __init__(self, config={}):
        sim.Component.__init__(self)

        # Attach the config dict to self
        self.config = config
        # self.resource = resource
        # self.n_supplied = n_supplied

    def process(self):

        # Destructure config
        arrival_dist, resource, n_supplied = itemgetter(
            'arrival_dist', 'resource', 'n_supplied')(self.config)

        # Generate objects
        while True:
            TAKE(resource, n_supplied)
            yield self.hold(arrival_dist.sample())


class TAKE(sim.Component):
    def __init__(self, resource, n_supplied):
        sim.Component.__init__(self)
        self.resource = resource
        self.n_supplied = n_supplied

    def process(self):
        print(f'TAKE arrived, supplying {self.n_supplied} resources')
        self.resource.set_capacity(self.resource.capacity() + self.n_supplied)
        # self.resource.set_capacity(self.resource.capacity() + 0)
        yield self.hold()


# class ERT(sim.Component):
#     def __init__(self, queue, reload_time):
#         sim.Component.__init__(self)
#         self.queue = queue
#         self.reload_time = reload_time

#     def process(self):
#         while True:
#             while len(self.queue) == 0:
#                 yield self.passivate()
#             self.customer = self.queue.pop()
#             yield self.hold(self.reload_time)
#             self.customer.activate()
