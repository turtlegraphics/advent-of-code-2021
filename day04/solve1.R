library(dplyr)
library(reshape2)
library(tidyr)
library(stringr)
library(readr)

inputpath <- "/Users/bryan/Documents/Puzzles/Advent 2021/day04/input.txt"

# Parse
records <- read_file(inputpath) %>%
  strsplit('\n\n') %>% unlist()
boards <- records[-1] %>% str_remove("^ ") %>% strsplit('[ \n]+',fixed=FALSE)
boards <- do.call(rbind, boards)
nboards <- nrow(boards)
calls <- unlist(strsplit(records[1],','))

# winning patterns
patterns <- matrix(FALSE,12,25)
patterns[ 1, 1: 5] <- TRUE
patterns[ 2, 6:10] <- TRUE
patterns[ 3,11:15] <- TRUE
patterns[ 4,16:20] <- TRUE
patterns[ 5,21:25] <- TRUE
patterns[ 6,seq(1,25,5)] <- TRUE
patterns[ 7,seq(2,25,5)] <- TRUE
patterns[ 8,seq(3,25,5)] <- TRUE
patterns[ 9,seq(4,25,5)] <- TRUE
patterns[10,seq(5,25,5)] <- TRUE
patterns[11,seq(1,25,6)] <- TRUE
patterns[12,seq(5,24,4)] <- TRUE

checkwin <- function (p) {
  apply(is.na(boards[1:nboards,patterns[p,]]),1,all)
}

for (c in calls) {
  boards[boards==c] <- NA
  won <- apply(sapply(1:12, checkwin),1,any)
  if (any(won)) {
    winner <- which(won)
    break
  }
}

print('winning board')
print(winner)
print("number just called")
print(c)
print("board sum")
boardsum <- sum(as.integer(boards[winner,]),na.rm=TRUE)
print(boardsum)
print("part 1:")
print(as.integer(c)*boardsum)
