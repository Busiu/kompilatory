import sys

import AST

from Memory import *
from Exceptions import *
from visit import *
from matrix_operations import *

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.global_memory = MemoryStack()

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
        if node.val1 == "break":
            raise BreakException()
        elif node.val1 == "continue":
            raise ContinueException()
        elif node.val1 == "return":
            raise ReturnValueException(None)

        self.visit(node.val1)
        self.visit(node.val2)

    @when(AST.Assignment)
    def visit(self, node):
        name = str(node.variable)
        value = self.visit(node.rvalue)
        var = self.global_memory.get(name)
        if node.op == "=":
            self.global_memory.set(name, value)
        elif node.op == "+=":
            self.global_memory.set(name, var + value)
        elif node.op == "-=":
            self.global_memory.set(name, var - value)
        elif node.op == "*=":
            self.global_memory.set(name, var * value)
        elif node.op == "/=":
            self.global_memory.set(name, var / value)
        elif node.op == ".+=":
            var.ass_dot_add(value)
            self.global_memory.set(name, var)
        elif node.op == ".-=":
            var.ass_dot_sub(value)
            self.global_memory.set(name, var)
        elif node.op == ".*=":
            var.ass_dot_mul(value)
            self.global_memory.set(name, var)
        elif node.op == "./=":
            var.ass_dot_div(value)
            self.global_memory.set(name, var)

    @when(AST.MatrixElem)
    def visit(self, node):
        name = str(node.identificator)
        val1 = self.visit(node.val1)
        val2 = self.visit(node.val1)
        matrix = self.global_memory.get(name)
        return matrix.get(val1, val2)

    @when(AST.Conditional)
    def visit(self, node):
        if node.cond_st == "if":
            allowed = self.visit(node.conditional)
            if allowed:
                self.global_memory.push(Memory("mem"))
                self.visit(node.block1)
                self.global_memory.pop()
            elif node.else_st is not None:
                self.global_memory.push(Memory("mem"))
                self.visit(node.block2)
                self.global_memory.pop()
        else:
            self.global_memory.push(Memory("mem"))
            while self.visit(node.conditional):
                try:
                    self.visit(node.block1)
                except BreakException:
                    break
                except ContinueException:
                    continue
            self.global_memory.pop()

    @when(AST.Block)
    def visit(self, node):
        self.global_memory.push(Memory("mem"))
        self.visit(node.val)
        self.global_memory.pop()

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
        start_index = self.visit(node.start)
        end_index = self.visit(node.finish)
        if self.global_memory.get(node.identificator) is None:
            self.global_memory.insert(node.identificator, start_index)
            iterator = self.global_memory.get(node.identificator)
        else:
            iterator = self.global_memory.get(node.identificator)
            self.global_memory.set(node.identificator, iterator + 1)
        if iterator >= end_index:
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

        if node.fun == "+":
            return val1 + val2
        elif node.fun == "-":
            return val1 - val2
        elif node.fun == "*":
            return val1 * val2
        elif node.fun == "/":
            return val1 / val2
        elif node.fun == ".+":
            return dot_add(val1, val2)
        elif node.fun == ".-":
            return dot_sub(val1, val2)
        elif node.fun == ".*":
            return dot_mul(val1, val2)
        elif node.fun == "./":
            return dot_div(val1, val2)
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
        return self.global_memory.get(str(node.name))

    @when(AST.Str)
    def visit(self, node):
        return str(node.val)
