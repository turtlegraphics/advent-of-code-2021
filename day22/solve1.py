#
# Advent of Code 2021
# Bryan Clair
#
# Day 22 
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

parser = re.compile(r"(\w+) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)")

box = []
for line in inputlines:
    vals = parser.match(line).groups()
    switch = (vals[0] == 'on')
    ivals = [int(x) for x in vals[1:]]
    low = (ivals[0],ivals[2],ivals[4])
    high = (ivals[1],ivals[3],ivals[5])
    box.append((switch,low,high))

reactor = {}

for b in box:
    switch,low,high = b
    if max(low) > 50 or min(low) < -50 or max(high) > 50 or min(high) > 50:
        continue
    for x in range(low[0],high[0]+1):
        for y in range(low[1],high[1]+1):
            for z in range(low[2],high[2]+1):
                reactor[(x,y,z)] = switch

count = 0
for p in reactor:
    if reactor[p]:
        count += 1

print 'part 1:', count
