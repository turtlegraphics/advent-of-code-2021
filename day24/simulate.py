#
# Advent of Code 2021
# Bryan Clair
#
# Day 24
#
import sys
import re
sys.path.append("..")
import aocutils

args = aocutils.parse_args()

inputlines = [x.strip() for x in open(args.file).readlines()]

class ALU:
    def __init__(self,code):
        self.prog = []
        for line in code:
            name, val = line.split(' ',1)
            if name == 'inp':
                reg = val
                op = None
            else:
                reg, op = val.split()
            self.prog.append((name,reg,op))
        self.registers = {'x':0,'y':0,'z':0,'w':0}
        self.ip = 0

    def printregs(self):
        print 'ip=%4d' % self.ip,
        for reg in ['x','y','z','w']:
            print reg,'=',self.registers[reg],
        print
        
    def disassemble(self,inst):
        name,reg,op = inst
        print name,
        if name == 'inp':
            print reg
        else:
            print reg,op
        
    def list(self):
        for inst in self.prog:
            self.disassemble(inst)

    def step(self):
        """run one step"""
        inst = self.prog[self.ip]
        print self.ip,
        self.disassemble(inst)
        
        name,reg,op = inst
        if name == 'inp':
            self.registers[reg] = self.input.pop(0)
            self.ip += 1
            return

        try:
            b = self.registers[op]
        except KeyError:
            b = int(op)

        a = self.registers[reg]
        if name == 'add':
            v = a+b
        elif name == 'mul':
            v = a*b
        elif name == 'div':
            v = a/b
        elif name == 'mod':
            v = a%b
        elif name == 'eql':
            if a == b:
                v = 1
            else:
                v = 0

        self.registers[reg] = v
        
        self.ip += 1

    def run(self,input):
        """input should be a list of integers"""
        self.input = input

        while self.ip < len(self.prog):
            self.step()

        return self.registers

alu = ALU(inputlines)

model = str(13579246899999)
alu.run([int(x) for x in list(model)])

alu.printregs()
