import salabim as sim
from operator import itemgetter
from globals import *

import crayons

verbose = VERBOSE_ALL or VERBOSE_CONSUMERS


class ddgGenerator(sim.Component):
    def __init__(self, config={}):
        sim.Component.__init__(self)
        self.config = config

        # Debug
        if verbose:
            print(f'creating a ddgGenerator, config: {config}')

    def process(self):
        # Destructure the config dict
        gen_dist, gen_time, base, env = itemgetter(
            'gen_dist', 'gen_time', 'base', 'env')(self.config)

        # Generate objects: If distribution is defined, overrides times

        if gen_dist:        # Generate based on distribution
            while True:
                if verbose:
                    print(crayons.green(
                        f'{round(env.now(), 2)}: Generating a DDG based on distribution:\n {gen_dist.print_info(as_str=True)}', bold=True))
                DDG(self.config)
                yield self.hold(gen_dist.sample())

        else:               # Generate at predefined times
            yield self.hold(gen_time.pop(0) - env.now())
            if verbose:
                print(crayons.green(
                    f'{round(env.now(), 2)}: Generating a DDG based on time', bold=True))
            DDG(self.config)
            while len(gen_time) > 0:
                yield self.hold(gen_time.pop(0) - env.now())
                if verbose:
                    print(crayons.green(
                        f'{round(env.now(), 2)}: Generating a DDG based on time', bold=True))
                DDG(self.config)


class DDG(sim.Component):
    def __init__(self, config={}):
        sim.Component.__init__(self)
        n_consumed = config.get('n_consumed_dist').sample()
        config['n_consumed'] = n_consumed
        self.config = config
        # self.config.get('base').config.get('resource').print_info()

    def animation_objects(self, id):
        size_x = 60
        size_y = 50
        b = 0.1 * size_x
        # Instances of Animate class:
        # an0 = sim.AnimateRectangle(
        #     # spec=(b, 2, xvisitor_dim - b, yvisitor_dim - b),
        #     spec=(0, 0, 20, 20),
        #     linewidth=0,
        #     # fillcolor=direction_color(self.direction),
        #     text='Needs: ' + str(round(self.config.get('n_consumed'))),
        #     # fontsize=xvisitor_dim * 0.7,
        #     textcolor="black"
        # )
        an0 = sim.AnimateImage(
            'img/warship2.png',
            width=50,
            text='Needs:\n' + str(round(self.config.get('n_consumed'))),
            text_offsety=-25,
            textcolor="white"
        )
        return size_x, size_y, an0

    def process(self):
        # Destructure the config dict
        base, n_consumed = itemgetter(
            'base', 'n_consumed')(self.config)

        # Enter the queue for resources at the assigned base
        self.enter(base.config.get('queue'))

        # Debugging
        if verbose:
            print(
                crayons.blue(f'DDG arrived, requesting {n_consumed} resources, number in line: {len(base.config.get("queue"))}'))

        if base.ispassive():
            base.activate()

        yield self.passivate()
        # yield self.hold(base.config.get('reload_team').reload_time)
        yield self.request((base.config.get('resource'), n_consumed))
        yield self.hold(float('inf'))
