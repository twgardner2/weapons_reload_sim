import salabim as sim
from operator import itemgetter
from globals import *

import crayons as cr

verbose = VERBOSE_ALL or VERBOSE_SUPPLIERS
cprint = MAKE_CPRINT(verbose, VERBOSE_SUPPLIERS_COLOR)
cprint(f"suppliers.py verbose output ON")


class Supplier_Config():
    def __init__(self, supplier_type, config={}):
        if supplier_type is None:
            raise Exception('You must pass "supplier_type"')
        if 'base' not in config and 'env' not in config:
            raise Exception('You must pass "env" and "base"')
        if 'base' not in config:
            raise Exception('You must pass "base"')
        if 'env' not in config:
            raise Exception('You must pass "env"')

        n_supplied_dict = {
            'TAKE': TAKE_N_SUPPLIED,
            'NGLS': NGLS_N_SUPPLIED,
            'C5': C5_N_SUPPLIED,
            'C17': C17_N_SUPPLIED,
            'C130': C130_N_SUPPLIED,
        }

        gen_dist_dict = {
            'TAKE': sim.Normal(12 * 24, 2 * 24),
            'NGLS': sim.IntUniform(800, 1000),
            'C5': sim.IntUniform(0.5 * 24, 1 * 24),
            'C17': sim.IntUniform(0.5 * 24, 1 * 24),
            'C130': sim.IntUniform(0.5 * 24, 1 * 24),
        }

        default_config = {
            'type': supplier_type,
            'description': f'{supplier_type} supplying {config["base"]}',
            'n_supplied': n_supplied_dict[supplier_type],
            'gen_dist': gen_dist_dict[supplier_type],
            'gen_time': SUPPLIER_GENERATION_TIMES.copy(),
        }

        if 'gen_time' in config:
            default_config['gen_dist'] = None

        self.config = {**default_config, **config}


class SupplierGenerator(sim.Component):
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
                cprint(
                    f'{round(env.now(), 2)}: Generating a Supplier at {base.name} based on distribution:\n {gen_dist.print_info(as_str=True)}')
                Supplier(self.config) if i > 1 else cprint(
                    'skipping generating Supplier on first loop')
                yield self.hold(gen_dist.sample())
                i += 1

        else:               # Generate at predefined times
            yield self.hold(gen_time.pop(0) - env.now())
            cprint(
                f'{round(env.now(), 2)}: Generating a Supplier at {base.name} based on time')
            Supplier(self.config)
            while len(gen_time) > 0:
                yield self.hold(gen_time.pop(0) - env.now())
                cprint(
                    f'{round(env.now(), 2)}: Generating a Supplier based on time')
                Supplier(self.config)


class Supplier(sim.Component):
    def __init__(self, config={}):
        sim.Component.__init__(self)
        self.config = config

        if OUTPUT:
            with open(OUTPUT_DIR + OUTPUT_SUBDIR + QUEUE_OUTPUT_FILE, 'a') as f:
                f.write(
                    # f'{self.config["env"].now()},{self.config["base"].config["name"]},supplier_arrived,{self.config["n_supplied"]},NA\n')
                    f'{self.config["env"].now()},{self.config["base"].config["name"]},supplier_arrived,NA,{self.config["type"]}, {self.config["n_supplied"]}\n')

    def process(self):

        # Destructure config
        n_supplied, base, env = itemgetter(
            'n_supplied', 'base', 'env')(self.config)
        cprint(f'Supplier arrived, supplying {n_supplied} resources')

        # Enter supplier queue at base
        cprint(f'{self} entering supplier queue at {self.config.get("base")}')
        self.enter(self.config.get('base').supplier_queue)

        # Simulate unloading resources at base
        n_left_to_unload = self.config.get('n_supplied')
        while n_left_to_unload > 0:
            if is_daytime(env.now()):
                n_to_unload_this_period = min(
                    SUPPLIER_UNLOAD_RATE, n_left_to_unload)
                cprint(
                    f'{env.now()}: {self} is unloading {n_to_unload_this_period} resources at {base}')
                base.resource.set_capacity(
                    base.resource.capacity() + n_to_unload_this_period)

                n_left_to_unload -= n_to_unload_this_period
            yield self.hold(1)

        # Leave supplier queue at base
        cprint(f'{self} leaving supplier queue at {self.config.get("base")}')
        self.leave(self.config.get('base').supplier_queue)
