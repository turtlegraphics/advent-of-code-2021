#
# Advent of Code 2021
# Bryan Clair
#
# Day 25
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]
inputlines.reverse()

floor = aocutils.Grid()
floor.scan(inputlines)

xmin, ymin, xmax, ymax = floor.bounds()
xlen = xmax + 1
ylen = ymax + 1

def movesouth():
    """Move the south herd, return True if they moved."""
    global floor
    tomove = []
    for x in range(xlen):
        for y in range(ylen):
            if floor[(x,y)] == 'v':
                p = (x,y)
                newy = (y + 1) % ylen
                if floor[(x,newy)] == '.':
                    tomove.append((x,y))

    for (x,y) in tomove:
        floor[(x,y)] = '.'
        newy = (y + 1) % ylen
        floor[(x,newy)] = 'v'

    return bool(tomove)

def moveeast():
    """Move the east herd, return True if they moved."""
    global floor
    tomove = []
    for x in range(xlen):
        for y in range(ylen):
            if floor[(x,y)] == '>':
                p = (x,y)
                newx = (x + 1) % xlen
                if floor[(newx,y)] == '.':
                    tomove.append((x,y))

    for (x,y) in tomove:
        floor[(x,y)] = '.'
        newx = (x + 1) % xlen
        floor[(newx,y)] = '>'

    return bool(tomove)

step = 0
moved = True
while moved:
    if step % 100 == 0:
        print 'step',step
#    floor.display(vflip=True)
    moved = moveeast()
    moved = movesouth() or moved
    step += 1

print 'stopped!'
print 'part 1:',step
