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

inputlines = [x.strip() for x in open(args.file).readlines()]

class Explosion(Exception):
    pass

# implement snailfish numbers as a tree, and keep the leaves in
# a doubly linked list from left to right.
class Leaf:
    def __init__(self,val):
        self.val = int(val)

    def magnitude(self):
        return self.val

    def _fancystr(self,depth):
        return str(self)

    def __str__(self):
        return str(self.val)

class Pair:
    def __init__(self,left=None,right=None):
        self.left = left
        self.right = right

        if isinstance(left,Leaf):
            self.leaves = [left]
        else:
            left.parent = self
            self.leaves = left.leaves

        if isinstance(right,Leaf):
            self.leaves.append(right)
        else:
            right.parent = self
            self.leaves = self.leaves + right.leaves

    def magnitude(self):
        return 3*self.left.magnitude() + 2*self.right.magnitude()

    def clean(self):
        split = True
        while split:
            # print self
            exploded = True
            while exploded:
                exploded = False
                try:
                    self._goexplode(self,0)
                except Explosion:
                    exploded = True
                    # print self
            split = self._gosplit(self)

    def _splitleaf(self,leaf):
        # print 'splitting',leaf.val
        i = self.leaves.index(leaf)
        self.leaves.pop(i)
        l = Leaf(leaf.val/2)
        r = Leaf(leaf.val-l.val)
        self.leaves.insert(i,r)
        self.leaves.insert(i,l)
        return Pair(l,r)

    def _gosplit(self, root):
        if isinstance(self.left,Leaf):
            if self.left.val > 9:
                self.left = root._splitleaf(self.left)
                self.left.parent = self
                return True
        else:
            if self.left._gosplit(root):
                return True

        if isinstance(self.right,Leaf):
            if self.right.val > 9:
                self.right = root._splitleaf(self.right)
                self.right.parent = self
                return True
        else:    
            if self.right._gosplit(root):
                return True

        return False

    def _goexplode(self, root, depth):
        explode = (depth >= 4)

        if not isinstance(self.left,Leaf):
            self.left._goexplode(root,depth+1)
            explode = False

        if not isinstance(self.right,Leaf):
            self.right._goexplode(root,depth+1)
            explode = False

        if explode:
            # print 'exploding',self
            self._explode(root)
            raise Explosion()
        
    def _explode(self,root):
        l = root.leaves.index(self.left)
        r = root.leaves.index(self.right)
        if l > 0:
            root.leaves[l-1].val += self.left.val
        if r < len(root.leaves)-1:
            root.leaves[r+1].val += self.right.val

        corpse = Leaf(0)
        if self == self.parent.left:
            self.parent.left = corpse
        else:
            self.parent.right = corpse
        root.leaves.pop(r)
        root.leaves[l] = corpse

    def _fancystr(self,depth):
        if depth < 4:
            return '['+self.left._fancystr(depth+1)+','+ self.right._fancystr(depth+1)+']'
        else:
            return '{'+self.left._fancystr(depth+1)+','+ self.right._fancystr(depth+1)+'}'

    def __str__(self):
        return self._fancystr(0)

def _parse(snail):
    """Return a Pair containing the value of snail, which is list of chars"""
    # this is destructive to snail, as it removes parsed chars
    c = snail.pop(0)
    
    if c in string.digits:
        while snail[0] in string.digits:
            c += snail.pop(0)
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


accum = None
for line in inputlines:
    p = parse(line)
    if accum == None:
        accum = p
    else:
        accum = Pair(accum,p)

    accum.clean()

print 'part 1:',accum.magnitude()

topmag = 0
for x in range(len(inputlines)):
    if x % 10 == 0:
        print str(100-x)+'%'+' remaining'
    for y in range(len(inputlines)):
        if x != y:
            vx = parse(inputlines[x])
            vy = parse(inputlines[y])
            sum = Pair(vx,vy)
            sum.clean()
            mag = sum.magnitude()
            if mag > topmag:
                topmag = mag

print 'part 2:',topmag
