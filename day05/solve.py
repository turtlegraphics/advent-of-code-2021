#
# Advent of Code 2021
# Bryan Clair
#
# Day 05
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

parser = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")

grid = aocutils.Grid()

for line in inputlines:
    x0,y0,x1,y1 = [int(t) for t in parser.match(line).groups()]
    p0 = aocutils.Point(x0,y0)
    p1 = aocutils.Point(x1,y1)
    delta = (p1 - p0)
    if (delta.x == 0):
        delta.y = delta.y/abs(delta.y)
    elif (delta.y == 0):
        delta.x = delta.x/abs(delta.x)
    else:
        if (args.part == 1):
            #  only consider vertical or horizontal lines
            continue
        else:
            assert(abs(delta.x) == abs(delta.y))
            delta.x = delta.x/abs(delta.x)
            delta.y = delta.y/abs(delta.y)

    p = p0
    if p in grid:
        grid[p] += 1
    else:
        grid[p] = 1
    while (p != p1):
        p += delta
        if p in grid:
            grid[p] += 1
        else:
            grid[p] = 1

grid.display('.')

count = 0
for g in grid:
    if grid[g] > 1:
        count += 1

print
print 'part',args.part,':',count
