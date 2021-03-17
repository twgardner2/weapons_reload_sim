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


# region: ((((((((((((((((((((((((((((((((Node1))))))))))))))))))))))))))))))))
# ---------- Base ----------
Node1 = bases.Base({
    'name': 'Node1',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 2,
})

# ---------- Consumers ----------
for i in range(8):
    con.ConsumerGenerator(
        con.ConsumerConfig(
            consumer_type='DDG',
            config={
                'env': env,
                'base': Node1,
                'gen_dist': sim.Normal(13 * 24, 3 * 24),
            }).config
    )

# Node1_CustGen = con.ConsumerGenerator(
#     con.ConsumerConfig(
#         consumer_type='DDG',
#         config={
#             'env': env,
#             'base': Node1,
#             'gen_dist': sim.IntUniform(140, 180),
#         }).config)

# ---------- Suppliers ----------
Node1_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Node1,
                            'gen_dist': sim.IntUniform(6 * 24, 12 * 24)
                        }).config)

sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Node1,
                            'gen_time': [0]
                        }).config)

Node1_NGLS_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='NGLS',
                        config={
                            'env': env,
                            'base': Node1,
                        }).config)

# Node1_C5_Generator = sup.SupplierGenerator(
#     sup.Supplier_Config(supplier_type='C5',
#                         config={
#                             'env': env,
#                             'base': Node1,
#                         }).config)

# Node1_C17_Generator = sup.SupplierGenerator(
#     sup.Supplier_Config(supplier_type='C17',
#                         config={
#                             'env': env,
#                             'base': Node1,
#                         }).config)

# Node1_C130_Generator = sup.SupplierGenerator(
#     sup.Supplier_Config(supplier_type='C130',
#                         config={
#                             'env': env,
#                             'base': Node1,
#                         }).config)
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((Node2)))))))))))))))))))))))))))))))))
# ---------- Base ----------
Node2 = bases.Base({
    'name': 'Node2',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 4,
})

# CRUDESs arriving at Node2
Node2_CustGen = con.ConsumerGenerator(
    con.ConsumerConfig(
        consumer_type='DDG',
        config={
            'env': env,
            'base': Node2,
            'gen_dist': sim.IntUniform(140, 180),
        }).config)

# ---------- Suppliers ----------
Node2_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Node2,
                        }).config)

Node2_C5_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C5',
                        config={
                            'env': env,
                            'base': Node2,
                        }).config)

Node2_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Node2,
                        }).config)

Node2_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Node2,
                        }).config)
# endregion ====================================================================


# region: ((((((((((((((((((((((((((((((((Node3))))))))))))))))))))))))))))))))
# ---------- Base ----------
Node3 = bases.Base({
    'name': 'Node3',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 2,
})

Node3_CustGen = con.ConsumerGenerator(
    con.ConsumerConfig(
        consumer_type='DDG',
        config={
            'env': env,
            'base': Node3,
            'gen_dist': sim.IntUniform(140, 180),
        }).config)

# ---------- Suppliers ----------
Node3_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Node3,
                            # 'gen_dist': None,
                            # 'gen_time': [1e9],
                        }).config)

Node3_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Node3,
                            'gen_dist': None,
                            'gen_time': [1e9],
                        }).config)

Node3_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Node3,
                            'gen_dist': None,
                            'gen_time': [1e9],
                        }).config)
# endregion ====================================================================


# region: ((((((((((((((((((((((((((((((((Node4))))))))))))))))))))))))))))))))

# ---------- Base ----------
Node4 = bases.Base({
    'name': 'Node4',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# ---------- Consumers ----------
Node4_CG_CustGen = con.ConsumerGenerator(
    con.ConsumerConfig(
        consumer_type='DDG',
        config={
            'env': env,
            'base': Node4,
            'gen_dist': sim.IntUniform(240, 280),
        }).config)


# ---------- Suppliers ----------
Node4_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Node4,
                            'gen_dist': sim.IntUniform(15 * 24, 20 * 24)
                        }).config)

Node4_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Node4,
                        }).config)

Node4_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Node4,
                        }).config)
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((Node5)))))))))))))))))))))))))))))))

# ---------- Base ----------
Node5 = bases.Base({
    'name': 'Node5',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# ---------- Consumers ----------
Node5_CustGen = con.ConsumerGenerator(
    con.ConsumerConfig(
        consumer_type='DDG',
        config={
            'env': env,
            'base': Node5,
            'gen_dist': sim.IntUniform(140, 180),
        }).config)

# ---------- Suppliers ----------
Node5_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Node5,
                        }).config)

Node5_C5_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C5',
                        config={
                            'env': env,
                            'base': Node5,
                        }).config)

Node5_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Node5,
                        }).config)

Node5_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Node5,
                        }).config)
# endregion ====================================================================


# region: ((((((((((((((((((((((((((((((((Node6))))))))))))))))))))))))))))))))
# ---------- Base ----------
Node6 = bases.Base({
    'name': 'Node6',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# ---------- Consumers ----------
Node6_CustGen = con.ConsumerGenerator(
    con.ConsumerConfig(
        consumer_type='DDG',
        config={
            'env': env,
            'base': Node6,
            'gen_dist': sim.IntUniform(140, 180),
        }).config)

# ---------- Suppliers ----------
Node6_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Node6,
                        }).config)

Node6_C5_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C5',
                        config={
                            'env': env,
                            'base': Node6,
                        }).config)

Node6_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Node6,
                        }).config)

Node6_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Node6,
                        }).config)

# endregion ====================================================================


# region: ((((((((((((((((((((((((((((((((Node7))))))))))))))))))))))))))))))))

# ---------- Base ----------
Node7 = bases.Base({
    'name': 'Node7',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# ---------- Consumers ----------
Node7_CustGen = con.ConsumerGenerator(
    con.ConsumerConfig(
        consumer_type='DDG',
        config={
            'env': env,
            'base': Node7,
            'gen_dist': sim.IntUniform(140, 180),
        }).config)

# ---------- Suppliers ----------
Node7_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Node7,
                            'gen_dist': None,
                            'gen_time': [1],
                        }).config)

Node7_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Node7,
                        }).config)

Node7_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Node7,
                        }).config)
# endregion ====================================================================


# region: ((((((((((((((((((((((((((((((((Node8))))))))))))))))))))))))))))))))

# ---------- Base ----------
Node8 = bases.Base({
    'name': 'Node8',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# ---------- Consumers ----------
Node8_CustGen = con.ConsumerGenerator(
    con.ConsumerConfig(
        consumer_type='DDG',
        config={
            'env': env,
            'base': Node8,
            'gen_dist': sim.IntUniform(140, 180),
        }).config)

# ---------- Suppliers ----------
Node8_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Node8,
                        }).config)

Node8_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Node8,
                        }).config)

Node8_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Node8,
                        }).config)
# endregion ====================================================================


# region: ((((((((((((((((((((((((((((((((Node9))))))))))))))))))))))))))))))))
# ---------- Base ----------
Node9 = bases.Base({
    'name': 'Node9',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})


# ---------- Consumers ----------
Node9_CustGen = con.ConsumerGenerator(
    con.ConsumerConfig(
        consumer_type='DDG',
        config={
            'env': env,
            'base': Node9,
            'gen_dist': sim.IntUniform(140, 180),
        }).config)

# ---------- Suppliers ----------
Node9_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Node9,
                        }).config)

Node9_C5_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C5',
                        config={
                            'env': env,
                            'base': Node9,
                        }).config)

Node9_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Node9,
                        }).config)

Node9_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Node9,
                        }).config)

# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((Node10)))))))))))))))))))))))))))))))))

# ---------- Base ----------
Node10 = bases.Base({
    'name': 'Node10',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})


# ---------- Suppliers ----------
Node10_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Node10,
                        }).config)

Node10_C5_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C5',
                        config={
                            'env': env,
                            'base': Node10,
                        }).config)

Node10_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Node10,
                        }).config)

Node10_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Node10,
                        }).config)
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((Node11)))))))))))))))))))))))))))))

# ---------- Base ----------
Node11 = bases.Base({
    'name': 'Node11',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})


# ---------- Suppliers ----------
Node11_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Node11,
                        }).config)

Node11_C5_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C5',
                        config={
                            'env': env,
                            'base': Node11,
                        }).config)

Node11_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Node11,
                        }).config)

Node11_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Node11,
                        }).config)
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((Node12)))))))))))))))))))))))))))))))

# ---------- Base ----------
Node12 = bases.Base({
    'name': 'Node12',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 1,
})

# ---------- Suppliers ----------
Node12_TAKE_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='TAKE',
                        config={
                            'env': env,
                            'base': Node12,
                        }).config)

Node12_C5_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C5',
                        config={
                            'env': env,
                            'base': Node12,
                        }).config)

Node12_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Node12,
                        }).config)

Node12_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Node12,
                        }).config)

# endregion ====================================================================


# region: (((((((((((((((((((((((((((((Node13)))))))))))))))))))))))))))))

# ---------- Base ----------
Node13 = bases.Base({
    'name': 'Node13',
    'env': env,
    'reload_team': fast_ERT,
    'n_reload_team': 2,
})

# ---------- Suppliers ----------
Node13_C17_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C17',
                        config={
                            'env': env,
                            'base': Node13,
                        }).config)

Node13_C130_Generator = sup.SupplierGenerator(
    sup.Supplier_Config(supplier_type='C130',
                        config={
                            'env': env,
                            'base': Node13,
                        }).config)
# endregion ====================================================================


# region: ((((((((((((((((((((((((((((((Animation))))))))))))))))))))))))))))))
# Queue length line plot
# sim.AnimateMonitor(monitor=Node2.queue.length,
#                    x=ani.q_lineplot_x_left,
#                    y=ani.q_lineplot_y_bottom,
#                    width=ani.q_lineplot_width,
#                    height=ani.q_lineplot_height,
#                    horizontal_scale=0.15,
#                    vertical_scale=7.5)
# # > Queue length of stay histogram
# sim.AnimateText(text=lambda: Node2.queue.length_of_stay.print_histogram(as_str=True),
#                 x=ani.q_LOS_hist_x_left,
#                 y=ani.q_LOS_hist_y_top,
#                 text_anchor='nw',
#                 font='narrow',
#                 fontsize=10)

# # Node2 Animation
# qa0 = sim.AnimateQueue(
#     queue=Node2.queue,
#     x=ani.queue_x_left + 50,
#     y=ani.queue_y_bottom,
#     title='Queue of Ships Waiting for Reload at Node2',
#     direction='e',
#     id='blue',
# )
# # sim.AnimateRectangle(spec=ani.resource_bar_spec,
# #                      arg=Node2.resource)
# sim.AnimateRectangle(spec=ani.resource_label_spec,
#                      text=ani.resource_label_text,
#                      arg=Node2.resource)

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
# all_queues_length = Node2.queue.length.merge(Node1.queue.length)
# all_queues_length = Node2.queue.length + Node1.queue.length
# endregion ====================================================================


# Run simulation
env.animation_parameters(animate=ANIMATE, speed=SIM_SPEED)  # , width=1500

env.background_color('20%gray')
env.run(till=SIM_LENGTH)

# Simulation statistics
# bases.base1.config.get('resource').print_histograms()
# bases.base1.config.get('resource').print_statistics()
# bases.base1.config.get('resource').print_info()


# Node2.length_of_stay.print_histogram()
# TLAMs1.occupancy.print_histogram()
# Node2.print_info()


# queue2.length_of_stay.print_histogram()
# queue2.print_info()

# Node2.queue.length.print_histogram()
# Node1.queue.length.print_histogram()
# print(all_queues_length)
# all_queues_length.print_histogram()
# Node2.queue.length.merge(
#     Node1.queue.length, name='combined queues').print_histogram()
# all_queues_length.print_histogram()

# print(bases.Base.getInstances())

# print([base.queue.length() for base in bases.Base.getInstances()])

# sum(base.queue.length for base in bases.Base.getInstances()
#     ).print_histogram()

# endregion ====================================================================

if CREATE_PLOTS:
    os.system(
        f'Rscript --verbose plots/r_plots.R {PLOT_DAY_NIGHT_SHADING} {SHOW_SUPPLIER_ARRIVALS}')
