import salabim as sim
import consumers as con
import suppliers as sup

dist = sim.Normal(10, 2)


# Setup environment
env = sim.Environment()
from resources import TLAMs, TLAMs1, TLAMs2, queue1, queue2, Base

ERT1 = sup.ERT(queue=queue1, reload_time=10)
queue1.reload_team = ERT1


con.ddgGenerator(queue=queue1, resource=TLAMs1)
# con.ddgGenerator(queue=queue2, mean_time=15)

sup.takeGenerator(resource=TLAMs1, n_supplied=1)

# Run simulation
env.run(till=5000)

base1_config = {
    "name": "base1",
    "queue": queue1,
    "resource": TLAMs1,
    "reload_team": ERT1
}
Base(base1_config)

# Simulation statistics
TLAMs.available_quantity.print_histogram()

# queue1.print_statistics()
# queue2.print_statistics()
