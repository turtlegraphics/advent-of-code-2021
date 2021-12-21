#
# Advent of Code 2021
# Bryan Clair
#
# Day 21
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()


pos = [8,6]
score = [0,0]

die = 1

rollcount = 0

def roll():
    global rollcount
    global die
    rollcount += 1
    v = die
    die += 1
    if die > 100:
        die = 1
    print v
    return v

who = 0
while score[0] < 1000 and score[1] < 1000:
    v = roll() + roll() + roll()
    pos[who] += v
    while pos[who] > 10:
        pos[who] -= 10
    score[who] += pos[who]
    who = 1-who
    if who == 0:
        print score

print 'position'
print pos
print 'score'
print score
print 'rollcount'
print rollcount

print

print score[0]*rollcount, score[1]*rollcount


