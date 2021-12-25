#
# Advent of Code 2021
# Bryan Clair
#
# Day 24
#
import itertools
import functools

#
# implement MONAD directly
#
code = {
    'div':  [  1,  1,  1,  1, 26,  1,  1, 26, 26, 26,  1, 26, 26, 26],
    'val1': [ 14, 15, 12, 11, -5, 14, 15,-13,-16, -8, 15, -8,  0, -4],
    'val2': [ 12,  7,  1,  2,  4, 15, 11,  5,  3,  9,  2,  3,  3, 11]
}

locked = [x == 1 for x in code['div']]

def roll(z, input, step):
    """Perform one roll of the model number, for the given step"""
    x = z % 26

    div = code['div'][step]
    
    if (input == (z % 26) + code['val1'][step]):
        return z/div
    else:
        return (z/div)*26 + input + code['val2'][step]

def goodinput(z, step):
    """Return a good input for given z and coming step"""
    return (z % 26) + code['val1'][step]

def testkey(key):
    z = 0
    k = 0  # index into key
    fullkey = []
    for i in range(len(locked)):
        if locked[i]:
            # print 'step',i,'(lock) z = ',z
            z = roll(z,key[k],i)
            fullkey.append(key[k])
            k += 1
        else:
            # print 'step',i,'(open) z = ',z
            good = goodinput(z,i)
            # print '   good:',good
            if 0 < good and good < 10:
                z = roll(z,good,i)
                fullkey.append(good)
            else:
                return False
    assert(z == 0)
    return fullkey

minvalid = 99999999999999
topvalid = 0
for key in itertools.product(range(1,10),repeat=7):
    fullkey = testkey(key)
    if fullkey:
        val = functools.reduce(lambda x,y: 10*x + y,fullkey)
        if val > topvalid:
            topvalid = val
        if val < minvalid:
            minvalid = val

print 'part 1:',topvalid
print 'part 1:',minvalid


