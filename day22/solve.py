#
# Advent of Code 2021
# Bryan Clair
#
# Day 22 
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

parser = re.compile(r"(\w+) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)")

boxspec1 = []
boxspec2 = []
for line in inputlines:
    vals = parser.match(line).groups()
    switch = (vals[0] == 'on')
    ivals = [int(x) for x in vals[1:]]
    low = (ivals[0],ivals[2],ivals[4])
    high = (ivals[1],ivals[3],ivals[5])
    if not (max(low) > 50 or min(low) < -50 or max(high) > 50 or min(high) > 50):
        # inside init range
        boxspec1.append((switch,low,high))
    boxspec2.append((switch,low,high))

def clip1d(b1,b2):
    """Clip segment b1 by segment b2.
    Returns a list of (clip,x1,x2) where clip is True or False depending
    on whether the segment (x1,x2) is kept."""
    
    low1,high1 = b1
    low2,high2 = b2

    segs = []
    
    if low2 > high1 or high2 < low1:
        # no overlap
        segs.append( (True, low1, high1) )
        return segs

    clow = max(low1,low2)
    chigh = min(high1,high2)
    segs.append( (False, clow, chigh) )
    
    if low1 < low2:
        segs.append( (True, low1, clow-1 ) )
    if high1 > high2:
        segs.append( (True, chigh+1, high1 ) )

    return segs

def overlap(b1,b2):
    """True if the boxes overlap"""
    low1,high1 = b1
    low2,high2 = b2

    for i in range(2):
        if low2[i] > high1[i] or high2[i] < low1[i]:
            # no overlap
            return False
    return True

def clip(b1,b2):
    """Clip box b1 by box b2.
    Returns a list of boxes."""
    low1,high1 = b1
    low2,high2 = b2
    
    segs = []
    for i in range(3):
        segs.append(clip1d((low1[i],high1[i]), (low2[i],high2[i])))

    boxes = []
    for sx in segs[0]:
        kx, lx, hx = sx
        for sy in segs[1]:
            ky, ly, hy = sy
            for sz in segs[2]:
                kz, lz, hz = sz
                if kx or ky or kz:
                    boxes.append( ((lx, ly, lz), (hx, hy, hz)) )

    return boxes

def volume(boxes):
    vol = 0
    for b in boxes:
        low,high = b
        v = 1
        for i in range(3):
            v = v * (high[i]-low[i]+1)
        vol += v
    return vol

def react(boxspec,quiet = True):
    boxes = []
    count = 0
    tick = 10
    for newb in boxspec:
        count += 1
        pct = 100*count/float(len(boxspec))
        if pct >= tick:
            if not quiet:
                print pct,'% done'
            tick += 10

        newboxes = []
        switch, low, high = newb
        for b in boxes:
            if overlap(b, (low,high) ):
                newboxes = newboxes + clip(b, (low,high) )
            else:
                newboxes.append(b)
        if switch:
            newboxes.append( (low,high) )
        boxes = newboxes
    return volume(boxes)

v1 = react(boxspec1)
v2 = react(boxspec2,quiet=False)
print 'part 1:',v1
print 'part 2:',v2
