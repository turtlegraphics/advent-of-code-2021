#
# Advent of Code 2021
# Bryan Clair
#
# Day 12
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

caves = {}

for line in inputlines:
    c1,c2 = line.split("-")
    if c1 in caves:
        caves[c1].append(c2)
    else:
        caves[c1] = [c2]
    if c2 in caves:
        caves[c2].append(c1)
    else:
        caves[c2] = [c1]

def numpaths(v0,v1,twice):
#    print 'finding paths from',v0,'to',v1
    ways = 0

    for nbr in caves[v0]:
        if nbr == v1:
            ways += 1
        elif nbr.isupper():
            ways += numpaths(nbr,v1,twice)
        elif nbr not in visited:
            visited.append(nbr)
            ways += numpaths(nbr,v1,twice)
            visited.pop()
        elif nbr not in ['start','end'] and not twice:
            ways += numpaths(nbr,v1,True)

    return ways

visited = ['start']
print 'part 1:', numpaths('start','end',twice=True)
visited = ['start']
print 'part 2:', numpaths('start','end',twice=False)
