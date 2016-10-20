'''
    This script assembles the bytecode for the eubanks-2 challenge.

    THIS SHOULD NOT BE DISTRIBUTED TO STUDENTS
'''


import base64
import sys
import zlib

OP_PUSH = 0
OP_DUP = 1
OP_ADD = 2
OP_SUB = 3
OP_XOR = 4
OP_INPUT = 5
OP_OUTPUT = 6
OP_SWAP = 7

class Ins :
    def __init__ (self, opcode, immediate) :
        self.opcode = opcode
        self.immediate = immediate

    def assemble (self) :
        return chr((self.opcode << 5) | (self.immediate & 0x1f))

def Push (immediate) :
    return Ins(OP_PUSH, immediate)

def Dup (immediate) :
    return Ins(OP_DUP, immediate)

def Add () :
    return Ins(OP_ADD, 0)

def Sub () :
    return Ins(OP_SUB, 0)

def Xor () :
    return Ins(OP_XOR, 0)

def Input () :
    return Ins(OP_INPUT, 0)

def Output () :
    return Ins(OP_OUTPUT, 0)

def Swap (immediate) :
    return Ins(OP_IMMEDIATE, 0)

def disassemble (ins) :
    opcode = ord(ins) >> 5
    immediate = ord(ins) & 0x1f

    if opcode == OP_PUSH :
        return "push %d" % (immediate)
    elif opcode == OP_DUP :
        return "dup %d" % (immediate)
    elif opcode == OP_ADD :
        return "add"
    elif opcode == OP_SUB :
        return "sub"
    elif opcode == OP_XOR :
        return "xor"
    elif opcode == OP_INPUT :
        return "input"
    elif opcode == OP_OUTPUT :
        return "output"
    elif opcode == OP_SWAP :
        return "swap %d" % (immediate)

def make_value (target) :
    instructions = []

    if target >= 0x1f * 2 :
        multiplier = target / 0x1f
        instructions.append(Push(0x1f))
        for i in range(multiplier - 1) :
            instructions.append(Push(0x1f))
            instructions.append(Add())
        target -= 0x1f * multiplier
        instructions.append(Push(target))
        instructions.append(Add())
    elif target > 0x1f :
        instructions.append(Push(0x1f))
        instructions.append(Push(target - 0x1f))
        instructions.append(Add())
    else :
        instructions.append(Push(target))

    return instructions

def output_string (string) :
    instructions = []
    for c in string :
        instructions += make_value(ord(c))
        instructions.append(Output())
    return instructions

def xor_input (xor_byte) :
    instructions = make_value(xor_byte)
    instructions.append(Input())
    instructions.append(Xor())
    return instructions

# output_string must be 8 characters long, and the 8 xor bytes should be
# on the top of the stack
def xor_output (output_string, xor_bytes) :
    instructions = []
    for i in range(8) :
        instructions.append(Dup(7))
    for i in range(8) :
        instructions += make_value(ord(output_string[i]) ^ xor_bytes[i])
        instructions.append(Xor())
        instructions.append(Output())
    return instructions

def xor_output_long (output_string, xor_bytes) :
    instructions = []
    for i in range(len(output_string) / 8) :
        instructions += xor_output(output_string[i*8:i*8+8], xor_bytes)
    if len(output_string) % 8 > 0 :
        start = 0 - (len(output_string) % 8)
        padding = ' ' * (8 - (len(output_string) % 8))
        instructions += xor_output(output_string[start:] + padding, xor_bytes)
    return instructions

instructions = output_string("Your input needs to make the characters between ")
instructions += output_string("[] say [We1!D0n3].\n")
instructions += output_string("Ready? Go!\n")

# read in the XOR bytes in reverse order
for i in range(8) :
    instructions.append(Input())

instructions += make_value(ord('['))
instructions += [Output()]

xor_bytes = [0x98, 0x74, 0x3e, 0x73, 0xfa, 0xed, 0x46, 0xc9]

instructions += xor_output('We1!D0n3', xor_bytes)

instructions += make_value(ord(']'))
instructions += [Output()]
instructions += make_value(ord('\n'))
instructions += [Output()]

s = "Your flag is St@CkVM15b3S7vM\n"
s += "Email all of your solutions to the eubanks challenges to CPT Eubanks at alexander.s.eubanks.mil@mail.mil"
instructions += xor_output_long(s, xor_bytes)

instructions += make_value(ord('\n'))
instructions += [Output()]

result = ''.join(map(lambda x: x.assemble(), instructions))

print base64.b64encode(zlib.compress(result))

#fh = open('code', 'wb')
#fh.write(result)
#fh.close()