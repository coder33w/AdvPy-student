import base64
import sys
import zlib

class Stack :
    def __init__ (self) :
        self.stack = []

    def push (self, item) :
        self.stack.append(item)

    def peek (self, depth=0) :
        return self.stack[-1 - depth]

    def size (self) :
        return len(self.stack)

    def pop (self, n=1) :
        result = self.stack[-1]
        self.stack = self.stack[:0-n]
        return result

    def swap (self, n) :
        tmp = self.stack[-1]
        self.stack[-1] = self.stack[-1 - n]
        self.stack[-1 - n] = tmp

class Machine :
    def __init__ (self) :
        self.stack = Stack()

    def execute (self, ins) :
        ins = ord(ins) & 0xff
        opcode = ins >> 5
        immediate = ins & 0x1f

        # push immediate
        if opcode == 0 :
            self.stack.push(immediate)
        # dup
        elif opcode == 1 :
            self.stack.push(self.stack.peek(immediate))
        # add
        elif opcode == 2 :
            lhs = self.stack.peek(0)
            rhs = self.stack.peek(1)
            self.stack.pop(2)
            self.stack.push(lhs + rhs)
        # sub
        elif opcode == 3 :
            lhs = self.stack.peek(0)
            rhs = self.stack.peek(1)
            self.stack.pop(2)
            self.stack.push(lhs - rhs)
        # xor
        elif opcode == 4 :
            lhs = self.stack.peek(0)
            rhs = self.stack.peek(1)
            self.stack.pop(2)
            self.stack.push(lhs ^ rhs)
        # input byte
        elif opcode == 5 :
            b = base64.b16decode(sys.stdin.read(2).upper())
            self.stack.push(ord(b))
        # output byte
        elif opcode == 6 :
            sys.stdout.write(chr(self.stack.pop()))
        # swap
        elif opcode == 7 :
            self.stack.swap(immediate)

machine = Machine()

code = zlib.decompress(base64.b64decode("eJyVVFt2gyAQVesjiWkTNSYmmvDZbbA0ltKlsLQKDDDg0JPqxwDOvXPnIYzxmUvGOOM92AnsuNoc1kewHdgh8r0hX+uzi2wD9op8byi2PTuDLcF+IZ4Y1xLf6uhbifLB+zri2kV+WGcV+VjMI5Fr57BPOMkQ2zVSskTed8SmKlPovdLbIf4LYj5xeVC7S6TDRmhQJMZzF2+P6l8ojh94jJZveLSPeUcuZCfkSZhwQqJvZbiFg318ynhhjzIVk4jSrA6z9vlcV3lEkHvGk1q2OIICEIyWlanyC1NlIbM0s9M/+LMkt05I2LnTiyyk6sLtS20rujJEBEAD4EBGUFMZ1YEd36rMtH6YhHwJ2Tv3h0c6mUEn23Sd66DOCrU44IA5SpLZZEZyv4xSmIvGgVDmNTFzJN/T9R80jR7U+6Wm2kz2OZ195SZWqfUVnTyHbuD1H5wfqIZ41oI+HTeZD3+rbHTPfRXvoSKFrtzJk+bqg16bnGsHWjzjeaOuSamLOYug1+bNI+bgDuhSzCrkqB1VjBs1isGmDStCztFsbkSYyQ4B0A+qr56vN9nu7n5iGwBDCneYr0rlPBuvxQ/5g5oe23HqfzQ1Pshf5xwSKw=="))
for c in code :
    machine.execute(c)
