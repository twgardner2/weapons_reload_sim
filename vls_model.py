import salabim as sim
import consumers as con
import suppliers as sup
from globals import *

dist = sim.Normal(10, 2)


# Setup environment
env = sim.Environment()
from resources import TLAMs, TLAMs1, TLAMs2, queue1, queue2, fast_ERT, slow_ERT

# ERT1 = sup.ERT(queue=queue1, reload_time=10)
# queue1.reload_team = ERT1

import bases

ddgGenerator1_config = {
    'gen_dist': DDG_ARRIVAL_DIST,
    'base': bases.base1,
    'n_consumed': DDG_N_CONSUMED,

}
con.ddgGenerator(ddgGenerator1_config)
# con.ddgGenerator(queue=queue2, mean_time=15)

sup.takeGenerator({
    'arrival_dist': TAKE_ARRIVAL_DIST,
    'resource': TLAMs1,
    'n_supplied': TAKE_N_SUPPLIED,
})


# Run simulation
env.run(till=5000)

for claimer in fast_ERT.claimers():
    print(claimer)


# Simulation statistics
# TLAMs.available_quantity.print_histogram()
# fast_ERT.print_statistics()
# queue1.print_statistics()
# queue2.print_statistics()


# bases.base1.config.get("queue").print_histograms()
# bases.base1.config.get("resource").print_info()
