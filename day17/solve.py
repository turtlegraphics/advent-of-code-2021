#
# Advent of Code 2021
# Bryan Clair
#
# Day 17
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()


xmin,xmax = 111,161
ymin,ymax = -154,-101

def shoot(vx, vy):
    global hitcount

    x = 0
    y = 0
 
    ypeak = 0
    hit = False

    while y >= ymin and x <= xmax:
        if y > ypeak:
            ypeak = y
        if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
            hitcount += 1
            return ypeak

        x += vx
        y += vy
        vx = max(0, vx-1)
        vy -= 1

    return 0

hitcount = 0
highest = 0

for vx in range(xmax+1):
    for vy in range(ymin,400):
        height = shoot(vx,vy)
        if height > highest:
            highest = height

print 'part 1:', highest
print 'part 2:', hitcount
