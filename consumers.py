import salabim as sim
from operator import itemgetter
from globals import *

import crayons as cr

# import time

# Verbose logging setup
verbose = VERBOSE_ALL or VERBOSE_CONSUMERS
cprint = MAKE_CPRINT(verbose, VERBOSE_CONSUMERS_COLOR)
cprint(f"consumers.py verbose output ON")


class ConsumerConfig():
    def __init__(self, consumer_type, config={}):
        if consumer_type is None:
            raise Exception('You must pass "consumer_type"')
        if 'base' not in config and 'env' not in config:
            raise Exception('You must pass "env" and "base"')
        if 'base' not in config:
            raise Exception('You must pass "base"')
        if 'env' not in config:
            raise Exception('You must pass "env"')

        n_res_resupply_dict = {
            'CG': CG_FULL_LOADOUT,
            'DDG': DDG_FULL_LOADOUT,
            'FFG': FFG_FULL_LOADOUT,
            'SAG': SAG_FULL_LOADOUT,
        }

        default_config = {
            'description': f'{consumer_type} resupplying at {config["base"]}',
            'n_res_resupply': n_res_resupply_dict[consumer_type],
            'n_res_onhand': 0,
            'gen_dist': CONSUMER_GENERATION_DIST,
            'gen_time': CONSUMER_GENERATION_TIMES,
        }
        self.config = {**default_config, **config}


class ConsumerGenerator(sim.Component):
    def __init__(self, config={}):
        sim.Component.__init__(self)
        self.config = config

        # Destructure the config dict
        gen_dist, gen_time, base, env = itemgetter(
            'gen_dist', 'gen_time', 'base', 'env')(config)
        # Debug
        cprint(f'{env.now()}: Creating a ConsumerGenerator, config: {config}')

    def process(self):
        # Destructure the config dict
        gen_dist, gen_time, base, env = itemgetter(
            'gen_dist', 'gen_time', 'base', 'env')(self.config)

        # Generate objects: If distribution is defined, overrides times

        if gen_dist:        # Generate based on distribution
            while True:
                cprint(
                    f'{round(env.now(), 2)}: Generating a Consumer based on distribution:\n {gen_dist.print_info(as_str=True)}')
                Consumer(self.config)
                yield self.hold(gen_dist.sample())

        else:               # Generate at predefined times
            yield self.hold(gen_time.pop(0) - env.now())
            cprint(f'{round(env.now(), 2)}: Generating a Consumer based on time')
            Consumer(self.config)
            while len(gen_time) > 0:
                yield self.hold(gen_time.pop(0) - env.now())
                cprint(
                    f'{round(env.now(), 2)}: Generating a Consumer based on time')
                Consumer(self.config)


class Consumer(sim.Component):
    def __init__(self, config={}):
        sim.Component.__init__(self)
        self.config = config
        self.n_res_resupply = config['n_res_resupply']
        self.n_res_onhand = config['n_res_onhand']
        cprint(f'Init Consumer:')
        cprint(self)
        cprint(f'n_res_required: {self.n_res_required()}')
        # n_consumed = config.get('n_consumed_dist').sample()
        # config['n_consumed'] = n_consumed

    def animation_objects(self, id):
        '''Defines representation of Consumers in a queue animation'''

        # Destructure config
        base = itemgetter('base')(self.config)

        size_x = 60
        size_y = 50
        b = 0.1 * size_x
        an0 = sim.AnimateImage(
            'img/warship2.png',
            width=50,
            text='Needs:\n' + str(round(self.n_res_required())),
            text_offsety=-25,
            textcolor='white' if base.queue.index(
                self) >= base.config.get('n_reload_team') else 'red'
        )
        return size_x, size_y, an0

    def n_res_required(self):
        '''Returns number of resources the Consumer requires'''
        return self.n_res_resupply - self.n_res_onhand

    def process(self):
        # Destructure the config dict
        base, env, n_res_resupply = itemgetter(
            'base', 'env', 'n_res_resupply')(self.config)

        # Enter the queue for resources at the assigned base
        self.enter(base.queue)

        # Debugging
        # cprint(
        #     f'{env.now()}: Consumer arrived, requesting {n_consumed} resources, number in line: {len(base.queue)}')

        if base.ispassive():
            base.activate()

        yield self.passivate()

        while self.n_res_required() > 0:
            # cprint(f'$$$$$ {self.n_issued}')
            yield self.request((base.resource, self.n_issued))
            yield self.hold(1)

        # Finished with the consumer object, hold for remainder of simulation
        # so it doesn't release its resources
        yield self.hold(float('inf'))
