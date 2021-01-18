import salabim as sim
import resources as res
from operator import itemgetter
from globals import *


class Base(sim.Component):
    def __init__(self, config={}):
        sim.Component.__init__(self)

        # Debug
        if VERBOSE:
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
            while len(resource.requesters()) == 0:
                yield self.passivate()
            self.customer = resource.pop()
            # if resource.available_quantity() >= self.customer.config.get('n_consumed'):
            yield self.hold(reload_team.reload_time)
            self.customer.activate()


base1_config = {
    "name": "base1",
    "queue": res.queue1,
    "resource": res.TLAMs1,
    "reload_team": res.fast_ERT
}

base1 = Base(base1_config)

base2 = Base({
    "name": "base2",
    "queue": res.queue2,
    "resource": res.TLAMs2,
    "reload_team": res.fast_ERT
})
print(base1.config.get('reload_team'))
