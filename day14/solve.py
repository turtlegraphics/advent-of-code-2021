#
# Advent of Code 2021
# Bryan Clair
#
# Day 14
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

parser = re.compile(r"(\w+) -> (\w)") # or whatever

template = inputlines[0]

# build rules
rules = {}
for line in inputlines[2:]:
    pair, insert = parser.match(line).groups()
    a,b = list(pair)
    rules[pair] = (a+insert,insert+b)

# build initial counts of pairs
counts = {}
for i in range(len(template)-1):
    pair = list(template)[i]+list(template)[i+1]
    try:
        counts[pair] += 1
    except:
        counts[pair] = 1

def checksum(counts):
    """Find frequency of each letter,
    then find the most and least common letter,
    then return the most count minus the least count."""
    # count elements
    lettercounts = {}
    for pair in counts:
        x,y = list(pair)
        if x not in lettercounts:
            lettercounts[x] = 0
        if y not in lettercounts:
            lettercounts[y] = 0

        lettercounts[x] += counts[pair]
        lettercounts[y] += counts[pair]

    lettercounts[list(template)[0]] += 1
    lettercounts[list(template)[-1]] += 1

    for x in lettercounts:
        lettercounts[x] /= 2

    maxl=0
    minl=10000000000000000000000

    for x in lettercounts:
        if lettercounts[x] > maxl:
            maxl = lettercounts[x]
        if lettercounts[x] < minl:
            minl = lettercounts[x]

    return maxl - minl

# Count pairs
for step in range(40):
    polylen = 1
    for pair in counts:
        polylen += counts[pair]
#    print 'step',step
#    print 'length', polylen

    newcounts = {}
    for pair in counts:
        x,y = rules[pair]
        if x not in newcounts:
            newcounts[x] = 0
        if y not in newcounts:
            newcounts[y] = 0
        newcounts[x] += counts[pair]
        newcounts[y] += counts[pair]
    counts = newcounts

    if step==9:
        print 'part 1:',checksum(counts)
 
print 'part 2:',checksum(counts)
