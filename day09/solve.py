#
# Advent of Code 2021
# Bryan Clair
#
# Day 09
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

floor = aocutils.Grid()
y = 0
for line in inputlines:
    x = 0
    for d in [int(v) for v in list(line)]:
        floor[(x,y)] = d
        x += 1
    y -= 1

# floor.display()

risk = 0

basins = aocutils.Grid()
basincount = 0

for p in floor:
    depth = floor[p]
    low = True
    for n in floor.neighbors(p):
        if floor[n] <= floor[p]:
            low = False
    if low:
        risk += depth + 1
        basins[p] = basincount
        basincount += 1

print 'part 1: risk =',risk
print 'there are', basincount,'basins'

# basins.display()

changed = True
while changed:
    changed = False
    newbasins = aocutils.Grid()
    for p in basins:
        for n in floor.neighbors(p):
            if n not in basins and floor[n] < 9 and floor[n] > floor[p]:
                newbasins[n] = basins[p]
                changed = True

    for p in newbasins:
        basins[p] = newbasins[p]

    #print '----------'
    #basins.display()

sizes = [0]*basincount

for p in basins:
    sizes[basins[p]] += 1
sizes.sort()
print 'part 2:',sizes[-1]*sizes[-2]*sizes[-3]
