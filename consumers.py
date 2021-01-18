import salabim as sim
from operator import itemgetter
from globals import *


class ddgGenerator(sim.Component):
    def __init__(self, config={}):
        sim.Component.__init__(self)
        self.config = config

        # Debug
        if VERBOSE:
            print(f'creating a ddgGenerator, config: {config}')

    def process(self):
        # Destructure the config dict
        gen_dist, base = itemgetter('gen_dist', 'base')(self.config)

        # Generate objects
        i = 0
        while i > -1:
            DDG(self.config)
            yield self.hold(gen_dist.sample())
            i += 1


class DDG(sim.Component):
    def __init__(self, config={}):
        sim.Component.__init__(self)
        self.config = config
        # self.config.get('base').config.get('resource').print_info()

    def process(self):
        # Destructure the config dict
        _, base, n_consumed = itemgetter(
            'gen_dist', 'base', 'n_consumed')(self.config)

        # Debugging
        if VERBOSE:
            # print(f'DDG arrived, requesting {n_consumed} resources')
            # base.config.get('resource').print_info()
            print(base.config.get('resource').requesters().length())

        # Enter the queue for resources at the assigned base
        yield self.hold(base.config.get('reload_team').reload_time)
        yield self.request((base.config.get('resource'), n_consumed))
        yield self.passivate()
