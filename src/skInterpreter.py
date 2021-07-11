from skParse import TTypes
from skObject import Types, Object

import numpy as np
from random import choice, randint
from datetime import datetime

class Interpreter:
    def __init__(self, tokens, logobj):
        self.tokens = tokens
        self.pointer = 0
        self.registor = 0
        self.memory_stack = []
        self.log = logobj

        self.for_each_i = 0
        self.for_each_popped = None

    def op_eval(self, op, before, after):
        # For each reset
        if len(before) > 0 and before[-1].value == ']':
            self.for_each_i = 0
            self.for_each_popped = None
        # For logging
        if self.log is not None:
            self.log.write('Pointer: ' + str(self.pointer) + '\n')
            self.log.write('  ' + str(op) + '\n')
            self.log.write('  [ ')
            for obj in self.memory_stack:
                self.log.write(str(obj) + ' ')
            self.log.write(']\n')
            self.log.write('  ' + str(self.registor) + '\n')
        # Stack operators
        if op.value == '_':
            obj = Object(len(self.memory_stack), Types.Number)
            self.memory_stack.append(obj)
        elif op.value == '≡':
            self.memory_stack.append(self.memory_stack[-1].copy())
        elif op.value == ',':
            self.memory_stack.pop()
        elif op.value == '?':
            for obj in self.memory_stack:
                print(end=str(obj.value) + ' ')
            print()
        elif op.value == '⇅':
            self.memory_stack = self.memory_stack[::-1]
        elif op.value == '$':
            self.memory_stack.append(self.memory_stack[-2].copy())
            self.memory_stack.append(self.memory_stack[-2].copy())
        elif op.value == "'":
            tmp = self.memory_stack[-2].copy()
            self.memory_stack[-2] = self.memory_stack[-1].copy()
            self.memory_stack[-1] = tmp
        # Input
        elif op.value == 'ī':
            val = input()
            try:
                # Check if its int
                obj = Object(int(val), Types.Number)
                self.memory_stack.append(obj)
            except:
                try:
                    # Float?
                    obj = Object(float(val), Types.Number)
                    self.memory_stack.append(obj)
                except:
                    try:
                        # Maybe array?
                        obj = Object(np.array(eval(val)), Types.Array)
                        self.memory_stack.append(obj)
                    except:
                        # Oh its a string
                        obj = Object(val, Types.String)
                        self.memory_stack.append(obj)
        # Output
        elif op.value == 'ṭ':
            if self.memory_stack:
                print(self.memory_stack.pop().value)
        elif op.value == 'ō':
            print(after[1].value)
            self.pointer += 2
        # Constants
        elif op.type == TTypes.NUMBER:
            obj = Object(op.value, Types.Number)
            self.memory_stack.append(obj)
        elif op.value == 'p':
            obj = Object(after[1].value, Types.String)
            self.memory_stack.append(obj)
            self.pointer += 2
        elif op.value == '\\':
            obj = Object(after[1].value, Types.String)
            self.memory_stack.append(obj)
            self.pointer += 1
        # Registor push and copy
        elif op.value == '©':
            self.registor = self.memory_stack.pop()
        elif op.value == '®':
            if self.registor:
                self.memory_stack.append(self.registor)
        # Arithmetic Operators
        elif op.value == '+':
            if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                if after[1].type == TTypes.NUMBER:
                    self.memory_stack[-1].value += after[1].value
                    self.pointer += 1
                elif self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value += obj2.value
            elif self.memory_stack[-1].type == Types.String:
                obj2 = self.memory_stack.pop()
                self.memory_stack[-1].value += str(obj2.value)
        elif op.value == '-':
            if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                if after[1].type == TTypes.NUMBER:
                    self.memory_stack[-1].value -= after[1].value
                    self.pointer += 1
                elif self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value -= obj2.value
        elif op.value == '×':
            if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                if after[1].type == TTypes.NUMBER:
                    self.memory_stack[-1].value *= after[1].value
                    self.pointer += 1
                elif self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value *= obj2.value
            elif self.memory_stack[-1].type == Types.String:
                obj2 = self.memory_stack.pop()
                self.memory_stack[-1].value *= obj2.value
        elif op.value == '÷':
            if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                if after[1].type == TTypes.NUMBER:
                    self.memory_stack[-1].value /= after[1].value
                    self.pointer += 1
                elif self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value /= obj2.value
        elif op.value == '%':
            if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                if after[1].type == TTypes.NUMBER:
                    self.memory_stack[-1].value = after.memory_stack[-1].value % after[1].value
                    self.pointer += 1
                elif self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = self.memory_stack[-1].value % obj2.value
        elif op.value == '*':
            if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                if after[1].type == TTypes.NUMBER:
                    self.memory_stack[-1].value = after.memory_stack[-1].value ** after[1].value
                    self.pointer += 1
                elif self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = self.memory_stack[-1].value ** obj2.value
        # Bitwise operators
        elif op.value == '»':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TTypes.NUMBER:
                    self.memory_stack[-1].value = self.memory_stack[-1].value >> after[1].value
                    self.pointer += 1
                elif self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = self.memory_stack[-1].value >> obj2.value
        elif op.value == '«':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TTypes.NUMBER:
                    self.memory_stack[-1].value = self.memory_stack[-1].value << after[1].value
                    self.pointer += 1
                elif self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = self.memory_stack[-1].value << obj2.value
        elif op.value == '&':
            if self.memory_stack[-1].type == Types.Number:
                if self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = self.memory_stack[-1].value & obj2.value
        elif op.value == '|':
            if self.memory_stack[-1].type == Types.Number:
                if self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = self.memory_stack[-1].value | obj2.value
        elif op.value == '^':
            if self.memory_stack[-1].type == Types.Number:
                if self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = self.memory_stack[-1].value ^ obj2.value
        elif op.value == '!':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = ~self.memory_stack[-1].value
        # Logical operators
        elif op.value == '∧':
            if self.memory_stack[-1].type == Types.Number:
                if self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = 1 if self.memory_stack[-1].value and obj2.value else 0
        elif op.value == '∨':
            if self.memory_stack[-1].type == Types.Number:
                if self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = 1 if self.memory_stack[-1].value or obj2.value else 0
        elif op.value == '¬':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = 1 if not self.memory_stack[-1].value else 0
        # Powers
        elif op.value == '²':
            if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                self.memory_stack[-1].value = self.memory_stack[-1].value ** 2
        elif op.value == '³':
            if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                self.memory_stack[-1].value = self.memory_stack[-1].value ** 3
        elif op.value == '√':
            if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                self.memory_stack[-1].value = self.memory_stack[-1].value ** (1 / 2)
        elif op.value == '∛':
            if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                self.memory_stack[-1].value = self.memory_stack[-1].value ** (1 / 3)
        # Fractions
        elif op.value == '½':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value *= 1 / 2
            elif self.memory_stack[-1].type == Types.Array:
                popped = self.memory_stack.pop()
                arrlis = np.array_split(popped.value, 2)
                for arr in arrlis:
                    self.memory_stack.append(Object(arr, Types.Array))
            elif self.memory_stack[-1].type == Types.String:
                popped = self.memory_stack.pop()
                half = int(len(popped.value) / 2)
                parts = [popped.value[:half], popped.value[half:]]
                for p in parts:
                    self.memory_stack.append(Object(p, Types.String))
        elif op.value == '¼':
            if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                self.memory_stack[-1].value *= 1 / 4
        elif op.value == '¾':
            if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                self.memory_stack[-1].value *= 3 / 4
        # Math
        elif op.value == 'm':
            if after[1].value == '!':
                if self.memory_stack[-1].type == Types.Number:
                    self.memory_stack[-1].value = np.math.factorial(int(self.memory_stack[-1].value))
            elif after[1].value == 's':
                if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                    self.memory_stack[-1].value = np.sin(self.memory_stack[-1].value)
            elif after[1].value == 'S':
                if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                    self.memory_stack[-1].value = np.asin(self.memory_stack[-1].value)
            elif after[1].value == 'c':
                if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                    self.memory_stack[-1].value = np.cos(self.memory_stack[-1].value)
            elif after[1].value == 'C':
                if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                    self.memory_stack[-1].value = np.acos(self.memory_stack[-1].value)
            elif after[1].value == 't':
                if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                    self.memory_stack[-1].value = np.tan(self.memory_stack[-1].value)
            elif after[1].value == 'T':
                if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                    self.memory_stack[-1].value = np.atan(self.memory_stack[-1].value)
            elif after[1].value == 'l':
                if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                    self.memory_stack[-1].value = np.log10(self.memory_stack[-1].value)
            elif after[1].value == 'L':
                if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                    self.memory_stack[-1].value = np.log(self.memory_stack[-1])
            self.pointer += 1
        # Constants
        elif op.value == 'k':
            if after[1].value == '1':
                obj = Object(10 ** 3, Types.Number)
                self.memory_stack.append(obj)
            elif after[1].value == '2':
                obj = Object(10 ** 4, Types.Number)
                self.memory_stack.append(obj)
            elif after[1].value == '3':
                obj = Object(10 ** 5, Types.Number)
                self.memory_stack.append(obj)
            elif after[1].value == 'A':
                obj = Object("ABCDEFGHIJKLMNOPQRSTUVWXYZ", Types.String)
                self.memory_stack.append(obj)
            elif after[1].value == 'a':
                obj = Object("abcdefghijklmnopqrstuvwxyz", Types.String)
                self.memory_stack.append(obj)
            elif after[1].value == 'e':
                obj = Object(np.e, Types.Number)
                self.memory_stack.append(obj)
            elif after[1].value == 'H':
                obj = Object("Hello, World!", Types.String)
                self.memory_stack.append(obj)
            elif after[1].value == 'p':
                obj = Object(np.pi, Types.Number)
                self.memory_stack.append(obj)
            elif after[1].value == 's':
                obj = Object(datetime.now().second, Types.Number)
                self.memory_stack.append(obj)
            elif after[1].value == 'M':
                obj = Object(datetime.now().minute, Types.Number)
                self.memory_stack.append(obj)
            elif after[1].value == 'm':
                obj = Object(datetime.now().microsecond, Types.Number)
                self.memory_stack.append(obj)
            elif after[1].value == 'w':
                obj = Object('www', Types.String)
                self.memory_stack.append(obj)
            self.pointer += 1
        # Length
        elif op.value == 'l':
            if self.memory_stack[-1].type == Types.Array or self.memory_stack[-1].value == Types.String:
                obj = Object(len(self.memory_stack[-1].value), Types.Number)
                self.memory_stack.append(obj)
        # Range
        elif op.value == 'r':
            if self.memory_stack[-1].type == Types.Number:
                obj = self.memory_stack.pop()
                obj = Object(np.arange(obj.value), Types.Array)
                self.memory_stack.append(obj)
            elif self.memory_stack[-1].type == Types.Array:
                obj = self.memory_stack.pop()
                if len(obj.value) == 2:
                    pobj = Object(randint(obj.value[0], obj.value[1]), Types.Number)
                    self.memory_stack.append(pobj)
                else:
                    pobj = Object(choice(obj.value), Types.Number)
                    self.memory_stack.append(pobj)
        elif op.value == 'R':
            if self.memory_stack[-1].type == Types.Number:
                obj = self.memory_stack.pop()
                obj = Object(np.arange(1, obj.value + 1), Types.Array)
                self.memory_stack.append(obj)
            elif self.memory_stack[1].type == Types.Array:
                    self.memory_stack[-1].value = np.rot90(self.memory_stack[-1].value)
        # Pair
        elif op.value == '"':
            obj1, obj2 = self.memory_stack.pop(), self.memory_stack.pop()
            obj = Object(np.array([obj1.value, obj2.value], dtype=object), Types.Array)
            self.memory_stack.append(obj)
        # Negate
        elif op.value == '±':
            if self.memory_stack[-1].type == Types.Number or self.memory_stack[-1].type == Types.Array:
                self.memory_stack[-1].value *= -1
        # Floor and ceil
        elif op.value == '⊥':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = int(self.memory_stack[-1].value)
        elif op.value == '⊤':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = int(self.memory_stack[-1].value) + 1
        # Array operators
        elif op.value == 'S':
            if self.memory_stack[-1].type == Types.Array:
                self.memory_stack[-1].value = np.sort(self.memory_stack[-1].value)
        elif op.value == 'T':
            if self.memory_stack[-1].type == Types.Array:
                self.memory_stack[-1].value = self.memory_stack[-1].value.T
        elif op.value == 'F':
            if self.memory_stack[-1].type == Types.Array:
                self.memory_stack[-1].value = self.memory_stack[-1].value.flatten()
        elif op.value == '∑':
            if self.memory_stack[-1].type == Types.Array:
                self.memory_stack[-1].value = np.sum(self.memory_stack[-1].value)
                self.memory_stack[-1].type = Types.Number
        # ABS
        elif op.value == '⊢':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = abs(self.memory_stack[-1].value)
        # number -> string and vice versa
        elif op.value == 's':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1] = Object(chr(self.memory_stack[-1].value), Types.String)
        elif op.value == 'S':
            if self.memory_stack[-1].type == Types.String:
                if len(self.memory_stack[-1].value) == 1:
                    self.memory_stack[-1] = Object(ord(self.memory_stack[-1].value), Types.Number)
                else:
                    self.memory_stack[-1] = Object([ord(c) for c in self.memory_stack[-1].value], Types.Array)
        elif op.value == 'B':
            if self.memory_stack[-1].type == Types.Number:
                val = np.array([i for i in map(int, bin(self.memory_stack[-1].value)[2:])])
                self.memory_stack[-1] = Object(val, Types.Array)
        # (Un)Wrapping
        elif op.value == 'W':
            stack = self.memory_stack[:]
            i = 0
            while i < len(stack):
                stack[i] = stack[i].value
                i += 1
            self.memory_stack = []
            self.memory_stack.append(Object(np.array(stack, dtype=object), Types.Array))
        elif op.value == 'U':
            if self.memory_stack[-1].type == Types.Array:
                popped = self.memory_stack.pop()
                for v in popped.value:
                    self.memory_stack.append(Object(v, Types.Number))
        # Belongs to
        elif op.value == 'c':
            if self.memory_stack[-1].type == Types.Array:
                if self.memory_stack[-2].type == Types.Number:
                    obj = Object(1 if self.memory_stack[-2].value in self.memory_stack[-1].value else 0, Types.Number)
                    self.memory_stack.append(obj)
        # Comparision operators
        elif op.value == '=':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TTypes.NUMBER:
                    self.memory_stack[-1].value = 1 if self.memory_stack[-1].value == after[1].value else 0
                    self.pointer += 1
                elif self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = 1 if self.memory_stack[-1].value == obj2.value else 0
            elif self.memory_stack[-1].type == Types.Array:
                if self.memory_stack[-2].type == Types.Array:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1] = Object(1 if np.array_equal(self.memory_stack[-1].value, obj2.value) else 0, Types.Number)
            elif self.memory_stack[-1].type == Types.String:
                if self.memory_stack[-2].type == Types.String:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1] = Object(1 if self.memory_stack[-1].value == obj2.value else 0, Types.Number)
        elif op.value == '≠':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TTypes.NUMBER:
                    self.memory_stack[-1].value = 1 if self.memory_stack[-1].value != after[1].value else 0
                    self.pointer += 1
                elif self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = 1 if self.memory_stack[-1].value != obj2.value else 0
            elif self.memory_stack[-1].type == Types.Array:
                if self.memory_stack[-2].type == Types.Array:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1] = Object(0 if np.array_equal(self.memory_stack[-1].value, obj2.value) else 1, Types.Number)
            elif self.memory_stack[-1].type == Types.String:
                if self.memory_stack[-2].type == Types.String:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1] = Object(1 if self.memory_stack[-1].value != obj2.value else 0, Types.Number)
        elif op.value == '>':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TTypes.NUMBER:
                    self.memory_stack[-1].value = 1 if self.memory_stack[-1].value > after[1].value else 0
                    self.pointer += 1
                elif self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = 1 if self.memory_stack[-1].value > obj2.value else 0
        elif op.value == '<':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TTypes.NUMBER:
                    self.memory_stack[-1].value = 1 if self.memory_stack[-1].value < after[1].value else 0
                    self.pointer += 1
                elif self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = 1 if self.memory_stack[-1].value < obj2.value else 0
        elif op.value == '≤':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TTypes.NUMBER:
                    self.memory_stack[-1].value = 1 if self.memory_stack[-1].value <= after[1].value else 0
                    self.pointer += 1
                elif self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = 1 if self.memory_stack[-1].value <= obj2.value else 0
        elif op.value == '≥':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TTypes.NUMBER:
                    self.memory_stack[-1].value = 1 if self.memory_stack[-1].value >= after[1].value else 0
                    self.pointer += 1
                elif self.memory_stack[-2].type == Types.Number:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = 1 if self.memory_stack[-1].value >= obj2.value else 0
        # If statements
        elif op.value == '{':
            popped = self.memory_stack.pop()
            if popped.value:
                # Do nothing
                pass
            else:
                if op.misc["else"] != None:
                    self.pointer = op.misc["else"]
                else:
                    self.pointer = op.misc["end"]
        elif op.value == ':':
            # Jump to '}'
            self.pointer = op.misc["end"]
        elif op.value == '⁇':
            if self.memory_stack[-1].value:
                pass
            else:
                self.pointer += 1
        # While loop
        elif op.value == '(':
            if self.memory_stack[-1].value:
                pass
            else:
                self.pointer = op.misc["end"]
        elif op.value == ')':
            self.pointer = op.misc["start"] - 1
        # For each
        elif op.value == '[':
            if self.for_each_popped is None:
                self.for_each_popped = self.memory_stack.pop()
                if self.for_each_popped.type == Types.Number:
                    self.for_each_popped = Object(range(self.for_each_popped.value, 0, -1), Types.Array)
                self.memory_stack.append(Object(self.for_each_popped.value[self.for_each_i], Types.Number))
                self.for_each_i += 1
            else:
                if self.for_each_i < len(self.for_each_popped.value):
                    self.memory_stack.append(Object(self.for_each_popped.value[self.for_each_i], Types.Number))
                    self.for_each_i += 1
                else:
                    self.pointer = op.misc["end"]
        elif op.value == ']':
            self.pointer = op.misc["start"] - 1

    def run(self):
        # Main loop
        while self.pointer < len(self.tokens):
            before = self.tokens[:self.pointer]
            token = self.tokens[self.pointer]
            after = self.tokens[self.pointer:]

            self.op_eval(token, before, after)

            self.pointer += 1
