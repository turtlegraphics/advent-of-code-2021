#
# Advent of Code 2021
# Bryan Clair
#
# Day 02
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

class Sub():
    def __init__(self):
        self.h = 0
        self.depth = 0
        self.aim = 0

    def move(self,dir,x):
        if dir == "forward":
            self.h += x
            self.depth += self.aim*x
        if dir == "down":
            self.aim += x
        if dir == "up":
            self.aim -= x

hpos = 0
depth = 0

s = Sub()

for line in inputlines:
    dir, dist = line.split()
    dist = int(dist)
    s.move(dir,dist)

print s.h*s.depth

    

