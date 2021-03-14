import salabim as sim
import crayons
import datetime

# region: (((((((((((((((((((((((((Simulation Controls)))))))))))))))))))))))))
TRACE = 0
SIM_LENGTH = 20 * 24
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
PLOT_DAY_NIGHT_SHADING = 0
# endregion ====================================================================

# region: ((((((((((((((((((((((((((((((Consumers))))))))))))))))))))))))))))))
# defining CONSUMER_GENERATION_DIST overrides CONSUMER_GENERATION_TIMES
# CONSUMER_GENERATION_DIST = sim.IntUniform(60, 110)
CONSUMER_GENERATION_DIST = sim.Normal(50, 15)
# CONSUMER_GENERATION_DIST = None
# CONSUMER_GENERATION_TIMES = [3, 33, 333, 3333]
CONSUMER_GENERATION_TIMES = list(range(1, 300, 50))
# CONSUMER_N_CONSUMED_DIST = sim.IntUniform(8, 96)
CONSUMER_N_CONSUMED_DIST = sim.IntUniform(25, 25)

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

SUPPLIER_N_SUPPLIED = 1000
TAKE_N_SUPPLIED = 100
C5_N_SUPPLIED = 18
C17_N_SUPPLIED = 8
C130_N_SUPPLIED = 2

SUPPLIER_UNLOAD_RATE = 8  # resources/hour
# endregion ====================================================================


# region: (((((((((((((((((((((((((((((((((ERTs)))))))))))))))))))))))))))))))))
# - make reload time be missiles/hour
NUM_FAST_ERT = 3
NUM_SLOW_ERT = 3

FAST_ERT_RELOAD_RATE = 4
SLOW_ERT_RELOAD_RATE = 2
# endregion ====================================================================
