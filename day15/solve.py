#
# Advent of Code 2021
# Bryan Clair
#
# Day 15
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

def find_path(floor):
    xmin, ymin, xmax, ymax = floor.bounds()

    risk = aocutils.Grid()
    maxint = xmax*ymax*10
    for p in floor:
        risk[p] = maxint

    explore = []
    risk[(0,0)] = 0
    explore.append((0,0))

    cooldown = 100000
    while explore:
        cooldown -= 1
        if len(explore) % 1000 == 0 and cooldown < 0:
            print len(explore),'out of',(xmax+1)*(ymax+1),
            print 'nodes on the explore list'
            cooldown = 100000

        p = explore.pop(0)
        r_here = risk[p]
        nbrs = floor.neighbors(p)
        for n in nbrs:
            r_there = r_here + floor[n]
            if r_there < risk[n]:
                risk[n] = r_there
                explore.append(n)

    return risk[(xmax,ymax)]

small_floor = aocutils.Grid()
small_floor.scan(inputlines)
for p in small_floor:
    small_floor[p] = int(small_floor[p])

# small_floor.display(vflip=True)

print 'part 1:',find_path(small_floor)

xmin, ymin, xmax, ymax = small_floor.bounds()
w = xmax + 1
h = ymax + 1
big_floor = aocutils.Grid()
for p in small_floor:
    (x,y) = p
    for r in range(5):
        for c in range(5):
            v = small_floor[p]+r+c
            if v > 9:
                v -= 9
            big_floor[(x + w*r, y + h*c)] = v

v = find_path(big_floor)
print 'part 2:',v
