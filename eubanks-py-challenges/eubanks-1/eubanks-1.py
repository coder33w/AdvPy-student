'''
    python eubanks2.py 6483 48404
'''

import sys

lhs = int(sys.argv[1]) % (2 ** 16)
rhs = int(sys.argv[2]) % (2 ** 16)


def add (lhs, rhs) :
    return (lhs + rhs) & 0xffff

def sub (lhs, rhs) :
    return (lhs - rhs) & 0xffff

def mul (lhs, rhs) :
    return (lhs * rhs) & 0xffff

def xor (lhs, rhs) :
    return (lhs ^ rhs) & 0xffff

functions = [add, sub, mul, xor]

for i in range(8) :
    lhs = functions[lhs % 3](lhs, rhs)

if lhs == 64476 :
    print 'pass'
else :
    print 'fail'