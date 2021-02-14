library(tidyverse)

model_output_path <- '/home/tom/Documents/weapons_reload_sim/output/'

df <- read_csv(file = file.path(model_output_path, 'output.csv'), 
               col_names = c('time', 'base', 'key', 'value'))

# Queue length plot
df_queue_length <- df %>% filter(key=='queue_length')
p <- ggplot(data = df_queue_length,
            mapping = aes(x=time, y=value, color=key)) +
    geom_step() + 
    facet_grid(rows = vars(base))
ggsave(filename = file.path(model_output_path, 'queue_length.png'),
       plot = p)

# Resources available plot
df_resources_avail <- df %>% filter(key=='resources_available')
p <- ggplot(data = df_resources_avail,
            mapping = aes(x=time, y=value, color=key)) +
  geom_step() + 
  facet_grid(rows = vars(base))
ggsave(filename = file.path(model_output_path, 'resources_available.png'),
       plot = p)
