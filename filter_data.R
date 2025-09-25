library(tidyverse)

file <- "/Volumes/T7 Shield/Downloads/panel_data/ITA_PANEL.csv"

df <- read_csv(file)


df <- df %>% 
  mutate(
    nuts1 = as.factor(nuts1),
    nuts2 = as.factor(nuts2),
    nuts3 = as.factor(nuts3),
    city_latin_alphabet = as.factor(city_latin_alphabet)
  )


df_north <- df %>% 
  filter(
    str_detect(nuts1, "North")
  )


df_north %>% 
  summary


write_csv(df_north, "/Volumes/T7 Shield/Downloads/panel_data/ITA_NORTH_PANEL.csv")
