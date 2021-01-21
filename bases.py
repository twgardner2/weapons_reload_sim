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

        # Attach config to self to pass to process
        self.config = config

        # Destructure config
        name, queue, resource, reload_team = itemgetter(
            'name', 'queue', 'resource', 'reload_team')(config)

        # Consume the assigned reload_team resource
        if reload_team.available_quantity() > 1:
            self.request((reload_team, 1))
        else:
            raise Exception(
                f'not enough ERTs. {self} tried to request reload_team {reload_team} but there are none')

    def process(self):
        # Destructure config
        name, queue, resource, reload_team = itemgetter(
            'name', 'queue', 'resource', 'reload_team')(self.config)

        # Run process
        while True:
            if verbose:
                print(
                    crayons.red(f'Available resources, {resource} at base {self}: {resource.available_quantity()}'))
            # While no ship in line, passivate
            while len(queue) == 0:
                yield self.passivate()
            print(crayons.blue(
                f'Number in line: {len(queue)}, front of line: {queue[0]}'))
            if resource.available_quantity() >= queue[0].config.get('n_consumed'):
                self.customer = queue.pop()
                print(crayons.yellow(f'popped customer: {self.customer}'))
                self.customer.hold(reload_team.reload_time)
                yield self.hold(reload_team.reload_time)
            else:
                yield self.passivate()


base1_config = {
    "name": "base1",
    "queue": res.queue1,
    "resource": res.TLAMs1,
    "reload_team": res.fast_ERT
}


# base2_config = {
#     "name": "base2",
#     "queue": res.queue2,
#     "resource": res.TLAMs2,
#     "reload_team": res.fast_ERT
# }
base1 = Base(base1_config)
# base2 = Base(base2_config)
