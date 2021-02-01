import salabim as sim
import crayons as cr
from globals import *

# Verbose logging setup
verbose = VERBOSE_ALL or VERBOSE_ANIMATION
cprint = MAKE_CPRINT(verbose, VERBOSE_ANIMATION_COLOR)
cprint(f"animation.py verbose output ON")


margins = {
    'top': 10,
    'bottom': 10,
    'left': 10,
    'right': 10,
    'general': 10
}

# ***** Queue Length Line Plot Parameters *****
q_lineplot_x_left = margins['left']
q_lineplot_y_bottom = margins['bottom'] + 450

q_lineplot_height = 300
q_lineplot_width = 500

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# ***** Queue Length of Stay Histogram Parameters *****
q_LOS_hist_x_left = q_lineplot_x_left + q_lineplot_width + margins['general']
q_LOS_hist_y_top = q_lineplot_y_bottom + q_lineplot_height
cprint(f'q_LOS_hist_y_top: {q_LOS_hist_y_top}')
q_lineplot_height = 300
q_lineplot_width = 500

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# ********** Resource Bar Animation **********
# Bottom and Top y-values #
resource_bar_y_bottom = margins['bottom'] + 0
resource_bar_height = 30
resource_bar_y_top = resource_bar_y_bottom + resource_bar_height

# Label Left and Right x-values #
resource_bar_label_x_left = margins['left'] + 0
resource_bar_label_width = 250
resource_bar_label_x_right = resource_bar_label_x_left + resource_bar_label_width
# Label Specification
resource_label_spec = (resource_bar_label_x_left,
                       resource_bar_y_bottom,
                       resource_bar_label_x_left + resource_bar_label_width,
                       resource_bar_y_top)


def resource_label_text(arg, t):
    return(
        f'TLAMs Available: {str(round(arg.available_quantity()))}'
    )


# Bar Left and Right x-values #
resource_bar_x_left = resource_bar_label_x_right + 10
resource_bar_width = 1000
resource_bar_x_right = resource_bar_x_left + resource_bar_width


def resource_bar_spec(arg, t):
    '''Bar Specification function'''

    return (
        resource_bar_x_left,
        resource_bar_y_bottom,
        resource_bar_x_left + 2 * arg.available_quantity(),
        resource_bar_y_top)


def resource_bar_text(arg, t):
    '''Bar text specification function'''

    return(
        str(round(arg.available_quantity()))
    )


# Queue Animation
queue_x_left = margins['left']
queue_y_bottom = resource_bar_y_top + margins['general'] + 40

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
