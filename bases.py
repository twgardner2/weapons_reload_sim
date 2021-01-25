import salabim as sim
import resources as res
from operator import itemgetter
from globals import *

import crayons

verbose = VERBOSE_ALL or VERBOSE_BASE


class Base(sim.Component):
    # https://stackoverflow.com/questions/328851/printing-all-instances-of-a-class
    instances = []

    def __init__(self, config={}):
        sim.Component.__init__(self)
        self.__class__.instances.append(self)

        # Debug
        if verbose:
            print(f'creating a BASE, config: {config}')

        # Destructure config
        name, reload_team = itemgetter(
            'name', 'reload_team')(config)

        # Create queue and resource for consumers
        self.queue = sim.Queue(f'{name}_queue')
        self.resource = sim.Resource(f'{name}_resource', 0)

        # Consume the assigned reload_team resource
        if reload_team.available_quantity() > 0:
            self.request((reload_team, 1))
        else:
            raise Exception(
                f'not enough ERTs. {name} tried to request reload_team {reload_team} but there are none')

        # Attach config to self to pass to process
        self.config = config

    @classmethod
    def getInstances(cls):
        return(cls.instances)

    def process(self):
        # Destructure config
        name, reload_team = itemgetter(
            'name', 'reload_team')(self.config)

        # Run process
        while True:
            if verbose:
                print(
                    crayons.red(f'Available resources, {self.resource} at base {self}: {self.resource.available_quantity()}'))
            # While no ship in line, passivate
            while len(self.queue) == 0:
                yield self.passivate()
            print(crayons.blue(
                f'Number in line: {len(self.queue)}, front of line: {self.queue[0]}'))
            if self.resource.available_quantity() >= self.queue[0].config.get('n_consumed'):
                self.customer = self.queue.pop()
                print(crayons.yellow(
                    f'popped customer: {self.customer}, resources: {self.resource.available_quantity()}'))
                self.customer.hold(reload_team.reload_time)
                yield self.hold(reload_team.reload_time)
            else:
                yield self.passivate()


guam_config = {
    'name': 'Guam',
    'reload_team': res.fast_ERT,
    'num_piers': 2,
}
Guam = Base(guam_config)


dgar_config = {
    'name': 'Diego Garcia',
    'reload_team': res.fast_ERT
}
DGar = Base(dgar_config)

okinawa_config = {
    'name': 'Okinawa Tengan',
    'reload_team': res.fast_ERT
}
Okinawa = Base(okinawa_config)
