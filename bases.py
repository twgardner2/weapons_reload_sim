import salabim as sim
import resources as res
from operator import itemgetter
from globals import *

import crayons

verbose = VERBOSE_ALL or VERBOSE_BASE


class Base(sim.Component):
    def __init__(self, config={}):
        sim.Component.__init__(self)

        # Debug
        if verbose:
            print(f'creating a BASE, config: {config}')

        # Destructure config
        name, resource, reload_team = itemgetter(
            'name', 'resource', 'reload_team')(config)

        # Create queue for consumers
        # config['queue'] = sim.Queue(name)
        self.queue = sim.Queue(name)

        # Consume the assigned reload_team resource
        if reload_team.available_quantity() > 1:
            self.request((reload_team, 1))
        else:
            raise Exception(
                f'not enough ERTs. {self} tried to request reload_team {reload_team} but there are none')

        # Attach config to self to pass to process
        self.config = config

    def process(self):
        # Destructure config
        name, resource, reload_team = itemgetter(
            'name', 'resource', 'reload_team')(self.config)

        # Run process
        while True:
            if verbose:
                print(
                    crayons.red(f'Available resources, {resource} at base {self}: {resource.available_quantity()}'))
            # While no ship in line, passivate
            while len(self.queue) == 0:
                yield self.passivate()
            print(crayons.blue(
                f'Number in line: {len(self.queue)}, front of line: {self.queue[0]}'))
            if resource.available_quantity() >= self.queue[0].config.get('n_consumed'):
                self.customer = self.queue.pop()
                print(crayons.yellow(
                    f'popped customer: {self.customer}, resources: {resource.available_quantity()}'))
                self.customer.hold(reload_team.reload_time)
                yield self.hold(reload_team.reload_time)
            else:
                yield self.passivate()


guam_config = {
    'name': 'Guam',
    'resource': res.TLAMs1,
    'reload_team': res.fast_ERT,
    'num_piers': 2,
}
Guam = Base(guam_config)


# dgar_config = {
#     'name': 'Diego Garcia',
#     'queue': res.queue2,
#     'resource': res.TLAMs2,
#     'reload_team': res.fast_ERT
# }
# DGAR = Base(dgar_config)
