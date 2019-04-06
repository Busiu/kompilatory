
class Node(object):
    def __str__(self):
        return self.print_tree()


class Program(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class Instructions(Node):

    def __init__(self, instruction, instructions):
        self.instruction = instruction
        self.instructions = instructions


class Instruction(Node):
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2


class Assignment(Node):
    def __init__(self, variable, op, rvalue):
        self.variable = variable
        self.op = op
        self.rvalue = rvalue


class Variable(Node):
    def __init__(self, val):
        self.val = val


class MatrixElem(Node):
    def __init__(self, val):
        self.val = val


class Conditional(Node):
    def __init__(self, val):
        self.val = val


class Cond(Node):
    def __init__(self, val):
        self.val = val


class Block(Node):
    def __init__(self, val):
        self.val = val


class PtrValues(Node):
    def __init__(self, vals):
        self.vals = vals


class Rvalue(Node):
    def __init__(self, val):
        self.val = val


class ForExpr(Node):
    def __init__(self, val):
        self.val = val


class Matrix(Node):
    def __init__(self, val, fun, val2):
        self.val = val
        self.val2 = val2
        self.fun = fun


class Rows(Node):
    def __init__(self, val):
        self.val = val


class RowElems(Node):
    def __init__(self, val):
        self.val = val


class LogExpr(Node):
    def __init__(self, val):
        self.val = val


class NumExpr(Node):
    def __init__(self, val1, op, val2):
        self.val1 = val1
        self.op = op
        self.val2 = val2


class Error(Node):
    def __init__(self):
        pass
