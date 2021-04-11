import salabim as sim
import crayons
import datetime

# region: (((((((((((((((((((((((((Simulation Controls)))))))))))))))))))))))))
TRACE = 0
SIM_LENGTH = 60 * 24
SIM_SPEED = 32
ANIMATE = 0
# endregion ====================================================================

# region: ((((((((((((((((((((((((((((((Debugging))))))))))))))))))))))))))))))
VERBOSE_ALL = 0
VERBOSE_MAIN = 0
VERBOSE_BASE = 0
VERBOSE_CONSUMERS = 0
VERBOSE_SUPPLIERS = 0
VERBOSE_ANIMATION = 0

VERBOSE_MAIN_COLOR = crayons.yellow
VERBOSE_BASE_COLOR = crayons.blue
VERBOSE_CONSUMERS_COLOR = crayons.green
VERBOSE_SUPPLIERS_COLOR = crayons.magenta
VERBOSE_ANIMATION_COLOR = crayons.red


def MAKE_CPRINT(verbose, color):
    if verbose:
        def cprint(str):
            print(color(str, bold=True))
    else:
        def cprint(str):
            pass
    return cprint
# endregion ====================================================================


def is_daytime(simtime):
    time_of_day = simtime % 24
    if time_of_day >= 6 and time_of_day <= 18:
        # cprint(f'{simtime}: is DAYTIME')
        return True
    # cprint(f'{simtime}: is NIGHTTIME')
    return False


# region: ((((((((((((((((((((((((((((((((Output))))))))))))))))))))))))))))))))
OUTPUT = 1
OUTPUT_DIR = 'output/'
OUTPUT_SUBDIR = 'ERT_SENS/'
TIME = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
# QUEUE_OUTPUT_FILE = f'queue_lengths_{TIME}.csv'
QUEUE_OUTPUT_FILE = f'output.csv'

# Plots
CREATE_PLOTS = 1
# >> Queue length plot
PLOT_DAY_NIGHT_SHADING = 0
SHOW_SUPPLIER_ARRIVALS = 0
# endregion ====================================================================

NUMBER_OF_NODES_TAKE_SERVES = 5

# region: ((((((((((((((((((((((((((((((Consumers))))))))))))))))))))))))))))))
# defining CONSUMER_GENERATION_DIST overrides CONSUMER_GENERATION_TIMES
CONSUMER_INITIAL_DELAY = sim.Uniform(2 * 24, 9 * 24)  # used for base case
# CONSUMER_INITIAL_DELAY = sim.Constant(2 * 24)
# CONSUMER_GENERATION_DIST = sim.IntUniform(60, 110)
CONSUMER_GENERATION_DIST = sim.Uniform(7 * 24, 12 * 24)
# CONSUMER_GENERATION_DIST = None
CONSUMER_GENERATION_TIMES = [90.79066, 106.09239, 124.90767, 139.58267, 159.16610, 162.69245, 173.56653, 182.03732, 411.39817, 426.42268, 443.92510, 525.30269, 539.28258,
                             544.50600, 546.60131, 628.37381, 689.37248, 775.95700, 817.15438, 854.44863, 864.72499, 893.82298, 906.18687, 987.56915, 1006.71410, 1132.56552,
                             1160.06076, 1181.15994, 1267.75148, 1301.07262, 1324.20185, 1335.82771, 1377.58643, 1393.09976]

CG_FULL_LOADOUT = 122
DDG_FULL_LOADOUT = 96
FFG_FULL_LOADOUT = 50
SAG_FULL_LOADOUT = CG_FULL_LOADOUT + DDG_FULL_LOADOUT
# endregion ====================================================================

# region: ((((((((((((((((((((((((((((((Suppliers))))))))))))))))))))))))))))))
# defining SUPPLIER_GENERATION_DIST overrides SUPPLIER_GENERATION_TIMES
SUPPLIER_GENERATION_DIST = sim.IntUniform(500, 900)
# SUPPLIER_GENERATION_DIST = None
SUPPLIER_GENERATION_TIMES = list(range(500, 5000, 500))

ERT_SENS_TAKE_TIMES = [316.6146, 555.7496, 775.3963, 1001.1766, 1288.3890]
ERT_SENS_C5_TIMES = [20, 38, 61, 82, 104, 123, 143, 160, 177, 201, 213, 233, 253, 275, 297, 310, 333, 349, 368, 386, 405, 420, 440, 455, 467, 486, 504, 521,
                     535, 558, 579, 594, 617, 641, 665, 689, 701, 717, 729, 744, 765, 786, 802, 825, 848, 860, 881, 899, 922, 935, 957, 975, 995, 1017, 1030, 1050,
                     1065, 1081, 1096, 1114, 1132, 1154, 1173, 1190, 1204, 1217, 1233, 1248, 1270, 1287, 1305, 1326, 1338, 1362, 1385, 1399, 1415, 1437]
ERT_SENS_C17_TIMES = [22, 39, 55, 78, 99, 119, 135, 159, 183, 206, 221, 244, 263, 277, 292, 310, 332, 353, 366, 383, 403, 415, 437, 453, 475, 499, 516, 535,
                      559, 572, 584, 598, 622, 634, 647, 670, 692, 714, 732, 748, 761, 785, 808, 824, 847, 862, 884, 907, 929, 953, 975, 991, 1008, 1031, 1049, 1069,
                      1088, 1102, 1114, 1126, 1139, 1161, 1177, 1193, 1206, 1226, 1242, 1256, 1271, 1283, 1306, 1318, 1340, 1362, 1381, 1397, 1417, 1431]
ERT_SENS_C130_TIMES = [15, 33, 53, 66, 82, 103, 117, 135, 152, 170, 189, 213, 229, 243, 267, 279, 302, 320, 337, 355, 378, 399, 418, 438, 453, 467, 485, 503,
                       521, 543, 560, 575, 587, 599, 619, 640, 652, 676, 689, 705, 726, 745, 766, 788, 804, 816, 836, 848, 863, 879, 893, 908, 930, 942, 955, 969,
                       989, 1001, 1014, 1026, 1047, 1071, 1089, 1105, 1119, 1139, 1157, 1169, 1185, 1204, 1225, 1249, 1265, 1279, 1291, 1311, 1327, 1345, 1357, 1381, 1398, 1416, 1436]


TAKE_N_SUPPLIED = 960 / NUMBER_OF_NODES_TAKE_SERVES
NGLS_N_SUPPLIED = 8
C5_N_SUPPLIED = 18
C17_N_SUPPLIED = 12
C130_N_SUPPLIED = 2

SUPPLIER_UNLOAD_RATE = 8  # resources/hour
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((ERTs)))))))))))))))))))))))))))))))))
# - make reload time be missiles/hour
NUM_FAST_ERT = 3
NUM_SLOW_ERT = 3

RELOAD_TEAM_RATES = {
    'QRT': 4,
    'ERT': 8,
}
# endregion ====================================================================
