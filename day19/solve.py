#
# Advent of Code 2021
# Bryan Clair
#
# Day 19
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

cubegroup = [
    "","a","aa","aaa",
     "b","ba","baa","baaa",
     "bb","bba","bbaa","bbaaa",
     "bbb","bbba","bbbaa","bbbaaa",
     "ab","aba","abaa","abaaa",
     "aaab","aaaba","aaabaa","aaabaaa"
    ]

def transform(t,p):
    """Transform p by one of 0-23 numbered orientation transforms"""
    q = aocutils.Point3d(p)

    for move in list(cubegroup[t]):
        if move == 'a':
            # x-axis rot
            w = q.y
            q.y = q.z
            q.z = -w
        else:
            # y-axis rot
            w = q.x
            q.x = q.z
            q.z = -w

    return q

class Scanner:
    def __init__(self,id):
        self.id = id
        self.points = []

    def add(self,p):
        self.points.append(p)

    def distance_signature(self):
        try:
            return self.distances
        except:
            pass
        self.distances = {}
        for p1 in range(len(self.points)):
            for p2 in range(p1+1,len(self.points)):
                d = self.points[p1].dist2(self.points[p2])
                if d in self.distances:
                    self.distances[d].append((p1,p2))
                else:
                    self.distances[d] = [(p1,p2)]

        return self.distances

    def __str__(self):
        out = 'scanner %d sees %d beacons' % (self.id,len(self.points))
        return out

    def _match(self, other):
        matches = []
        odists = other.distance_signature()
        for pn in range(len(self.points)):
            p = self.points[pn]

            matchcounts = {}
            for x in range(len(other.points)):
                matchcounts[x] = 0

            for q in self.points:
                d = p.dist2(q)
                if d in odists:
                    for (o1,o2) in odists[d]:
                        matchcounts[o1] += 1
                        matchcounts[o2] += 1

            matched = False
            for x in matchcounts:
                if matchcounts[x] >= 11:
                    assert(matched == False)
                    matches.append((pn,x))
                    matched == True

        if len(matches) > 11:
            return matches
        return None

    def align(self,other, quick=False):
        matches = self._match(other)
        if matches == None:
            return None

        for t in range(24):
            (me,you) = matches[0]
            p = self.points[me]
            q = transform(t,other.points[you])
            onlyd = p - q

            matched = True

            count = 0
            for (me,you) in matches:
                p = self.points[me]
                q = transform(t,other.points[you])
                d = p - q
                if d != onlyd:
                    matched = False
                    break
            if matched:
                break

        assert(matched)

        if quick:
            return onlyd

        for p in other.points:
            q = transform(t,p) + onlyd
            found = False
            for r in self.points:
                if r == q:
                    found = True
                    break
            if not found:
                self.add(q)
        
# Read input
scanners = []
for line in inputlines:
    if line:
        if line[0:3] == '---':
            k = line.split()
            id = int(k[2])
            s = Scanner(id)
            scanners.append(s)
        else:
            p = aocutils.Point3d([int(v) for v in line.split(',')])
            s.add(p)

# Match 'em up

for i in range(len(scanners)-1):
    j = len(scanners)-i-2
    print j
    for k in range(j+1,len(scanners)):
        scanners[j].align(scanners[k])

print 'part 1:', len(scanners[0].points)

for s in scanners[1:]:
    s.align(scanners[0])

maxd = 0
count = len(scanners)
for s in scanners:
    print count
    count -= 1
    for t in scanners:
        d = s.align(t,quick=True)
        man = abs(d.x) + abs(d.y) + abs(d.z)
        if man > maxd:
            maxd = man

print 'part 2:',maxd
