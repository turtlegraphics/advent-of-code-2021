library(dplyr)
library(reshape2)
library(tidyr)
library(stringr)
library(readr)

inputpath <- "/Users/bryan/Documents/Puzzles/Advent 2021/day01/input.txt"

# Parse
inputlines <- read_file(inputpath) %>%
  strsplit('\n') %>% unlist()
depths <- as.numeric(inputlines)
windows <- na.omit(depths + lag(depths) + lag(depths,2))

part1 <- sum(diff(depths) > 0)
cat("part 1: ",part1)

part2 <- sum(diff(windows) > 0)
cat("part 2: ",part2)
