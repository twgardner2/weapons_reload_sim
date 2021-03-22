import salabim as sim
from operator import itemgetter
import math
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
            'pct_res_onhand_dist': sim.Uniform(5, 50),
            'initial_delay_dist': CONSUMER_INITIAL_DELAY,
            'gen_dist': CONSUMER_GENERATION_DIST,
            'gen_time': CONSUMER_GENERATION_TIMES,
        }

        self.config = {**default_config, **config}


class ConsumerGenerator(sim.Component):
    def __init__(self, config={}):

        sim.Component.__init__(self)
        self.config = config
        self.generated_ship_is_inport = False

        # Destructure the config dict
        gen_dist, gen_time, base, env = itemgetter(
            'gen_dist', 'gen_time', 'base', 'env')(config)
        # Debug
        cprint(f'{env.now()}: Creating a ConsumerGenerator, config: {config}')

    def process(self):
        print(
            f'generator: {self}, ship is inport: {self.generated_ship_is_inport}')
        # Destructure the config dict
        initial_delay_dist, gen_dist, gen_time, base, env = itemgetter(
            'initial_delay_dist', 'gen_dist', 'gen_time', 'base', 'env')(self.config)

        # initial_delay = initial_delay_dist.sample()

        # Generate objects: If distribution is defined, overrides times
        # if not self.generated_ship_is_inport and env.now() >= initial_delay:
        if not self.generated_ship_is_inport:
            if gen_dist:        # Generate based on distribution
                while True:
                    yield self.hold(initial_delay_dist.sample())
                    cprint(
                        f'{round(env.now(), 2)}: Generating a Consumer based on distribution:\n {gen_dist.print_info(as_str=True)}')
                    if not self.generated_ship_is_inport:
                        print(env.now())
                        print(self.generated_ship_is_inport)
                        Consumer(self, self.config)
                        yield self.hold(gen_dist.sample())

            else:               # Generate at predefined times
                yield self.hold(gen_time.pop(0) - env.now())
                cprint(
                    f'{round(env.now(), 2)}: Generating a Consumer based on time')
                Consumer(self, self.config)
                while len(gen_time) > 0:
                    yield self.hold(gen_time.pop(0) - env.now())
                    cprint(
                        f'{round(env.now(), 2)}: Generating a Consumer based on time')
                    Consumer(self, self.config)


class Consumer(sim.Component):
    def __init__(self, generator, config={}):
        sim.Component.__init__(self)
        self.config = config
        self.generator = generator
        self.n_res_resupply = config['n_res_resupply']
        self.pct_res_onhand = config['pct_res_onhand_dist'].sample()
        self.n_res_onhand = round(
            self.pct_res_onhand * config['n_res_resupply'] / 100)
        cprint(f'Init Consumer:')
        cprint(self)
        cprint(f'n_res_required: {self.n_res_required()}')

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

        if OUTPUT:
            with open(OUTPUT_DIR + QUEUE_OUTPUT_FILE, 'a') as f:
                f.write(
                    f'{self.config["env"].now()},{self.config["base"].config["name"]},consumer_arrived,NA,{self.n_res_required()}\n')

        # Enter the queue for resources at the assigned base
        self.generator.generated_ship_is_inport = True
        print('consumer entering port')
        print(self.generator.generated_ship_is_inport)
        self.enter(base.queue)

        # Debugging
        # cprint(
        #     f'{env.now()}: Consumer arrived, requesting {n_consumed} resources, number in line: {len(base.queue)}')

        if base.ispassive():
            base.activate()

        yield self.passivate()

        while self.n_res_required() > 0:
            yield self.request((base.resource, self.n_issued))
            yield self.hold(1)

        # Finished with the consumer object, hold for remainder of simulation
        # so it doesn't release its resources
        self.generator.generated_ship_is_inport = False
        yield self.hold(float('inf'))
