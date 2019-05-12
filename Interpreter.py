import sys

import AST

from Memory import *
from Exceptions import *
from visit import *

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
        if(node.val1 == "BREAK"):
            raise BreakException()
        elif(node.val1 == "CONTINUE"):
            raise ContinueException()
        self.visit(node.val1)
        self.visit(node.val2)

    @when(AST.Assignment)
    def visit(self, node):
        value = self.visit(node.rvalue)
        var = self.globalMemory.get(node.variable)
        if node.op == "=":
            self.globalMemory.set(node.variable, value)
        elif node.op == "+=":
            self.globalMemory.set(node.variable, var + value)
        elif node.op == "-=":
            self.globalMemory.set(node.variable, var - value)
        elif node.op == "*=":
            self.globalMemory.set(node.variable, var * value)
        elif node.op == "/=":
            self.globalMemory.set(node.variable, var / value)
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
        if node.condSt == "IF":
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
        if self.globalMemory.get(node.identificator) is None:
            self.globalMemory.insert(node.identificator, node.start)
        iterator = self.globalMemory.get(node.identificator)
        if iterator >= node.finish:
            return False
        self.globalMemory.set(node.identificator, iterator + 1)
        return True

    @when(AST.Expr)
    def visit(self, node):
        val1 = self.visit(node.val1)
        val2 = self.visit(node.val2)
        if node.fun == "+":
            return val1 + val2
        elif node.fun == "-":
            return val1 - val2
        elif node.fun == "*":
            return val1 * val2
        elif node.fun == "/":
            return val1 / val2
        else:
            raise Exception("Not implemented yet!")

    @when(AST.Int)
    def visit(self, node):
        return int(node.val)

    @when(AST.Float)
    def visit(self, node):
        return float(node.val)

    @when(AST.Str)
    def visit(self, node):
        return str(node.val)
