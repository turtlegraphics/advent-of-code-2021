#
# Advent of Code 2021
# Bryan Clair
#
# Day 08
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

def common(s1,s2):
    """Return a list of common characters between two strings"""
    c1 = list(s1)
    c2 = list(s2)
    result = []
    for c in c1:
        if c in c2:
            result.append(c)
    return result

def segint(s1,s2):
    """Return the number of segments two patterns have in common"""
    return len(common(s1,s2))

def solve(patterns):
    codes = {}
    fives = []
    sixes = []
    for p in patterns:
        if len(p) == 2:
            codes[1] = p
        elif len(p) == 3:
            codes[7] = p
        elif len(p) == 4:
            codes[4] = p
        elif len(p) == 7:
            codes[8] = p
        elif len(p) == 5:
            fives.append(p)
        elif len(p) == 6:
            sixes.append(p)
        else:
            assert(False)

    assert(len(sixes) == 3)
    for p in sixes:
        if segint(p,codes[1]) == 1:
            codes[6] = p
        else:
            if segint(p,codes[4]) == 3:
                codes[0] = p
            else:
                codes[9] = p

    for p in fives:
        if segint(p,codes[9]) == 4:
            codes[2] = p
        else:
            if segint(p,codes[1]) == 1:
                codes[5] = p
            else:
                codes[3] = p

    assert(len(codes) == 10)
    return codes

def decode(o,codes):
    for i in range(10):
        if segint(o,codes[i]) == max(len(o),len(codes[i])):
            return i

outputsum = 0
uniques = 0
for line in inputlines:
    p, o = line.split('|')
    patterns = [x.strip() for x in p.split()]
    outputs = [x.strip() for x in o.split()]
    result = solve(patterns)
    
    total = 0
    for o in outputs:
        # count (for part 1)
        if len(o) in [2, 4, 3, 7]:
            uniques += 1
        val = decode(o,result)
        total = total*10 + val

    outputsum += total

print 'part 1:',uniques
print 'part 2:',outputsum
