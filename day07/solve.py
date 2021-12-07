#
# Advent of Code 2021
# Bryan Clair
#
# Day 07
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

parser = re.compile(r"name: (\w+) val: (\d+)") # or whatever

vals = [int(x) for x in inputlines[0].split(',')]

sum = 0
for x in vals:
    sum += x

# post-competition "cleanup" of code to compute both parts..
# during the competition I only did the part I was working on

min1 = 100000000
min2 = 100000000

for target in range(1000):
    dist1 = 0
    dist2 = 0
    for x in vals:
        n = abs(x - target)
        dist1 += n
        dist2 += n*(n+1)/2

    if dist1 < min1:
        min1 = dist1
        best1 = target

    if dist2 < min2:
        min2 = dist2
        best2 = target

print 'part 1:',best1,'uses fuel:',min1
print 'part 2:',best2,'uses fuel:',min2
