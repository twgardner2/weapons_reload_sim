import salabim as sim
import consumers as con
import suppliers as sup
import animation as ani
from globals import *


# Verbose logging setup
verbose = VERBOSE_ALL or VERBOSE_MAIN
cprint = MAKE_CPRINT(verbose, VERBOSE_MAIN_COLOR)
cprint(f"vls_model.py verbose output ON")

# Setup environment then import bases.py, which requires the env object
env = sim.Environment(time_unit='hours', trace=TRACE)
# env.animate_debug(False)
# env = sim.Environment(time_units='hours')
import bases


print(sup.TAKE_Config({'env': env}).config)
print(sup.TAKE_Config({'env': env, 'n_supplied': 9}).config)

print(sup.C5_Config({'env': env}).config)
print(sup.C5_Config({'env': env, 'n_supplied': 9}).config)

print(sup.C17_Config({'env': env}).config)
print(sup.C17_Config({'env': env, 'n_supplied': 9}).config)

print(sup.C130_Config({'env': env}).config)
print(sup.C130_Config({'env': env, 'n_supplied': 9}).config)
# region: ((((((((((((((((((((((((((((((Resources))))))))))))))))))))))))))))))
from resources import *
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((Port of Alma)))))))))))))))))))))))))))))
# Base
PortOfAlma = bases.Base({
    'name': 'Port of Alma',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# Consumers
PortAlma_CRUDES_CustGen = con.ConsumerGenerator({
    'description': 'Cruisers and Destroyers arriving at Diego Garcia for resupply',
    'env': env,
    'gen_dist': CONSUMER_GENERATION_DIST,
    'gen_time': CONSUMER_GENERATION_TIMES,
    'base': PortOfAlma,
    'n_res_resupply': 40,
    'n_res_onhand': 1,
    'n_consumed_dist': CONSUMER_N_CONSUMED_DIST,
})

# Suppliers
PortOfAlma_TAKE_Generator = sup.SupplierGenerator(
    sup.TAKE_Config({
        'env': env,
        'base': PortOfAlma,
    }).config)

PortOfAlma_C17_Generator = sup.SupplierGenerator(
    sup.C17_Config({
        'env': env,
        'base': PortOfAlma,
    }).config)

PortOfAlma_C130_Generator = sup.SupplierGenerator(
    sup.C130_Config({
        'env': env,
        'base': PortOfAlma,
    }).config)
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((Diego Garcia)))))))))))))))))))))))))))))
DGar = bases.Base({
    'name': 'Diego Garcia',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

DGar_CRUDES_CustGen = con.ConsumerGenerator({
    'description': 'Cruisers and Destroyers arriving at Diego Garcia for resupply',
    'env': env,
    'gen_dist': CONSUMER_GENERATION_DIST,
    'gen_time': CONSUMER_GENERATION_TIMES,
    'base': DGar,
    'n_res_resupply': 40,
    'n_res_onhand': 1,
    'n_consumed_dist': CONSUMER_N_CONSUMED_DIST,
})

DGar_TAKE_Generator = sup.SupplierGenerator({
    'env': env,
    'base': DGar,
    # 'gen_dist': SUPPLIER_GENERATION_DIST,
    'gen_dist': None,
    # 'gen_time': None,
    'gen_time': [10, 300, 400],
    'n_supplied': TAKE_N_SUPPLIED,
})
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((Guam)))))))))))))))))))))))))))))))))
Guam = bases.Base({
    'name': 'Guam',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# CRUDESs arriving at Guam
GU_CRUDES_CustGen = con.ConsumerGenerator({
    'description': 'Cruisers and Destroyers arriving at Guam for resupply',
    'env': env,
    'gen_dist': sim.IntUniform(30, 60),
    # 'gen_dist': None,
    # 'gen_time': list(range(10, 15, 5)),
    'gen_time': [15, 25, 35],
    'base': Guam,
    'n_res_resupply': 40,
    'n_res_onhand': 1,
    'n_consumed_dist': CONSUMER_N_CONSUMED_DIST,
})

GU_TAKE_Generator = sup.SupplierGenerator({
    'env': env,
    'base': Guam,
    'gen_dist': sim.Normal(300, 40),
    # 'gen_dist': None,
    'gen_time': [55, 56, 57],
    # 'gen_time': list(range(100, 1000, 100)),
    'n_supplied': TAKE_N_SUPPLIED,
})
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((Saipan)))))))))))))))))))))))))))))))))
Saipan = bases.Base({
    'name': 'Saipan',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

Saipan_CRUDES_CustGen = con.ConsumerGenerator({
    'description': 'Cruisers and Destroyers arriving at Diego Garcia for resupply',
    'env': env,
    'gen_dist': CONSUMER_GENERATION_DIST,
    'gen_time': CONSUMER_GENERATION_TIMES,
    'base': Saipan,
    'n_res_resupply': 40,
    'n_res_onhand': 1,
    'n_consumed_dist': CONSUMER_N_CONSUMED_DIST,
})

Saipan_TAKE_Generator = sup.SupplierGenerator({
    'env': env,
    'base': Saipan,
    # 'gen_dist': SUPPLIER_GENERATION_DIST,
    'gen_dist': None,
    # 'gen_time': None,
    'gen_time': [10, 300, 400],
    'n_supplied': TAKE_N_SUPPLIED,
})
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((Port of Brisbane)))))))))))))))))))))))))))))))))

PortOfBrisbane = bases.Base({
    'name': 'Port of Brisbane',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

PortOfBrisbane_CRUDES_CustGen = con.ConsumerGenerator({
    'description': 'Cruisers and Destroyers arriving at Diego Garcia for resupply',
    'env': env,
    'gen_dist': CONSUMER_GENERATION_DIST,
    'gen_time': CONSUMER_GENERATION_TIMES,
    'base': PortOfBrisbane,
    'n_res_resupply': 40,
    'n_res_onhand': 1,
    'n_consumed_dist': CONSUMER_N_CONSUMED_DIST,
})

PortOfBrisbane_TAKE_Generator = sup.SupplierGenerator({
    'env': env,
    'base': PortOfBrisbane,
    # 'gen_dist': SUPPLIER_GENERATION_DIST,
    'gen_dist': None,
    # 'gen_time': None,
    'gen_time': [10, 300, 400],
    'n_supplied': TAKE_N_SUPPLIED,
})


# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((Darwin Anchorage)))))))))))))))))))))))))))))))))
DarwinAnchorage = bases.Base({
    'name': 'Darwin Anchorage',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})


DarwinAnchorage_CRUDES_CustGen = con.ConsumerGenerator({
    'description': 'Cruisers and Destroyers arriving at Diego Garcia for resupply',
    'env': env,
    'gen_dist': CONSUMER_GENERATION_DIST,
    'gen_time': CONSUMER_GENERATION_TIMES,
    'base': DarwinAnchorage,
    'n_res_resupply': 40,
    'n_res_onhand': 1,
    'n_consumed_dist': CONSUMER_N_CONSUMED_DIST,
})

DarwinAnchorage_TAKE_Generator = sup.SupplierGenerator({
    'env': env,
    'base': DarwinAnchorage,
    # 'gen_dist': SUPPLIER_GENERATION_DIST,
    'gen_dist': None,
    # 'gen_time': None,
    'gen_time': [10, 300, 400],
    'n_supplied': TAKE_N_SUPPLIED,
})

# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((Point Wilson)))))))))))))))))))))))))))))))))
PointWilson = bases.Base({
    'name': 'Point Wilson',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})


PointWilson_CRUDES_CustGen = con.ConsumerGenerator({
    'description': 'Cruisers and Destroyers arriving at Diego Garcia for resupply',
    'env': env,
    'gen_dist': CONSUMER_GENERATION_DIST,
    'gen_time': CONSUMER_GENERATION_TIMES,
    'base': PointWilson,
    'n_res_resupply': 40,
    'n_res_onhand': 1,
    'n_consumed_dist': CONSUMER_N_CONSUMED_DIST,
})

PointWilson_TAKE_Generator = sup.SupplierGenerator({
    'env': env,
    'base': PointWilson,
    # 'gen_dist': SUPPLIER_GENERATION_DIST,
    'gen_dist': None,
    # 'gen_time': None,
    'gen_time': [10, 300, 400],
    'n_supplied': TAKE_N_SUPPLIED,
})
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((Banyuwangi)))))))))))))))))))))))))))))))))

# Base
Banyuwangi = bases.Base({
    'name': 'Banyuwangi',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# Consumers
Banyuwangi_CRUDES_CustGen = con.ConsumerGenerator({
    'description': 'Cruisers and Destroyers arriving at Diego Garcia for resupply',
    'env': env,
    'gen_dist': CONSUMER_GENERATION_DIST,
    'gen_time': CONSUMER_GENERATION_TIMES,
    'base': Banyuwangi,
    'n_res_resupply': 40,
    'n_res_onhand': 1,
    'n_consumed_dist': CONSUMER_N_CONSUMED_DIST,
})

# Suppliers
Banyuwangi_TAKE_Generator = sup.SupplierGenerator({
    'env': env,
    'base': Banyuwangi,
    # 'gen_dist': SUPPLIER_GENERATION_DIST,
    'gen_dist': None,
    # 'gen_time': None,
    'gen_time': [10, 300, 400],
    'n_supplied': TAKE_N_SUPPLIED,
})

Banyuwangi_C17_Generator = sup.SupplierGenerator({
    'env': env,
    'base': Banyuwangi,
    'gen_dist': SUPPLIER_GENERATION_DIST,
    'gen_time': SUPPLIER_GENERATION_TIMES,
    'n_supplied': SUPPLIER_N_SUPPLIED,
})

Banyuwangi_C130_Generator = sup.SupplierGenerator({
    'env': env,
    'base': Banyuwangi,
    'gen_dist': SUPPLIER_GENERATION_DIST,
    'gen_time': SUPPLIER_GENERATION_TIMES,
    'n_supplied': SUPPLIER_N_SUPPLIED,
})
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((Semarang)))))))))))))))))))))))))))))))))
Semarang = bases.Base({
    'name': 'Semarang',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((Male)))))))))))))))))))))))))))))))))
Male = bases.Base({
    'name': 'Male',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((Kauri Point)))))))))))))))))))))))))))))))))
KauriPoint = bases.Base({
    'name': 'Kauri Point',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((Tauranga)))))))))))))))))))))))))))))))))
Tauranga = bases.Base({
    'name': 'Tauranga',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((Pearl Harbor)))))))))))))))))))))))))))))))))

PearlHarbor = bases.Base({
    'name': 'Pearl Harbor',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})
# endregion ====================================================================


# region: ((((((((((((((((((((((((((((((Animation))))))))))))))))))))))))))))))
# # > Queue length line plot
# sim.AnimateMonitor(monitor=Guam.queue.length,
#                    x=ani.q_lineplot_x_left,
#                    y=ani.q_lineplot_y_bottom,
#                    width=ani.q_lineplot_width,
#                    height=ani.q_lineplot_height,
#                    horizontal_scale=0.15,
#                    vertical_scale=7.5)
# # > Queue length of stay histogram
# sim.AnimateText(text=lambda: Guam.queue.length_of_stay.print_histogram(as_str=True),
#                 x=ani.q_LOS_hist_x_left,
#                 y=ani.q_LOS_hist_y_top,
#                 text_anchor='nw',
#                 font='narrow',
#                 fontsize=10)

# # Guam Animation
# qa0 = sim.AnimateQueue(
#     queue=Guam.queue,
#     x=ani.queue_x_left + 50,
#     y=ani.queue_y_bottom,
#     title='Queue of Ships Waiting for Reload at Guam',
#     direction='e',
#     id='blue',
# )
# # sim.AnimateRectangle(spec=ani.resource_bar_spec,
# #                      arg=Guam.resource)
# sim.AnimateRectangle(spec=ani.resource_label_spec,
#                      text=ani.resource_label_text,
#                      arg=Guam.resource)

# Base rectangle
for i, base in enumerate(bases.Base.getInstances()):
    sim.AnimateRectangle(spec=(ani.base_rectangle_x_left,
                               ani.base_queues_y_bottom + ani.base_queues_vertical_spacing * i,
                               ani.base_rectangle_x_left + ani.base_rectangle_width,
                               ani.base_queues_y_bottom + ani.base_queues_vertical_spacing * i + 50),
                         text=ani.base_rectangle_text,
                         arg=base,
                         offsety=-25)

# Consumers Queue
for i, base in enumerate(bases.Base.getInstances()):
    cprint(f'{i}: {base}')
    sim.AnimateQueue(
        queue=base.queue,
        # x=ani.queue_x_left + 50,
        x=ani.base_rectangle_x_left + \
        ani.base_rectangle_width + ani.margins['general'],
        y=ani.base_queues_y_bottom + ani.base_queues_vertical_spacing * i,
        # title=f'Queue of Ships Waiting for Reload at {base.config["name"]}',
        title=f'Consumers',
        direction='e',
        id='blue',
    )

# Suppliers Queue
for i, base in enumerate(bases.Base.getInstances()):
    cprint(f'{i}: {base}')
    sim.AnimateQueue(
        queue=base.supplier_queue,
        # x=ani.queue_x_left + 50,
        x=ani.base_rectangle_x_left - ani.margins['general'],
        y=ani.base_queues_y_bottom + ani.base_queues_vertical_spacing * i,
        # title=f'Queue of Suppliers Unloading at {base.config["name"]}',
        title=f'Suppliers',
        direction='w',
        id='blue',
    )
# endregion ====================================================================


# region: ((((((((((((((((((((((((((((((Monitors))))))))))))))))))))))))))))))
# all_queues_length = Guam.queue.length.merge(DGar.queue.length)
# all_queues_length = Guam.queue.length + DGar.queue.length

# Run simulation
env.animation_parameters(animate=ANIMATE, speed=SIM_SPEED)  # , width=1500

env.background_color('20%gray')
env.run(till=SIM_LENGTH)

# Simulation statistics
# bases.base1.config.get('resource').print_histograms()
# bases.base1.config.get('resource').print_statistics()
# bases.base1.config.get('resource').print_info()


# Guam.length_of_stay.print_histogram()
# TLAMs1.occupancy.print_histogram()
# Guam.print_info()


# queue2.length_of_stay.print_histogram()
# queue2.print_info()

# Guam.queue.length.print_histogram()
# DGar.queue.length.print_histogram()
# print(all_queues_length)
# all_queues_length.print_histogram()
# Guam.queue.length.merge(
#     DGar.queue.length, name='combined queues').print_histogram()
# all_queues_length.print_histogram()

# print(bases.Base.getInstances())

# print([base.queue.length() for base in bases.Base.getInstances()])

# sum(base.queue.length for base in bases.Base.getInstances()
#     ).print_histogram()

# endregion ====================================================================
