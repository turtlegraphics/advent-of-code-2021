#
# Advent of Code 2020
# Bryan Clair
#
# Utilities
#
from argparse import ArgumentParser
from math import sqrt

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        action = "count",
                        dest = "verbose",
                        default = 1,
                        help = "Set verbosity level (-v, -vv, -vvv,...)")
    parser.add_argument("-q", "--quiet",
                        action = "store_const",
                        const = 0,
                        dest = "verbose",
                        help = "Suppress output.")
    
    parser.add_argument("-p", "--part",
                        action="store",
                        dest = "part",
                        default = 1,
                        type = int,
                        help = "Which part of the problem to solve (1 or 2)")
    
    parser.add_argument("file",
                        nargs = "?",
                        default = "input.txt",
                        help = "Problem input file (optional).")
    args = parser.parse_args()
    if args.verbose > 2:
        print(args)

    return args

# CRT from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python      
def chinese_remainder(n, a):
    """solves the chinese remainder theorem for x == a (mod n)"""
    sum = 0
    prod = reduce(lambda a, b: a*b, n)

    for n_i, a_i in zip(n, a):
        p = prod / n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

def mul_inv(a, b):
    """returns the multiplicative inverse of a (mod b)"""
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a / b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

class Point:
    """
    A 2d point class
    """
    def __init__(self, x=0, y=0):
        """
        Construct from another point, an (x,y) tuple,
        or x and y passed as values.
        """
        if isinstance(x,Point):
            self.x = x.x
            self.y = x.y
        elif isinstance(x,tuple):
            self.x, self.y = x
        else:
            self.x, self.y = x,y

    def __copy__(self):
        return Point(self)

    def __iter__(self):
        yield self.x
        yield self.y

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def dist(self, other):
        """Euclidean distance."""
        return abs(self - other)

    def __eq__(self,other):
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self,other):
        return not self == other

    def __add__(self,other):
        newpt = self.__copy__()
        newpt += other
        return newpt

    def __iadd__(self,other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self,other):
        newpt = self.__copy__()
        newpt -= other
        return newpt

    def __isub__(self,other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __str__(self):
        return '(%s,%s)' % (str(self.x),str(self.y))

class Grid:
    """
    A 2d grid of tile objects (probably characters) that can be any size.
    Coordinates are tuples (x,y) or Points.
    Keeps track of its own dimensions and displays the smallest rectangle that
    contains all data.
    """
    def __init__(self):
        self.raster = {}

    def __setitem__(self,p,tile):
        x,y = p

        if self.raster:
            self.xmin = min(self.xmin,x)
            self.xmax = max(self.xmax,x)
            self.ymin = min(self.ymin,y)
            self.ymax = max(self.ymax,y)
        else:
            self.xmin = x
            self.xmax = x
            self.ymin = y
            self.ymax = y

        self.raster[(x,y)] = tile

    def __getitem__(self,p):
        x,y = p
        return self.raster[(x,y)]

    def __contains__(self,p):
        x,y = p
        return (x,y) in self.raster

    def __iter__(self):
        return iter(self.raster)

    def _neighbors(self, p, dirs, validate):
        """Return a list of neighbors of p in dirs directions.
        * Returns only neighbors present in the grid if validate==True
        * Returns all possible neighbors if validate==False
        """
        n = []
        for d in dirs:
            q = p + Point(d)
            if (not validate) or q in self:
                n.append(q)
        return n

    _dirs = [(1,0),(-1,0),(0,1),(0,-1),
             (1,1),(-1,1),(1,-1),(-1,-1)]

    def neighbors(self, p, diagonal = False, validate = True):
        """
        * Returns only neighbors present in the grid if validate==True
        * Returns all possible neighbors if validate==False

        Uses the four cardinal directions, unless diagonal is True,
        in which case it uses the eight grid neighbors
        """
        x,y = p
        if diagonal:
            return self._neighbors(Point((x,y)),self._dirs,validate)
        return self._neighbors(Point((x,y)),self._dirs[:4],validate)

    def display(self):
        for y in range(self.ymax,self.ymin-1,-1):
            out = ''
            for x in range(self.xmin,self.xmax + 1):
                if (x,y) in self.raster:
                    out += str(self.raster[(x,y)])
                else:
                    out += ' '
            print(out)

class HexGrid(Grid):
    """
    Class representing a hexagonal grid.
    See HexPoint class for details of coordinates
    """
    def neighbors(self, p, validate=True):
        """
        * Returns only neighbors present in the grid if validate==True
        * Returns all possible neighbors if validate==False

        p must be a HexPoint
        """
        return self._neighbors(p,p.DIRECTIONS.values(),validate)

    def display(self):
        for y in range(self.ymax,self.ymin-1,-1):
            out = ' '*(y-self.ymin)
            for x in range(self.xmin,self.xmax + 1):
                if (x,y) in self.raster:
                    out += str(self.raster[(x,y)])
                else:
                    out += ' '
                out += ' '
            print(out)

class HexPoint(Point):
    """
    Class for working with coordinates on a hexagonal grid.
    Coordinates are mappped to (x,y) with connections made in this way:
      NW  NE
     W  *   E
      SW  SE
    """
    DIRECTIONS = {
        'ne' : (0,1),
        'sw' : (0,-1),
        'nw' : (-1,1),
        'se' : (1,-1),
        'w' : (-1,0),
        'e' : (1,0)
        }
        
    def __copy__(self):
        return HexPoint(self)

    def __abs__(self):
        """Returns distance to the origin on the hex grid"""
        x,y = self.x,self.y
        diag = 0
        if (x > 0 and y < 0):
            diag = -min(abs(x),abs(y))
        if (x < 0 and y > 0):
            diag = min(abs(x),abs(y))
        return abs(diag) + abs(x + diag) + abs(y - diag)

    def move(self,dir):
        self += HexPoint(self.DIRECTIONS[dir.lower()])

if __name__ == '__main__':
    # Argument parsing
    print(parse_args())

    # Number Theory
    print '-'*20
    print "Number Theory"
    print '-'*20
    print 'The multiplicative inverse of 5 mod 13 is',mul_inv(5,13)
    print 'Solve x = 4 mod 16 and x = 2 mod 21:',
    print chinese_remainder([16,21],[4,2])

    # Point
    print '-'*20
    print "Point class"
    print '-'*20
    p = Point(1,2)
    q = Point((3,3)) # ok to use tuple
    r = Point(p)
    r += Point(10,10)
    r -= Point(5,1)

    print 'p=%s,q=%s,r=%s' % (str(p),str(q),str(r))
    print 'q and q are',p.dist(q),'apart'
    print 'p + q = ',p+q
    print 'r - q = ',r-q
    assert(r - q == Point(3,8))
    assert(p != q)

    # Grid
    print '-'*20
    print "Grid class"
    print '-'*20
    g = Grid()
    g[Point(-1,0)] = 'o'
    g[Point(1,0)] = 'o'
    dots = [(-1,2),(0,2),(1,2),(-2,1),(-2,0),(-2,-1),
            (2,1),(2,0),(2,-1),(-1,-2),(0,-2),(1,-2)]
    for p in dots:
        g[p] = '.'
    nose = Point(0,-1)
    g[nose] = 'U'
    g.display()

    dotcount = 0
    for p in g:
        if g[p] == '.':
            dotcount += 1
    print 'There are %d dots.' % dotcount
    assert(dotcount == len(dots))

    assert(g[nose] == 'U')
    assert((5,5) not in g)
    assert((2,0) in g)

    nosenbrs = tuple([len(g.neighbors(nose,diag)) for diag in [False,True]])
    print 'nose U has %d cardinal and %d diagonal neighbors.' % nosenbrs
    assert((1,5) == nosenbrs)

    # HexGrid, HexPoint
    print '-'*20
    print "HexGrid, HexPoint"
    print '-'*20
    print 'Distances from origin:'
    h = HexGrid()
    for x in range(-3,4):
        for y in range(-3,4):
            p = HexPoint(x,y)
            h[p] = str(abs(p))

    h.display()

    h = HexGrid()
    for x in range(-5,4):
        for y in range(-2,6):
            h[(x,y)] = '.'

    print
    print 'Take a stroll'
    p = HexPoint()
    q = HexPoint()
    q.move('sw')
    q.move('sw')
    q.move('w')
    h[q] = 'q'

    i = 0
    h[p] = '0'
    for d in ['e','ne','ne','nw','w','w','w','sw','se']:
        print '%s --%s-->' % (str(p),d),
        p.move(d)
        i += 1
        h[p] = str(i)
    print p

    h.display()

    print 'Ended',abs(p),'from start'
    print 'Ended',p.dist(q),'from q'

    assert(p.dist(q) == 3)
    assert(len(h.neighbors(p)) == 6)
    assert(len(h.neighbors(p,validate=False)) == 6)
