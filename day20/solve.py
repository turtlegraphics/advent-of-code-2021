#
# Advent of Code 2021
# Bryan Clair
#
# Day 20
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

rule = list(inputlines[0])

g = aocutils.Grid()
g.scan(inputlines[2:],vflip=True)

dirs = [(-1,1),(0,1),(1,1),
        (-1,0),(0,0),(1,0),
        (-1,-1),(0,-1),(1,-1)]

oob = '.'
for i in range(50):
    xmin,ymin,xmax,ymax = g.bounds()
    xmin -= 1
    ymin -= 1
    xmax += 1
    ymax += 1

    lit = 0
    h = aocutils.Grid()
    for x in range(xmin,xmax+1):
        for y in range(ymin,ymax+1):
            p = aocutils.Point(x,y)
            num = 0
            for d in dirs:
                q = p + aocutils.Point(d)
                try:
                    val = g[q]
                except KeyError:
                    val = oob
                num = num*2 + (1 if val == '#' else 0)
            newval = rule[num]
            if newval == '#':
                lit += 1
            h[p] = newval
    if i % 2:
        print 'step',i+1,'lit:',lit,
        if i+1 == 2:
            print '<-- part 1'
        elif i+1 == 50:
            print '<-- part 2'
        else:
            print

    if oob == '.':
        oob = '#'
    else:
        oob = '.'
    g = h

