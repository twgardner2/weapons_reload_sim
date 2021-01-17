import salabim as sim


class ddgGenerator(sim.Component):
    def __init__(self, queue, resource, mean_time=30):
        sim.Component.__init__(self)
        self.queue = queue
        self.resource = resource
        self.mean_time = mean_time

    def process(self):
        while True:
            DDG(self.queue, self.resource)
            yield self.hold(sim.Normal(int(self.mean_time), 2).sample())


class DDG(sim.Component):
    def __init__(self, queue, resource):
        sim.Component.__init__(self)
        self.queue = queue
        self.resource = resource
        # print(self.queue.reload_team)

    def process(self):
        self.enter(self.queue)
        # yield self.hold(sim.Uniform(5, 15).sample())
        yield self


# sim.ComponentGenerator(con.DDG, duration=5000, number=521, queue=queue1)
