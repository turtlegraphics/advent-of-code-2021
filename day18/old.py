#
# Advent of Code 2021
# Bryan Clair
#
# Day 18
#
import sys
import string
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

# inputlines = [x.strip() for x in open(args.file).readlines()]

# implement snailfish numbers as a tree, and keep the leaves in
# a doubly linked list from left to right.
class Leaf:
    def __init__(self,val):
        self.val = int(val)
        self.left_nbr = None
        self.right_nbr = None
        self.leftmost = self
        self.rightmost = self

    def __str__(self):
        return str(self.val)

class Pair:
    def __init__(self,left=None,right=None):
        self.left = left
        self.right = right

        # each Pair tracks it's leftmost and rightmost leaf
        self.leftmost = left.leftmost
        self.rightmost = right.rightmost
        assert(self.leftmost.left_nbr == None)
        assert(self.rightmost.right_nbr == None)

        # link the leaf list
        assert(left.rightmost.right_nbr == None)
        assert(right.leftmost.left_nbr == None)

        left.rightmost.right_nbr = right.leftmost
        right.leftmost.left_nbr = left.rightmost

    

    def __str__(self):
        return '['+str(self.left)+','+str(self.right)+']'

    def leaves(self):
        """Return a list of leaf values, in order left to right"""
        leaflist = []

        l = self.leftmost
        while l:
            leaflist.append(l.val)
            l = l.right_nbr

        return leaflist

def _parse(snail):
    """Return a Pair containing the value of snail, which is list of chars"""
    # this is destructive to snail, as it removes parsed chars
    c = snail.pop(0)
    
    if c in string.digits:
        v = int(c)
        return Leaf(v)

    assert(c == '[')
    left = _parse(snail)
    c = snail.pop(0)
    assert(c == ',')
    right = _parse(snail)
    c = snail.pop(0)
    assert(c == ']')

    return Pair(left,right)

def parse(snail):
    """Return a Pair containing the value of snail, which is a string"""
    s = list(snail)
    p = _parse(s)
    assert(len(s) == 0)

    return p

p = parse('[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]')

print p
print p.leaves()

