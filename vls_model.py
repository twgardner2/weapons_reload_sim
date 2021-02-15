import salabim as sim
import consumers as con
import suppliers as sup
import animation as ani
import os
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


# region: ((((((((((((((((((((((((((((((Resources))))))))))))))))))))))))))))))
from resources import *
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((Port of Alma)))))))))))))))))))))))))))))

# ---------- Base ----------
PortOfAlma = bases.Base({
    'name': 'Port of Alma',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# ---------- Consumers ----------
PortOfAlma_CG_CustGen = con.ConsumerGenerator(
    con.ConsumerConfig(
        consumer_type='CG',
        config={
            'env': env,
            'base': PortOfAlma,
            'gen_dist': sim.IntUniform(40, 80),
        }).config)

PortOfAlma_DDG_CustGen = con.ConsumerGenerator(
    con.ConsumerConfig(
        consumer_type='DDG',
        config={
            'env': env,
            'base': PortOfAlma,
            'gen_dist': sim.IntUniform(40, 80),
        }).config)

# ---------- Suppliers ----------
PortOfAlma_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': PortOfAlma,
                            'gen_dist': sim.IntUniform(100, 200)
                        }).config)

PortOfAlma_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': PortOfAlma,
                        }).config)

PortOfAlma_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': PortOfAlma,
                        }).config)
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((Diego Garcia)))))))))))))))))))))))))))))
# ---------- Base ----------
DGar = bases.Base({
    'name': 'Diego Garcia',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# ---------- Consumers ----------
DGar_CG_CustGen = con.ConsumerGenerator(
    con.ConsumerConfig(
        consumer_type='CG',
        config={
            'env': env,
            'base': DGar,
            'gen_dist': sim.IntUniform(40, 80),
        }).config)

DGar_DDG_CustGen = con.ConsumerGenerator(
    con.ConsumerConfig(
        consumer_type='DDG',
        config={
            'env': env,
            'base': DGar,
            'gen_dist': sim.IntUniform(40, 80),
        }).config)

# ---------- Suppliers ----------
DGar_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': DGar,
                        }).config)

DGar_C5_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C5',
                        config={
                            'env': env,
                            'base': DGar,
                        }).config)

DGar_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': DGar,
                        }).config)

DGar_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': DGar,
                        }).config)
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((Guam)))))))))))))))))))))))))))))))))
# ---------- Base ----------
Guam = bases.Base({
    'name': 'Guam',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# CRUDESs arriving at Guam
Guam_CRUDES_CustGen = con.ConsumerGenerator(
    con.ConsumerConfig(
        consumer_type='SAG',
        config={
            'env': env,
            'base': Guam,
            'gen_dist': sim.IntUniform(40, 80),
        }).config)

# ---------- Suppliers ----------
Guam_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Guam,
                        }).config)

Guam_C5_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C5',
                        config={
                            'env': env,
                            'base': Guam,
                        }).config)

Guam_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Guam,
                        }).config)

Guam_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Guam,
                        }).config)
# endregion ====================================================================


# region: ((((((((((((((((((((((((((((((((Saipan))))))))))))))))))))))))))))))))
# ---------- Base ----------
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

# ---------- Suppliers ----------
Saipan_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Saipan,
                        }).config)

Saipan_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Saipan,
                        }).config)

Saipan_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Saipan,
                        }).config)
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((Brisbane)))))))))))))))))))))))))))))))

# ---------- Base ----------
Brisbane = bases.Base({
    'name': 'Port of Brisbane',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

Brisbane_CRUDES_CustGen = con.ConsumerGenerator({
    'description': 'Cruisers and Destroyers arriving at Diego Garcia for resupply',
    'env': env,
    'gen_dist': CONSUMER_GENERATION_DIST,
    'gen_time': CONSUMER_GENERATION_TIMES,
    'base': Brisbane,
    'n_res_resupply': 40,
    'n_res_onhand': 1,
    'n_consumed_dist': CONSUMER_N_CONSUMED_DIST,
})

# ---------- Suppliers ----------
Brisbane_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Brisbane,
                        }).config)

Brisbane_C5_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C5',
                        config={
                            'env': env,
                            'base': Brisbane,
                        }).config)

Brisbane_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Brisbane,
                        }).config)

Brisbane_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Brisbane,
                        }).config)
# endregion ====================================================================


# region: ((((((((((((((((((((((((((((((((Darwin))))))))))))))))))))))))))))))))
# ---------- Base ----------
Darwin = bases.Base({
    'name': 'Darwin',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})


Darwin_CRUDES_CustGen = con.ConsumerGenerator({
    'description': 'Cruisers and Destroyers arriving at Diego Garcia for resupply',
    'env': env,
    'gen_dist': CONSUMER_GENERATION_DIST,
    'gen_time': CONSUMER_GENERATION_TIMES,
    'base': Darwin,
    'n_res_resupply': 40,
    'n_res_onhand': 1,
    'n_consumed_dist': CONSUMER_N_CONSUMED_DIST,
})

# ---------- Suppliers ----------
Darwin_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Darwin,
                        }).config)

Darwin_C5_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C5',
                        config={
                            'env': env,
                            'base': Darwin,
                        }).config)

Darwin_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Darwin,
                        }).config)

Darwin_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Darwin,
                        }).config)

# endregion ====================================================================


# region: (((((((((((((((((((((((((((((Point Wilson)))))))))))))))))))))))))))))
# ---------- Base ----------
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

# ---------- Suppliers ----------
PointWilson_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': PointWilson,
                        }).config)

PointWilson_C5_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C5',
                        config={
                            'env': env,
                            'base': PointWilson,
                        }).config)

PointWilson_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': PointWilson,
                        }).config)

PointWilson_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': PointWilson,
                        }).config)

# endregion ====================================================================


# region: ((((((((((((((((((((((((((((((Banyuwangi))))))))))))))))))))))))))))))

# ---------- Base ----------
Banyuwangi = bases.Base({
    'name': 'Banyuwangi',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# ---------- Consumers ----------
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

# ---------- Suppliers ----------
Banyuwangi_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Banyuwangi,
                        }).config)

Banyuwangi_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Banyuwangi,
                        }).config)

Banyuwangi_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Banyuwangi,
                        }).config)
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((Semarang)))))))))))))))))))))))))))))))

# ---------- Base ----------
Semarang = bases.Base({
    'name': 'Semarang',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# ---------- Suppliers ----------
Semarang_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Semarang,
                        }).config)

Semarang_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Semarang,
                        }).config)

Semarang_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Semarang,
                        }).config)
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((Male)))))))))))))))))))))))))))))))))

# ---------- Base ----------
Male = bases.Base({
    'name': 'Male',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})


# ---------- Suppliers ----------
Male_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Male,
                        }).config)

Male_C5_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C5',
                        config={
                            'env': env,
                            'base': Male,
                        }).config)

Male_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Male,
                        }).config)

Male_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Male,
                        }).config)
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((Kauri Point)))))))))))))))))))))))))))))

# ---------- Base ----------
KauriPoint = bases.Base({
    'name': 'Kauri Point',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})


# ---------- Suppliers ----------
KauriPoint_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': KauriPoint,
                        }).config)

KauriPoint_C5_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C5',
                        config={
                            'env': env,
                            'base': KauriPoint,
                        }).config)

KauriPoint_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': KauriPoint,
                        }).config)

KauriPoint_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': KauriPoint,
                        }).config)
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((Tauranga)))))))))))))))))))))))))))))))

# ---------- Base ----------
Tauranga = bases.Base({
    'name': 'Tauranga',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# ---------- Suppliers ----------
Tauranga_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Tauranga,
                        }).config)

Tauranga_C5_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C5',
                        config={
                            'env': env,
                            'base': Tauranga,
                        }).config)

Tauranga_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Tauranga,
                        }).config)

Tauranga_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Tauranga,
                        }).config)

# endregion ====================================================================


# region: (((((((((((((((((((((((((((((Pearl Harbor)))))))))))))))))))))))))))))

# ---------- Base ----------
PearlHarbor = bases.Base({
    'name': 'Pearl Harbor',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# ---------- Suppliers ----------
PearlHarbor_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': PearlHarbor,
                        }).config)

PearlHarbor_C5_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C5',
                        config={
                            'env': env,
                            'base': PearlHarbor,
                        }).config)

PearlHarbor_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': PearlHarbor,
                        }).config)

PearlHarbor_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': PearlHarbor,
                        }).config)
# endregion ====================================================================


# region: ((((((((((((((((((((((((((((((Animation))))))))))))))))))))))))))))))
# Queue length line plot
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

# ---------- Consumers ---------- Queue
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

# ---------- Suppliers ---------- Queue
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


# region: (((((((((((((((((((((((((((((((Monitors)))))))))))))))))))))))))))))))
# all_queues_length = Guam.queue.length.merge(DGar.queue.length)
# all_queues_length = Guam.queue.length + DGar.queue.length
# endregion ====================================================================


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


os.system("Rscript plots/r_plots.R")
