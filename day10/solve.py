#
# Advent of Code 2021
# Bryan Clair
#
# Day 10
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

close =  {'(':')','[':']','{':'}','<':'>'}
ill_val =  {')':3, ']':57,'}':1197,'>':25137}
points =  {')':1, ']':2,'}':3,'>':4}

def balance(str):
    stack = []
    for c in list(str):
        if c in close:
            # it's an open delimiter
            stack.append(c)
        else:
            # it's a close delimiter
            expected = stack.pop()
            if close[expected] != c:
                raise Exception(c)

    return stack

ill_score = 0
allpoints = []
for line in inputlines:
    try:
        stack = balance(line)
        total = 0
        while stack:
            c = close[stack.pop()]
            total = 5*total + points[c]
        if total > 0:
            allpoints.append(total)

    except Exception as found:
        ill_score += ill_val[str(found)]

print 'part 1:',ill_score
allpoints.sort()
print 'part 2:',allpoints[len(allpoints)/2]


