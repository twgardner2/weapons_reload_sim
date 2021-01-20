import salabim as sim

margins = {
    "top": 10,
    "bottom": 10,
    "left": 10,
    "right": 10,
    "general": 10
}

# Resource Bar Animation
# Bottom and Top y-values #
resource_bar_y_bottom = margins['bottom'] + 0
resource_bar_height = 30
resource_bar_y_top = resource_bar_y_bottom + resource_bar_height

# Label Left and Right x-values #
resource_bar_label_x_left = margins['left'] + 0
resource_bar_label_width = 150
resource_bar_label_x_right = resource_bar_label_x_left + resource_bar_label_width
# Label Specification
resource_label_spec = (resource_bar_label_x_left,
                       resource_bar_y_bottom,
                       resource_bar_label_x_left + resource_bar_label_width,
                       resource_bar_y_top)

# Bar Left and Right x-values #
resource_bar_x_left = resource_bar_label_x_right + 10
resource_bar_width = 1000
resource_bar_x_right = resource_bar_x_left + resource_bar_width

# Bar Specification function


def resource_bar_spec(arg, t): return (
    resource_bar_x_left,
    resource_bar_y_bottom,
    resource_bar_x_left + 2 * arg.available_quantity(),
    resource_bar_y_top)

# Bar text specification function


def resource_bar_text(arg, t): return(
    str(round(arg.available_quantity()))
)


# Queue Animation
queue_x_left = margins['left']
queue_y_bottom = resource_bar_y_top + margins['general']
