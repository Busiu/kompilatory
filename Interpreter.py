import sys

import AST

from Memory import *
from Exceptions import *
from visit import *
from matrix_operations import *

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.globalMemory = MemoryStack()

    @on("node")
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        self.visit(node.instructions)

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    @when(AST.Instruction)
    def visit(self, node):
        if(node.val1 == "break"):
            raise BreakException()
        elif(node.val1 == "continue"):
            raise ContinueException()
        elif(node.val1 == "return"):
            raise ReturnValueException(None)

        self.visit(node.val1)
        self.visit(node.val2)

    @when(AST.Assignment)
    def visit(self, node):
        name = str(node.variable)
        value = self.visit(node.rvalue)
        var = self.globalMemory.get(name)
        if node.op == "=":
            self.globalMemory.set(name, value)
        elif node.op == "+=":
            self.globalMemory.set(name, var + value)
        elif node.op == "-=":
            self.globalMemory.set(name, var - value)
        elif node.op == "*=":
            self.globalMemory.set(name, var * value)
        elif node.op == "/=":
            self.globalMemory.set(name, var / value)
        elif node.op == ".+=":
            raise Exception("Not implemented yet!")
        elif node.op == ".-=":
            raise Exception("Not implemented yet!")
        elif node.op == ".*=":
            raise Exception("Not implemented yet!")
        elif node.op == "./=":
            raise Exception("Not implemented yet!")


    @when(AST.Conditional)
    def visit(self, node):
        if node.condSt == "if":
            allowed = self.visit(node.conditional)
            if allowed:
                self.globalMemory.push(Memory("mem"))
                self.visit(node.block1)
                self.globalMemory.pop()
            elif node.elseSt is not None:
                self.globalMemory.push(Memory("mem"))
                self.visit(node.block2)
                self.globalMemory.pop()
        else:
            self.globalMemory.push(Memory("mem"))
            while self.visit(node.conditional):
                self.visit(node.block1)
            self.globalMemory.pop()

    @when(AST.Block)
    def visit(self, node):
        self.globalMemory.push(Memory("mem"))
        self.visit(node.val)
        self.globalMemory.pop()

    @when(AST.PtrValues)
    def visit(self, node):
        for val in node.vals:
            result = self.visit(val)
            print(result)

    @when(AST.Rvalue)
    def visit(self, node):
        value = self.visit(node.val)
        return value

    @when(AST.ForExpr)
    def visit(self, node):
        startValue = self.visit(node.start)
        finishValue = self.visit(node.finish)
        if self.globalMemory.get(node.identificator) is None:
            self.globalMemory.insert(node.identificator, startValue)
            iterator = self.globalMemory.get(node.identificator)
        else:
            iterator = self.globalMemory.get(node.identificator)
            self.globalMemory.set(node.identificator, iterator + 1)
        if iterator >= finishValue:
            return False
        return True

    @when(AST.Rows)
    def visit(self, node):
        matrix = []
        for row in node.row_elems:
            vector = self.visit(row)
            matrix.append(vector)
        return matrix

    @when(AST.RowElems)
    def visit(self, node):
        vector = []
        for row_elem in node.elems:
            elem = self.visit(row_elem)
            vector.append(elem)
        return vector

    @when(AST.Expr)
    def visit(self, node):
        val1 = self.visit(node.val1)
        val2 = self.visit(node.val2)
        #print("val1 is instance of: ", type(val1).__name__)
        #print("val2 is instance of: ", type(val2).__name__)

        print(val1)
        print(val2)
        if node.fun == "+":
            return val1 + val2
        elif node.fun == "-":
            return val1 - val2
        elif node.fun == "*":
            return val1 * val2
        elif node.fun == "/":
            return val1 / val2
        elif node.fun == ">":
            return val1 > val2
        elif node.fun == "<":
            return val1 < val2
        elif node.fun == "<=":
            return val1 <= val2
        elif node.fun == ">=":
            return val1 >= val2
        elif node.fun == "==":
            return val1 == val2
        elif node.fun == "!=":
            return val1 != val2
        elif node.fun == "[":
            return Matrix(val1)
        elif node.fun == "(":
            return val1
        elif node.fun == "zeros":
            return zeros(val1)
        elif node.fun == "ones":
            return ones(val1)
        elif node.fun == "eye":
            return eye(val1)
        else:
            raise Exception("Not implemented yet! expr")

    @when(AST.Int)
    def visit(self, node):
        return int(node.val)

    @when(AST.Float)
    def visit(self, node):
        return float(node.val)

    @when(AST.Id)
    def visit(self, node):
        return self.globalMemory.get(str(node.name))

    @when(AST.Str)
    def visit(self, node):
        return str(node.val)
