library(tidyverse)

# Collect arguments
args <- commandArgs(trailingOnly = TRUE)
PLOT_DAY_NIGHT_SHADING <- as.logical(as.integer(args[1]))
SHOW_SUPPLIER_ARRIVALS <- as.logical(as.integer(args[2]))


theme_set(theme_minimal())

model_output_path <- '/home/tom/Documents/weapons_reload_sim/output/'

integer_breaks <- function(x) unique(floor(pretty(seq(0, (max(x) + 1) * 1.1))))

df <- read_csv(file = file.path(model_output_path, 'output.csv'), 
               col_names = c('time', 'base', 'key', 'value','value2', 'value3'))

# bases_to_keep <- c('Node1', 'Node2', 'Node3', 'Node4', 
# 					'Node5', 'Node6', 'Node7', 'Node8')
# 
# df <- df %>%
# 	filter(base %in% bases_to_keep)

# Queue length plot
# > Node names in order, used for setting as factor levels
node_names_in_order <- c('Node1','Node2','Node3','Node4',
                          'Node5','Node6','Node7','Node8',
                          'Node9','Node10','Node11','Node12',
                          'Node13')

# > Separate out queue length and supplier arrival data
df_f <- df %>% 
  mutate(base_f = factor(base, levels = node_names_in_order))
  
df_queue_length <- df_f %>% 
  filter(key=='queue_length')
df_supplier_arrived <- df_f %>% 
  filter(key=='supplier_arrived')
df_resources_avail <- df_f %>% 
  filter(key=='resources_available')


# > Create queue length plot -------------------------------------------------------------------------
basic_queue_length <- ggplot(data = df_queue_length,
            mapping = aes(x=time, y=value, color=key)) +
    geom_step(show.legend = FALSE) + 
    facet_grid(rows = vars(base_f)) +
    theme(
      strip.text.x = element_text(size = 8, color = "black", face = "plain"),
      strip.text.y = element_text(size = 8, color = "black", face = "plain")
    ) +
	labs(title = 'Ship Queue at Nodes') +
	xlab('Time (hours)') +
  ylab('Ships in Queue') +
  scale_y_continuous(breaks = integer_breaks) 

# Save basic queue length plot
ggsave(filename = file.path(model_output_path, 'queue_length_basic.png'),
       plot = basic_queue_length)

# Add day/night shading to plot ----------------------------------------------------------

# Get x and y limits of faceted plot to make nighttime hours shaded
x_lim <- ggplot_build(basic_queue_length)$layout$panel_scales_x[[1]]$range$range
y_lim <- ggplot_build(basic_queue_length)$layout$panel_scales_y[[1]]$range$range
dusk <- c(0, seq(18, x_lim[2], 24))
dawn <- c(6, seq(30, x_lim[2], 24))

if( length(dusk) != length(dawn) ) {
  dawn <- c(dawn, x_lim[2])
}

day_night_shaded_queue_length <- basic_queue_length + 
	labs(
		title = 'Ship Queue at Nodes',
		subtitle = 'Nighttime hours shaded grey'
	) +
    annotate("rect",
            xmin = dusk,
            xmax = dawn,
            ymin = y_lim[1],
            ymax = y_lim[2],
            fill = 'lightgrey',
            alpha = .5) 

# Save day/night shaded queue length plot
ggsave(filename = file.path(model_output_path, 'queue_length_day_night.png'),
       plot = day_night_shaded_queue_length)


# Add supplier arrivals to queue length -----------------------------------------------------
supplier_arrival_queue_length <- basic_queue_length + 
	labs(
		title = 'Ship Queue at Nodes with Supplier Arrivals',
		subtitle = waiver()
	) +
	geom_point(data = df_supplier_arrived,
				mapping = aes(x=time, color=value2, shape=value2),
				y= 0.75*y_lim[2])


ggsave(filename = file.path(model_output_path, 'queue_length_supplier_arrival.png'),
       plot = supplier_arrival_queue_length)

# Resources available plot ------------------------------------------------------------------
p <- ggplot(data = df_resources_avail,
            mapping = aes(x=time, y=value, color=key)) +
  geom_step(show.legend = FALSE) + 
  facet_grid(rows = vars(base)) +
  theme(
    strip.text.x = element_text(
      size = 6, color = "black", face = "plain"
    ),
    strip.text.y = element_text(
      size = 6, color = "black", face = "plain"
    )
  )
ggsave(filename = file.path(model_output_path, 'resources_available.png'),
       plot = p)

# Total Queue Length -----------------------------------------------------------------------
df_total_queue <- df %>% 
  filter(key == "queue_length") %>% 
  group_by(time) %>% 
  summarize(total_queue = sum(value))

p <- ggplot(data = df_total_queue,
            mapping = aes(x=time, y=total_queue)) +
  geom_step(show.legend = FALSE) + 
  theme(
    strip.text.x = element_text(
      size = 6, color = "black", face = "plain"
    ),
    strip.text.y = element_text(
      size = 6, color = "black", face = "plain"
    )
  )
ggsave(filename = file.path(model_output_path, 'total_queue.png'),
       plot = p)



# Make queue length and resources available plot (dual y-axes) ----------------------------
queue_length_resources_available <- basic_queue_length +
  geom_line(data = df_resources_avail, mapping = aes(x=time, y=value/250, color=key)) +
  facet_grid(rows = vars(base_f)) +
  scale_y_continuous(
    breaks = integer_breaks,
    sec.axis = sec_axis(~.*250, name="Resources Available")
  ) + 
  theme(legend.position="bottom")

ggsave(filename = file.path(model_output_path, 'queue_length_w_resources_avail.png'),
       plot = queue_length_resources_available)
