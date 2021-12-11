#
# Advent of Code 2021
# Bryan Clair
#
# Day 11
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

octopi = aocutils.Grid()
y = 0
for line in inputlines:
    x = 0
    for d in [int(v) for v in list(line)]:
        octopi[(x,y)] = d
        x += 1
    y -= 1

flashcount = 0
step = 0
stepflash = 0
while stepflash < 100:
    stepflash = 0
    flashers = []
    for p in octopi:
        octopi[p] += 1
        if octopi[p] > 9:
            octopi[p] = -1
            flashers.append(p)
    
    while flashers:
        p = flashers.pop(0)
        flashcount += 1
        stepflash += 1
        # print p,'flashed'

        for n in octopi.neighbors(p,diagonal=True):
            if octopi[n] >= 0:
                # print '   ',n,'boosted'
                octopi[n] += 1
                if octopi[n] > 9:
                    octopi[n] = -1
                    flashers.append(n)

    for p in octopi:
        if octopi[p]<0:
            octopi[p] = 0

    step += 1
    if step == 100:
        print 'part 1:',flashcount

print 'part 2:', step
