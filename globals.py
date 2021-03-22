import salabim as sim
import crayons
import datetime

# region: (((((((((((((((((((((((((Simulation Controls)))))))))))))))))))))))))
TRACE = 0
SIM_LENGTH = 80 * 24
SIM_SPEED = 32
ANIMATE = 0
# endregion ====================================================================

# region: ((((((((((((((((((((((((((((((Debugging))))))))))))))))))))))))))))))
VERBOSE_ALL = 0
VERBOSE_MAIN = 0
VERBOSE_BASE = 1
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
CONSUMER_INITIAL_DELAY = sim.Uniform(2 * 24, 9 * 24)
# CONSUMER_GENERATION_DIST = sim.IntUniform(60, 110)
CONSUMER_GENERATION_DIST = sim.Uniform(7 * 24, 12 * 24)
# CONSUMER_GENERATION_DIST = None
CONSUMER_GENERATION_TIMES = list(range(1, 300, 50))

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

FAST_ERT_RELOAD_RATE = 4
SLOW_ERT_RELOAD_RATE = 2
RELOAD_TEAM_RATES = {
    'QRT': 4,
    'ERT': 2,
}
# endregion ====================================================================
