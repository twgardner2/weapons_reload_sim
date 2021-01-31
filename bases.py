import salabim as sim
import resources as res
from operator import itemgetter
import crayons as cr
from globals import *

# Verbose logging setup
verbose = VERBOSE_ALL or VERBOSE_BASE

cprint = MAKE_CPRINT(verbose, VERBOSE_BASE_COLOR)

# def make_cprint(verbose):
#     if verbose:
#         def cprint(str):
#             print(cr.magenta(str, bold=True))
#     else:
#         def cprint(str):
#             pass
#     return cprint
#
#
# cprint = make_cprint(verbose)


cprint(f"bases.py verbose output ON")


class Base(sim.Component):
    # https://stackoverflow.com/questions/328851/printing-all-instances-of-a-class
    instances = []

    def __init__(self, config={}):
        sim.Component.__init__(self)
        self.__class__.instances.append(self)

        # Destructure config
        name, reload_team, env, n_reload_team = itemgetter(
            'name', 'reload_team', 'env', 'n_reload_team')(config)

        # Verbose logging
        # if verbose:
        #     print(cr.blue(f'{env.now()}: Creating a BASE, config: {config}'))
        cprint(f'{env.now()}: Creating a BASE, config: {config}')

        # Create queue and resources for consumers
        self.queue = sim.Queue(f'{name}_queue')
        self.resource = sim.Resource(f'{name}_resource', 0)
        self.reload_teams = sim.Resource(f'{name}_reload_teams', n_reload_team)
        self.reload_queue = [None] * n_reload_team

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
        name, reload_team, env, n_reload_team = itemgetter(
            'name', 'reload_team', 'env', 'n_reload_team')(self.config)

        # Run process
        while True:

            # Verbose logging
            cprint(
                f'{env.now()}: Available resources, {self.resource} at base {self}: {self.resource.available_quantity()}')
            cprint([customer for customer in self.queue])
            cprint([customer.n_res_required() for customer in self.queue])

            # While no consumers in line, passivate
            while len(self.queue) == 0:
                yield self.passivate()

            # When consumers are in line
            cprint(
                f'{env.now()}: Number in line: {len(self.queue)}, front of line: {self.queue[0]} needs: {self.queue[0].n_res_required()}')

            # Resources at base are > 0
            cprint(
                f'Resources available: {self.resource.available_quantity()}')

            # Resources available
            if self.resource.available_quantity() > 0:

                # Issue resources to as many Consumers as there are Reload Teams
                # starting from the first in line
                n = 0               # resources issued to one team
                n_all_teams = 0     # resources issued to all teams

                # Loop through reload teams
                for team in range(0, n_reload_team):

                    # Determine n resources to issue to consumer
                    n = min(self.resource.available_quantity() - n_all_teams,
                            self.queue[team].n_res_required(),
                            reload_team.reload_rate)

                    # Track number issued this time step
                    n_all_teams += n

                    # Issue resources to Consumer, have Consumer request the resource
                    cprint(f'issuing {n} to {self.queue[team]}')
                    cprint(
                        f"!@#$ - {self.queue[team]} n_res_onhand: {self.queue[team].n_res_onhand}, n_res_required: {self.queue[team].n_res_required()}")
                    cprint(self.queue[team].n_res_onhand)
                    cprint(
                        f"!@#$ - {self.queue[team]} n_res_onhand: {self.queue[team].n_res_onhand}, n_res_required: {self.queue[team].n_res_required()}")

                    self.queue[team].n_res_onhand += n
                    self.queue[team].n_issued = n
                    self.queue[team].activate()

                # Remove consumers who no longer need resources from queue
                for consumer in self.queue[0:n_reload_team]:
                    if consumer.n_res_required() <= 0:
                        self.queue.remove(consumer)

                # Hold  until next time step
                yield self.hold(1)

            # Resources not available
            else:
                yield self.hold(1)
