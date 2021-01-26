import salabim as sim
from operator import itemgetter
from globals import *

import crayons

verbose = VERBOSE_ALL or VERBOSE_SUPPLIERS


class SupplierGenerator(sim.Component):
    # def __init__(self, resource, n_supplied=1):
    def __init__(self, config={}):
        sim.Component.__init__(self)

        # Attach the config dict to self
        self.config = config

    def process(self):

        # Destructure config
        gen_dist, gen_time, n_supplied, env, base = itemgetter(
            'gen_dist', 'gen_time', 'n_supplied', 'env', 'base')(self.config)

        # Generate objects: If distribution is defined, overrides times
        if gen_dist:        # Generate based on distribution
            i = 1
            while i > 0:
                if verbose:
                    print(crayons.green(
                        f'{round(env.now(), 2)}: Generating a Supplier at {base.name} based on distribution:\n {gen_dist.print_info(as_str=True)}', bold=True))
                Supplier(self.config) if i > 1 else print(
                    'skipping generating Supplier on first loop')
                yield self.hold(gen_dist.sample())
                i += 1

        else:               # Generate at predefined times
            yield self.hold(gen_time.pop(0) - env.now())
            if verbose:
                print(crayons.green(
                    f'{round(env.now(), 2)}: Generating a Supplier at {base.name} based on time', bold=True))
            Supplier(self.config)
            while len(gen_time) > 0:
                yield self.hold(gen_time.pop(0) - env.now())
                if verbose:
                    print(crayons.green(
                        f'{round(env.now(), 2)}: Generating a Supplier based on time', bold=True))
                Supplier(self.config)


class Supplier(sim.Component):
    def __init__(self, config={}):
        sim.Component.__init__(self)
        self.config = config

    def process(self):

        # Destructure config
        n_supplied, base = itemgetter(
            'n_supplied', 'base')(self.config)
        if verbose:
            print(crayons.green(
                f'Supplier arrived, supplying {n_supplied} resources'))

        # Simulate unloading resources at base
        n_left_to_unload = self.config.get('n_supplied')
        while n_left_to_unload > 0:
            n_to_unload_this_period = min(
                SUPPLIER_UNLOAD_RATE, n_left_to_unload)
            print(crayons.yellow(n_to_unload_this_period))
            base.resource.set_capacity(
                base.resource.capacity() + n_to_unload_this_period)
            base.activate()
            n_left_to_unload -= n_to_unload_this_period
            yield self.hold(1)
