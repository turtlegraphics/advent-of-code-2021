#
# Advent of Code 2021
# Bryan Clair
#
# Day 03
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]
report = [[int(x) for x in list(line)] for line in inputlines]

bitlen = len(report[0])

def most_common(report, position):
    """return the most common bit in given position"""
    counts = [0,0]
    for row in report:
        counts[row[position]] += 1
    if counts[0] > counts[1]:
        return 0
    return 1

gamma = ''
epsilon = ''

for i in range(bitlen):
    common = most_common(report,i)
    if common == 0:
        gamma += '0'
        epsilon  += '1'
    else:
        gamma += '1'
        epsilon  += '0'

print 'part 1:', int(gamma,2)*int(epsilon,2)

oxygen = [r for r in report]
co2 = [r for r in report]

for i in range(bitlen):
    oxcommon = most_common(oxygen, i)
    co2common = 1-most_common(co2, i)
    oxygen = [x for x in oxygen if x[i] == oxcommon]
    if len(co2) > 1:
        co2 =    [x for x in co2 if x[i] == co2common]


oval = int(''.join([str(x) for x in oxygen[0]]),2)
co2val = int(''.join([str(x) for x in co2[0]]),2)

print 'part 2:', oval * co2val
