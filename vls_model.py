import salabim as sim
import consumers as con
import suppliers as sup
from globals import *
import animation as ani


# Setup environment
env = sim.Environment(time_unit='hours', trace=TRACE)
env.animate_debug(True)
# env = sim.Environment(time_units='hours')


### Resources ##################################################################
from resources import *

### Bases ######################################################################
import bases

### Consumers ##################################################################
# CRUDESs arriving at Guam
GU_CRUDES_CustGen_config = {
    'description': 'Cruisers and Destroyers arriving at Guam for resupply',
    'env': env,
    'gen_dist': CONSUMER_GENERATION_DIST,
    'gen_time': CONSUMER_GENERATION_TIMES,
    'base': bases.Guam,
    'n_consumed_dist': CONSUMER_N_CONSUMED_DIST,
}
GU_CRUDES_CustGen = con.ConsumerGenerator(
    GU_CRUDES_CustGen_config)

### Suppliers ##################################################################

sup.SupplierGenerator({
    'env': env,
    'base': bases.Guam,
    'gen_dist': SUPPLIER_GENERATION_DIST,
    'gen_time': SUPPLIER_GENERATION_TIMES,
    # 'resource': TLAMs1,
    'n_supplied': SUPPLIER_N_SUPPLIED,
})


# Animation
# > Queue length line plot
sim.AnimateMonitor(monitor=bases.Guam.queue.length,
                   x=ani.q_lineplot_x_left,
                   y=ani.q_lineplot_y_bottom,
                   width=ani.q_lineplot_width,
                   height=ani.q_lineplot_height,
                   horizontal_scale=0.1,
                   vertical_scale=7.5)
# > Queue length of stay histogram
sim.AnimateText(text=lambda: bases.Guam.queue.length_of_stay.print_histogram(as_str=True),
                x=ani.q_LOS_hist_x_left,
                y=ani.q_LOS_hist_y_top,
                text_anchor='nw',
                font='narrow',
                fontsize=10)

# Guam Animation
qa0 = sim.AnimateQueue(
    queue=bases.Guam.queue,
    x=ani.queue_x_left + 50,
    y=ani.queue_y_bottom,
    title='Queue of Ships Waiting for Reload at Base 1',
    direction='e',
    id='blue',
)
sim.AnimateRectangle(spec=ani.resource_bar_spec,
                     arg=bases.Guam.resource)
sim.AnimateRectangle(spec=ani.resource_label_spec,
                     text=ani.resource_label_text,
                     arg=bases.Guam.resource)


# Run simulation
env.animation_parameters(animate=ANIMATE, speed=SIM_SPEED)  # , width=1500

env.background_color('20%gray')
env.run(till=SIM_LENGTH)

# Simulation statistics
# TLAMs.available_quantity.print_histogram()
# fast_ERT.print_statistics()
# TLAMs1.print_info()
# TLAMs1.requesters().length.print_histogram()
# TLAMs1.requesters().length_of_stay.print_histogram()
# TLAMs1.claimers().length.print_histogram()
# bases.base1.config.get('resource').print_histograms()
# bases.base1.config.get('resource').print_statistics()
# bases.base1.config.get('resource').print_info()


# Guam.length_of_stay.print_histogram()
# TLAMs1.occupancy.print_histogram()
# Guam.print_info()


# queue2.length_of_stay.print_histogram()
# queue2.print_info()
