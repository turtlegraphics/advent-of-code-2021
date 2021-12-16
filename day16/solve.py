#
# Advent of Code 2021
# Bryan Clair
#
# Day 16
#
import sys
import re
sys.path.append("..")
import aocutils

import binascii

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

bits = []
for c in list(inputlines[0]):    
    for b in list(format(int(c, 16), "04b")):
        bits.append(b)

opnames = {
    0: 'sum',
    1: 'product',
    2: 'min',
    3: 'max',
    4: 'literal',
    5: 'greater than?',
    6: 'less than?',
    7: 'equal?'
}

def parse_literal(bits):
    i = 0
    val = 0
    while bits[i] == '1':
        val = val * 16 + int(''.join(bits[i+1:i+5]),2)
        i += 5
    val = val * 16 + int(''.join(bits[i+1:i+5]),2)
    i += 5

    print 'literal',val
    return (i,val)

def parse_operator(typeID, bits):
    parsed = 1
    vals = []
    if bits[0] == '0':
        total_length = int(''.join(bits[1:16]),2)
        parsed += 15
        while total_length > 0:
            (b,val) = parse(bits[parsed:])
            parsed += b
            vals.append(val)
            total_length -= b
    else:
        num_packets = int(''.join(bits[1:12]),2)
        parsed += 11
        for p in range(num_packets):
            (b,val) = parse(bits[parsed:])
            parsed += b
            vals.append(val)

    val = 0
    if typeID == 0:
        for v in vals:
            val += v
    elif typeID == 1:
        val = 1
        for v in vals:
            val *= v
    elif typeID == 2:
        val = vals[0]
        for v in vals:
            if v < val:
                val = v
    elif typeID == 3:
        val = vals[0]
        for v in vals:
            if v > val:
                val = v
    elif typeID == 5:
        val = 1 if vals[0] > vals[1] else 0
    elif typeID == 6:
        val = 1 if vals[0] < vals[1] else 0
    elif typeID == 7:
        val = 1 if vals[0] == vals[1] else 0

    print 'operator'
    print '  ',opnames[typeID],'of vals',vals
    print '   returning',val

    return (parsed,val)

totalversion = 0

def parse(bits):
    version = int(''.join(bits[0:3]),2)
    typeID = int(''.join(bits[3:6]),2)
    parsed = 6

    global totalversion
    totalversion += version

    if typeID == 4:
        # literal
        (b,val) = parse_literal(bits[6:])
        parsed += b
    else:
        # operator
        (b,val) = parse_operator(typeID, bits[6:])
        parsed += b

    return (parsed,val)

(parsed,val) = parse(bits)
print 'part 1:',totalversion
print 'part 2:',val
    


