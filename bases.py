import os
import salabim as sim
# import resources as res
from operator import itemgetter
import crayons as cr
from globals import *

# Verbose logging setup
verbose = VERBOSE_ALL or VERBOSE_BASE
cprint = MAKE_CPRINT(verbose, VERBOSE_BASE_COLOR)
cprint(f"bases.py verbose output ON")

# Writing Output
out = OUTPUT

if out:
    try:
        os.remove(OUTPUT_DIR + QUEUE_OUTPUT_FILE)
    except OSError:
        pass


class BaseConfig():
    def __init__(self, config={}):
        if 'name' not in config and 'env' not in config:
            raise Exception('You must pass "env" and "name"')
        if 'name' not in config:
            raise Exception('You must pass "name"')
        if 'env' not in config:
            raise Exception('You must pass "env"')

        default_config = {
            'n_QRT': 1,
            'n_ERT': 1,
            'initial_resources': 100
        }
        self.config = {**default_config, **config}


class Base(sim.Component):
    # https://stackoverflow.com/questions/328851/printing-all-instances-of-a-class
    instances = []

    def __init__(self, config={}):
        sim.Component.__init__(self)
        self.__class__.instances.append(self)

        # Destructure config
        name, env, n_QRT, n_ERT = itemgetter(
            'name', 'env', 'n_QRT', 'n_ERT')(config)
        # name, reload_team, env, n_reload_team = itemgetter(
        # 'name', 'reload_team', 'env', 'n_reload_team')(config)

        # Verbose logging
        cprint(f'{env.now()}: Creating a BASE, config: {config}')

        # Create queue and resources for consumers
        self.queue = sim.Queue(f'{name}_queue')
        self.supplier_queue = sim.Queue(f'{name}_supplier_queue')
        self.resource = sim.Resource(
            f'{name}_resource', config['initial_resources'])
        self.reload_teams = n_QRT * ['QRT'] + n_ERT * ['ERT']
        self.n_reload_team = len(self.reload_teams)

        # Attach config to self to pass to process
        self.config = config

    @classmethod
    def getInstances(cls):
        '''Returns all instantiated objects of this class'''
        return(cls.instances)

    def process(self):
        # Destructure config
        # name, reload_team, env, n_reload_team = itemgetter(
        #     'name', 'reload_team', 'env', 'n_reload_team')(self.config)
        name, env = itemgetter('name', 'env')(self.config)
        # Run process
        while True:

            if OUTPUT:
                with open(OUTPUT_DIR + QUEUE_OUTPUT_FILE, 'a') as f:
                    f.write(
                        f'{env.now()},{name},queue_length,{self.queue.length()},NA\n')
                    f.write(
                        f'{env.now()},{name},resources_available,{self.resource.available_quantity()},NA\n')

            # Verbose logging
            cprint(
                f'{env.now()}: Available resources, {self.resource} at base {self}: {self.resource.available_quantity()}')

            # While no consumers in line, passivate
            while len(self.queue) == 0:
                yield self.passivate()

            # When consumers are in line
            cprint(
                f'{env.now()}: Number in line: {len(self.queue)}, front of line: {self.queue[0]} needs: {self.queue[0].n_res_required()}')

            # Resources at base are > 0
            cprint(
                f'Resources available: {self.resource.available_quantity()}')

            # During daytime and resources available
            if is_daytime(env.now()) and self.resource.available_quantity() > 0:

                # Issue resources to as many Consumers as there are Reload Teams
                # starting from the first in line

                # Available at base this time step
                avail = self.resource.available_quantity()
                # Required by each consumer
                n_req = [x.n_res_required()
                         for x in self.queue[:self.n_reload_team]]
                # Required by all consumers ahead of a particular consumer
                n_req_cum = [sum(n_req[:x]) for x in range(0, len(n_req))]
                n = 0               # resources issued to one team
                n_all_teams = 0     # resources issued to all teams

                # Reload rates for each reload team
                reload_rates = [RELOAD_TEAM_RATES[team]
                                for team in self.reload_teams]
                cprint(reload_rates)

                # Loop through reload teams
                for team in range(self.n_reload_team):
                    # If no consumer in line for this reload team, break
                    if self.queue[team] is None:
                        break
                    # Determine n resources to issue to consumer
                    n = min(avail - n_all_teams,
                            n_req[team],
                            reload_rates[team],
                            avail - n_req_cum[team] if avail >= n_req_cum[team] else 0)

                    # Track number issued this time step
                    n_all_teams += n

                    # Issue resources to Consumer, have Consumer request the resource
                    cprint(f'issuing {n} to {self.queue[team]}')

                    self.queue[team].n_res_onhand += n
                    self.queue[team].n_issued = n
                    self.queue[team].activate()

                # Remove consumers who no longer need resources from queue
                for consumer in self.queue[0:self.n_reload_team]:
                    if consumer.n_res_required() <= 0:
                        self.queue.remove(consumer)

                # Hold  until next time step
                yield self.hold(1)

            # Resources not available
            else:
                yield self.hold(1)
