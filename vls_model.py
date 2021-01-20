import salabim as sim
import consumers as con
import suppliers as sup
from globals import *


# Setup environment
env = sim.Environment(time_unit='hours', trace=True)
# env = sim.Environment(time_units='hours')


# Import resources
from resources import TLAMs, TLAMs1, TLAMs2, queue1, queue2, fast_ERT, slow_ERT
# Import bases
import bases

ddgGenerator1_config = {
    'gen_dist': DDG_ARRIVAL_DIST,
    'base': bases.base1,
    'n_consumed': DDG_N_CONSUMED,
}
# ddgGenerator2_config = {
#     'gen_dist': DDG_ARRIVAL_DIST,
#     'base': bases.base2,
#     'n_consumed': DDG_N_CONSUMED,
# }
con.ddgGenerator(ddgGenerator1_config)
# con.ddgGenerator(ddgGenerator2_config)

sup.takeGenerator({
    'arrival_dist': TAKE_ARRIVAL_DIST,
    'resource': TLAMs1,
    'n_supplied': TAKE_N_SUPPLIED,
})

sim.AnimateMonitor(queue1.length, x=10, y=450, width=1600,
                   height=300, horizontal_scale=0.2, vertical_scale=7.5)
qa0 = sim.AnimateQueue(
    queue1, x=100, y=50, title='queue, normal', direction='e', id='blue')
sim.AnimateRectangle(spec=lambda arg, t: (0, 10, arg.available_quantity(), 30),
                     text="", arg=TLAMs1)
# spec=(100, 10, 300, 30)
# Run simulation
env.animation_parameters(animate=True, speed=250)

env.background_color('20%gray')
env.run(till=3500)

# Simulation statistics
# TLAMs.available_quantity.print_histogram()
# fast_ERT.print_statistics()
# TLAMs1.print_info()
# TLAMs1.requesters().length.print_histogram()
# TLAMs1.requesters().length_of_stay.print_histogram()
# TLAMs1.claimers().length.print_histogram()
# bases.base1.config.get("resource").print_histograms()
# bases.base1.config.get("resource").print_statistics()
# bases.base1.config.get("resource").print_info()


# queue1.length_of_stay.print_histogram()
# TLAMs1.occupancy.print_histogram()
# queue1.print_info()


# queue2.length_of_stay.print_histogram()
# queue2.print_info()
