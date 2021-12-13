#
# Advent of Code 2021
# Bryan Clair
#
# Day 13
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

parser = re.compile(r"fold along (\w+)=(\d+)") # or whatever

folding = False
points = []

folds = []
for line in inputlines:
    if line == '':
        folding = True
    elif not folding:
        x,y = [int(v) for v in line.split(',')]
        points.append((x,y))
    else:
        axis, val = parser.match(line).groups()
        folds.append((axis,int(val)))

def printpoints(points):
    g = aocutils.Grid()
    for p in points:
        (x,y)= p
        g[(x,-y)] = '#'
    g.display(blank='.')

def fold(points, axis, where):
    newpoints = []
    for p in points:
        (x,y) = p
        if axis == 'y':
            if y > where:
                y = y - 2*(y-where)
        else:
            if x > where:
                x = x - 2*(x-where)
        if (x,y) not in newpoints:
            newpoints.append((x,y))
    return newpoints

first = True
for f in folds:
    axis, where = f
    points = fold(points, axis, where)
    if first:
        print 'part 1:',len(points)
        first = False

print 'part 2:'
printpoints(points)
