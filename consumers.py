import salabim as sim
from operator import itemgetter
from globals import *


class ddgGenerator(sim.Component):
    def __init__(self, config={}):
        sim.Component.__init__(self)
        self.config = config

    def process(self):
        # Destructure the config dict
        gen_dist, base = itemgetter('gen_dist', 'base')(self.config)

        # Generate objects
        while True:
            DDG(self.config)
            yield self.hold(gen_dist.sample())


class DDG(sim.Component):
    def __init__(self, config):
        sim.Component.__init__(self)
        self.config = config
        # self.config.get('base').config.get('resource').print_info()

    def process(self):
        # Destructure the config dict
        _, base, n_consumed = itemgetter(
            'gen_dist', 'base', 'n_consumed')(self.config)

        if VERBOSE:
            print(f'DDG arrived, requesting {n_consumed} resources')

        # Enter the queue at the assigned base
        self.enter(base.config.get('queue'))
        if base.ispassive():
            base.activate()
            self.request((base.config.get('resource'), n_consumed))
        yield self.passivate()
