library(tidyverse)

# Collect arguments
args <- commandArgs(trailingOnly = TRUE)
PLOT_DAY_NIGHT_SHADING <- as.logical(as.integer(args[1]))


theme_set(theme_minimal())

model_output_path <- '/home/tom/Documents/weapons_reload_sim/output/'

df <- read_csv(file = file.path(model_output_path, 'output.csv'), 
               col_names = c('time', 'base', 'key', 'value','value2'))

# Queue length plot
df_queue_length <- df %>% filter(key=='queue_length')
df_supplier_arrived <- df %>% filter(key=='supplier_arrived')


p <- ggplot(data = df_queue_length,
            mapping = aes(x=time, y=value, color=key)) +
    geom_step(show.legend = FALSE) + 
    facet_grid(rows = vars(base)) +
    theme(
      strip.text.x = element_text(
        size = 4, color = "black", face = "plain"
      ),
      strip.text.y = element_text(
        size = 4, color = "black", face = "plain"
      )
    ) +
    geom_rug(data = df_supplier_arrived,
              # mapping = aes(x=time),
              mapping = aes(x=time, color=value2),
              sides = 'b')+
              # show.legend = FALSE) +
    ylim(0, max(df_queue_length$value))


x_lim <- ggplot_build(p)$layout$panel_scales_x[[1]]$range$range
y_lim <- ggplot_build(p)$layout$panel_scales_y[[1]]$range$range
dusk <- c(0, seq(18, x_lim[2], 24))
dawn <- c(6, seq(30, x_lim[2], 24))

if( length(dusk) != length(dawn) ) {
  dawn <- c(dawn, x_lim[2])
}

if(PLOT_DAY_NIGHT_SHADING) {
  p <- p + 
      annotate("rect",
              xmin = dusk,
              xmax = dawn,
              ymin = y_lim[1],
              ymax = y_lim[2],
              fill = 'lightgrey',
              alpha = .5) 
}



ggsave(filename = file.path(model_output_path, 'queue_length.png'),
       plot = p)

# Resources available plot
df_resources_avail <- df %>% filter(key=='resources_available')
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

# Total Queue Length
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
