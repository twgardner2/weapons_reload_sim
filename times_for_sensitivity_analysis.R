library(tidyverse)

base <- read_csv('/home/tom/Documents/weapons_reload_sim/output/BASE/output.csv', 
               col_names = c('time', 'base', 'key', 'value','value2','value3'))

node2 <- base %>% filter(base == "Node2")

node2_con <- node2 %>% filter(key == 'consumer_arrived')
node2_sup <- node2 %>% filter(key == 'supplier_arrived')

node2_con_times <- node2_con$time
node2_con_times

node2_sup_times_C130 <- node2_sup %>% filter(value2 == "C130") %>% .$time
node2_sup_times_C17 <- node2_sup %>% filter(value2 == "C17") %>% .$time
node2_sup_times_C5 <- node2_sup %>% filter(value2 == "C5") %>% .$time
node2_sup_times_TAKE <- node2_sup %>% filter(value2 == "TAKE") %>% .$time

node2_sup_times_C130
node2_sup_times_C17
node2_sup_times_C5
node2_sup_times_TAKE
