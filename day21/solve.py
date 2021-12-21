#
# Advent of Code 2021
# Bryan Clair
#
# Day 21
#
import sys
sys.path.append("..")
import aocutils

args = aocutils.parse_args()
inputlines = [x.strip() for x in open(args.file).readlines()]

start = [int(line.split(':')[1]) for line in inputlines]
# 8,6 for me

rolls = [1,2,3]
boardsize = 10
winscore = 21

space = {}
space[(0,start[0]-1,start[1]-1,0,0)] = 1  # (who, p1, p2, s1, s2)

wins = [0,0]

def turn(space):
    newspace = {}
    for state in space:
        count = space[state]
        for roll1 in rolls:
            for roll2 in rolls:
                for roll3 in rolls:
                    win = False
                    who,p1,p2,s1,s2 = state
                    if who == 0:
                        p1 = (p1 + roll1 + roll2 + roll3) % boardsize
                        s1 = s1 + p1 + 1
                        if s1 >= winscore:
                            wins[0] += count
                            win = True
                    else:
                        p2 = (p2 + roll1 + roll2 + roll3) % boardsize
                        s2 = s2 + p2 + 1
                        if s2 >= winscore:
                            wins[1] += count
                            win = True
                    if not win:
                        newstate = (1-who, p1, p2, s1, s2)
                        try:
                            newspace[newstate] += count
                        except KeyError:
                            newspace[newstate] = count
    return newspace

t = 1
while len(space) > 0:
    space = turn(space)
    print 'turn %2d: %6d states.' % (t, len(space)),
    print 'Wins for each player:', wins
    t += 1

print 'part 2:',wins[0]
