import salabim as sim
import resources as res
from operator import itemgetter
from globals import *

import crayons as cr

verbose = VERBOSE_ALL or VERBOSE_BASE


class Base(sim.Component):
    # https://stackoverflow.com/questions/328851/printing-all-instances-of-a-class
    instances = []

    def __init__(self, config={}):
        sim.Component.__init__(self)
        self.__class__.instances.append(self)

        # Destructure config
        name, reload_team, env = itemgetter(
            'name', 'reload_team', 'env')(config)

        # Debug
        if verbose:
            print(cr.blue(f'{env.now()}: Creating a BASE, config: {config}'))

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
        '''Returns all instantiated objects of this class'''
        return(cls.instances)

    def process(self):
        # Destructure config
        name, reload_team, env = itemgetter(
            'name', 'reload_team', 'env')(self.config)

        # Run process
        while True:
            if verbose:
                print(
                    cr.red(f'{env.now()}: Available resources, {self.resource} at base {self}: {self.resource.available_quantity()}'))
            # While no consumers in line, passivate
            while len(self.queue) == 0:
                yield self.passivate()

            # When consumers are in line
            print(cr.blue(
                f'{env.now()}: Number in line: {len(self.queue)}, front of line: {self.queue[0]}'))
            if self.resource.available_quantity() >= self.queue[0].config.get('n_consumed'):
                reload_time = self.queue[0].config.get(
                    'n_consumed') / reload_team.reload_rate
                print(cr.cyan(
                    f'{env.now()}: Going to reoload customer: {self.queue[0]}, resources: {self.resource.available_quantity()}'))
                yield self.hold(reload_time)
                self.queue.pop()
            else:
                # yield self.passivate()
                yield self.hold(1)
