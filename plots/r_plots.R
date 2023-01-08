library(tidyverse)
library(scales)

# Collect arguments
args <- commandArgs(trailingOnly = TRUE)
OUTPUT_SUBDIR <- args[1]

print(OUTPUT_SUBDIR)
theme_set(theme_minimal())

model_output_path <- file.path('/home/tom/Documents/weapons_reload_sim/output', OUTPUT_SUBDIR)
dir.create(model_output_path, showWarnings = FALSE)

integer_breaks <- function(x) unique(floor(pretty(seq(0, (max(x) + 1) * 1.1))))

df <- read_csv(file = file.path(model_output_path, 'output.csv'), 
               col_names = c('time', 'base', 'key', 'value','value2','value3'))


# Queue length plot
# > Node names in order, used for setting as factor levels
node_names_in_order <- c('Node1','Node2','Node3','Node4',
                         'Node5','Node6')

# node_names_in_order <- c('Node2_1-ERT','Node2_2-ERT','Node2_3-ERT','Node2_4-ERT')

# > Separate out queue length and supplier arrival data
df_f <- df %>% 
  # mutate(base_f = factor(base))
  mutate(base_f = factor(base, levels = node_names_in_order))

df_queue_length <- df_f %>% 
  filter(key=='queue_length')
df_supplier_arrived <- df_f %>% 
  filter(key=='supplier_arrived')
df_resources_avail <- df_f %>% 
  filter(key=='resources_available')
df_consumers_departed <- df_f %>% 
  filter(key=='consumer_departed')


# > Create queue length plot -------------------------------------------------------------------------
basic_queue_length <- ggplot(data = df_queue_length,
            mapping = aes(x=time/24, y=value, color=key)) +
    geom_step(show.legend = FALSE) + 
    facet_grid(rows = vars(base_f)) +
  theme(
      strip.text.x = element_text(size = 8, color = "black", face = "plain"),
      strip.text.y = element_text(size = 8, color = "black", face = "plain")
    ) +
	labs(title = 'Ship Queue at Nodes') +
	xlab('Time (days)') +
  ylab('Ships in Queue') +
  scale_y_continuous(breaks = integer_breaks) 

# Save basic queue length plot
ggsave(filename = file.path(model_output_path, 'queue_length_basic.png'),
       plot = basic_queue_length)

# Add day/night shading to plot ----------------------------------------------------------

# Get x and y limits of faceted plot to make nighttime hours shaded
x_lim <- ggplot_build(basic_queue_length)$layout$panel_scales_x[[1]]$range$range
y_lim <- ggplot_build(basic_queue_length)$layout$panel_scales_y[[1]]$range$range
dusk <- c(0/24, seq(18/24, x_lim[2], 24/24))
dawn <- c(6/24, seq(30/24, x_lim[2], 24/24))

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
				mapping = aes(x=time/24, color=value2, shape=value2),
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
  ) +
  scale_y_continuous(labels=scales::comma)
ggsave(filename = file.path(model_output_path, 'resources_available.png'),
       plot = p)

# Total Queue Length -----------------------------------------------------------------------
df_total_queue <- df %>% 
  filter(key == "queue_length") %>% 
  group_by(time) %>% 
  summarize(total_queue = sum(value))

p <- ggplot(data = df_total_queue,
            mapping = aes(x=time/24, y=total_queue)) +
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
  geom_step(data = df_resources_avail, mapping = aes(x=time/24, y=value/100, color=key)) +
  facet_grid(rows = vars(base_f)) +
  scale_y_continuous(
    breaks = integer_breaks,
    sec.axis = sec_axis(~.*100, name="Resources Available", labels=scales::comma)
  ) + 
  labs(title="Ship Queue and Resources Available") +
  theme(
    legend.position = "bottom",
    legend.title = element_blank(),
    axis.title.y.right = element_text(margin = margin(t = 0, r = 0, b = 0, l = 10)),
    axis.title.y.left = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0))
  ) +
  scale_color_discrete(labels = c('Queue Length', 'Resources Available')) 

ggsave(filename = file.path(model_output_path, 'queue_and_resources.png'),
       plot = queue_length_resources_available)


make_base_queue_resource_plot <- function(filter_term, df_queue, df_resources) {
  print(filter_term)
  
  filename <- file.path(model_output_path, str_c(filter_term, '_queue_and_resources.png'))
  print(filename)
  # print(df_queue_length %>% filter(base=="Node1"))
  
  node_queue_data <- df_queue %>% filter(base == filter_term)
  print(node_queue_data)
  node_resources_data <- df_resources_avail %>% filter(base == filter_term)
  
  tmp <- ggplot(data = node_queue_data,
                mapping = aes(x=time/24, y=value, color=key)) +
          geom_step(show.legend = FALSE) + 
          # facet_grid(rows = vars(base_f)) +
          theme(
            strip.text.x = element_text(size = 8, color = "black", face = "plain"),
            strip.text.y = element_text(size = 8, color = "black", face = "plain")
          ) +
          geom_step(data = node_resources_data, 
                    mapping = aes(x=time/24, y=value/100, color=key)) +
          labs(title = str_c('Ship Queue and Resources Available at ', filter_term), color = 'asfd') +
          xlab('Time (days)') +
          # xlab('Time (hours)') +
          ylab('Ships in Queue') +
          scale_y_continuous(
            breaks = integer_breaks,
            sec.axis = sec_axis(~.*100, name="Resources Available", labels=scales::comma)
          ) + 
          theme(
            legend.position = "bottom",
            legend.title = element_blank(),
            axis.title.y.right = element_text(margin = margin(t = 0, r = 0, b = 0, l = 10)),
            axis.title.y.left = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0))
          ) +
        scale_color_discrete(labels = c('Queue Length', 'Resources Available')) 
    
  
  ggsave(filename = filename,
         plot = tmp,
         width = NA,
         height = 3,
         units = c("in"),
         dpi = 300)
  
}

purrr::map(unique(df$base), make_base_queue_resource_plot, df_queue_length, df_resources_avail)


# Cumulative ship wait time at each node ####
cum_queue_data <- df_queue_length %>% 
  # filter(key=="queue_length") %>% 
  group_by(base_f) %>% 
  complete(base_f, time, fill=list(value=0)) %>% 
  arrange(time) %>% 
  mutate(time_step_wait = (time-lag(time))*lag(value)) %>% 
  mutate(time_step_wait = ifelse(is.na(time_step_wait), 0, time_step_wait)) %>% 
  mutate(cum_wait = cumsum(time_step_wait)) 
  # ungroup() %>% 

# tmp <- df_queue_length %>% 
#   # filter(key=="queue_length") %>% 
#   group_by(base_f) %>% 
#   complete(base_f, time, fill=list(value=0)) %>% 
#   arrange(time) %>% 
#   mutate(time_step_wait = (time-lag(time))*lag(value)) %>% 
#   mutate(time_step_wait = ifelse(is.na(time_step_wait), 0, time_step_wait)) %>% 
#   mutate(cum_wait = cumsum(time_step_wait)) 

cum_queue_data %>% group_by(base_f) %>% arrange(time) %>% filter(row_number()==n())

plt <- ggplot(data = cum_queue_data, mapping = aes(x=time/24, y=cum_wait, color=base_f)) +
    geom_step() +
    labs(title = 'Cumulative Ship Queue Wait Time', color = 'Node') +
    xlab('Time (days)') +
    # xlab('Time (hours)') +
    ylab('Ship-Hours in Queue') +
    scale_y_continuous(labels=scales::comma) +
    theme(
        legend.position = "bottom",
        legend.title = element_blank(),
        axis.title.y.right = element_text(margin = margin(t = 0, r = 0, b = 0, l = 10)),
        axis.title.y.left = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0))
      ) 
plt


ggsave(filename = file.path(model_output_path, 'cumulative_wait_in_queue.png'),
       plot = plt,
       width = NA,
       height = 5,
       units = c("in"),
       dpi = 300)



# Cumulative Average Ship Wait Time at each Node
# Cumulative ship wait time at each node ####
# cum_queue_data <- df_queue_length %>% 
#   # filter(key=="queue_length") %>% 
#   group_by(base_f) %>% 
#   complete(base_f, time, fill=list(value=0)) %>% 
#   arrange(time) %>% 
#   mutate(time_step_wait = (time-lag(time))*lag(value)) %>% 
#   mutate(time_step_wait = ifelse(is.na(time_step_wait), 0, time_step_wait)) %>% 
#   mutate(cum_wait = cumsum(time_step_wait)) 
# # ungroup() %>% 
# 
# plt <- ggplot(data = cum_queue_data, mapping = aes(x=time/24, y=cum_wait, color=base_f)) +
#   geom_step() +
#   labs(title = 'Cumulative Ship Queue Wait Time', color = 'Node') +
#   xlab('Time (days)') +
#   # xlab('Time (hours)') +
#   ylab('Ship-Hours in Queue') +
#   scale_y_continuous(labels=scales::comma) +
#   theme(
#     legend.position = "bottom",
#     legend.title = element_blank(),
#     axis.title.y.right = element_text(margin = margin(t = 0, r = 0, b = 0, l = 10)),
#     axis.title.y.left = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0))
#   ) 
# plt
# 
# 
# ggsave(filename = file.path(model_output_path, 'cumulative_wait_in_queue.png'),
#        plot = plt,
#        width = NA,
#        height = 5,
#        units = c("in"),
#        dpi = 300)

# Total ships served by node
ships_served <- df_consumers_departed %>% 
  group_by(base_f) %>% 
  summarise(ships_served = n())
ships_served

