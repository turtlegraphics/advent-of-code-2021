#
# Advent of Code 2021
# Bryan Clair
#
# Day 23
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

apods = {None:'.',
         0:'A',
         1:'B',
         2:'C',
         3:'D'}

movecost = {0:1,
            1:10,
            2:100,
            3:1000}

class Board:
    def __init__(self,rooms):
        """size is the size of each room."""
        self.hall = [None]*11
        self.size = len(rooms[0])
        self.rooms = []
        for i in range(4):
            self.rooms.append(list(rooms[i]))

    def __str__(self):
        out = ''
        for i in range(11):
            out += apods[self.hall[i]]
        out += '\n'
        for r in range(self.size):
            out += '  '
            for c in range(4):
                out += apods[self.rooms[c][r]]
                out += ' '
            out += '\n'
        return out

    def front(self,room):
        """Return the index of the front apod in given room,
        or None if the room is empty."""
        i = 0
        while self.rooms[room][i] is None:
            i += 1
            if i == self.size:
                return None
        return i

    def is_parked(self,room):
        """Check if a room is 'parked', so nobody there but the right apods."""
 #       print room, self.rooms[room]
        for i in range(self.size):
            who = self.rooms[room][i]
            if who is None:
                continue
            if who == room:
                continue
            return False
        return True
    
    def hall_clear(self,p1,p2):
        """Check if there are obstructions moving from p1 to p2.
        Return True if the hall is clear."""
        if self.hall[p2] is not None:
            # something is at the destination already
            return False
        i = min(p1,p2)+1
        while i < max(p1,p2):
            if self.hall[i] is not None:
                return False
            i += 1

        return True
    
    def hall_moves(self):
        """Return a list of possible moves for apods in the hall."""
        moves = []
        for i in range(11):
            who = self.hall[i]
            if who is None:
                continue
            c = self.size-1
            while self.rooms[who][c] == who:
                c -= 1
            if self.rooms[who][c] is None:
                # check intermediate hall spaces
                target = 2*(who+1)
                if self.hall_clear(i,target):
                    moves.append( (('h',i),(who,c)) )
        return moves

    def room_moves(self,room,debug=False):
        """Return a list of legal moves starting with an apod in this room."""
        moves = []
        if self.is_parked(room):
            if debug:
                print 'parked!'
            return moves
        
        i = self.front(room)
        if debug:
            print 'front:',i
        if i is None:
            return moves
        
        for to in [0,1,3,5,7,9,10]:
            if debug:
                print 'trying to move to',to
            if self.hall_clear(2*(room+1),to):
                moves.append( ((room,i),('h',to)) )
        return moves

    def all_moves(self):
        """Return a list of all legal moves."""
        moves = self.hall_moves()
        for i in range(4):
            moves += self.room_moves(i)
        return moves
    
    def __getitem__(self,x):
        loc,i = x
        if loc == 'h':
            return self.hall[i]
        else:
            return self.rooms[loc][i]

    def __setitem__(self,x,val):
        loc,i = x
        if loc == 'h':
            assert(val is None or self.hall[i] is None)
            self.hall[i] = val
        else:
            assert(val is None or self.rooms[loc][i] is None)
            self.rooms[loc][i] = val

    def dist(self,fr,to):
        frr,frx = fr
        tor,tox = to
        if frr == 'h':
            x = 2*(tor + 1)
            return abs(frx - x) + tox + 1
        assert(tor == 'h')
        x = 2*(frr + 1)
        return abs(tox - x) + frx + 1
        
    def move(self,fr,to):
        """Move an apod from fr to to.  Return cost."""
        who = self[fr]
#        print 'moving',apods[who],'from',fr,'to',to
        self[fr] = None
        self[to] = who
        return self.dist(fr,to)*movecost[who]
    
def solve(b,depth=0,cost=0):
    global mincost
    if cost >= mincost:
        return
    
    complete = 0
    for i in range(4):
        if b.is_parked(i):
            if b.front(i) == 0:
                complete += 1
        
    if complete == 4:
        print 'solved, cost =',cost
        assert(cost < mincost)
        mincost = cost

    moves = b.all_moves()

    for m in moves:
        fr,to = m
        mcost = b.move(fr,to)
        solve(b,depth+1,cost+mcost)
        b.move(to,fr)

start_0 = ['A','B','D','C']
start_1 = ['BC','BC','DA','DA']
start_t1 =['AA','CB','DB','DC']
start_2 = ['BDDC','BCBC','DBAA','DACA']

def parse(state):
    start = []
    for r in state:
        p = [ord(c)-ord('A') for c in list(r)]
        start.append(p)
    return start

mincost = 1000*100000000

b = Board(parse(start_2))

solve(b)

print 'best:',mincost

