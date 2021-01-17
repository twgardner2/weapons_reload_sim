import salabim as sim


class takeGenerator(sim.Component):
    def __init__(self, resource, n_supplied=1):
        sim.Component.__init__(self)
        self.resource = resource
        self.n_supplied = n_supplied

    def process(self):
        while True:
            TAKE(self.resource, self.n_supplied)
            yield self.hold(sim.Uniform(5, 15).sample())


class TAKE(sim.Component):
    def __init__(self, resource, n_supplied):
        sim.Component.__init__(self)
        self.resource = resource
        self.n_supplied = n_supplied

    def process(self):
        self.resource.set_capacity(self.resource.capacity() + self.n_supplied)
        yield self.hold()


class ERT(sim.Component):
    def __init__(self, queue, reload_time):
        sim.Component.__init__(self)
        self.queue = queue
        self.reload_time = reload_time

    def process(self):
        while True:
            while len(self.queue) == 0:
                yield self.passivate()
            self.customer = self.queue.pop()
            yield self.hold(self.reload_time)
            self.customer.activate()
