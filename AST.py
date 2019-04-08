
class Node(object):
    def __str__(self):
        return self.print_tree()


class Program(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class Instructions(Node):
    #TODO zamienic na liste
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
    def __init__(self, identificator, val1, val2):
        self.identificator = identificator
        self.val1 = val1
        self.val2 = val2


class Conditional(Node):
    def __init__(self, condSt, conditional, block1, elseSt, block2):
        self.condSt = condSt
        self.conditional = conditional
        self.block1 = block1
        self.elseSt = elseSt
        self.block2 = block2


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
    def __init__(self, identificator, val):
        self.identificator = identificator
        self.val = val


class Matrix(Node):
    def __init__(self, fun, val1, val2):
        self.fun = fun
        self.val1 = val1
        self.val2 = val2


#class Matrix(Node):
#    def __init__(self, val, fun, val2):
#        self.val = val
#        self.val2 = val2
#        self.fun = fun


class Rows(Node):
    def __init__(self, rowelems, rows):
        self.rowelems = rowelems
        self.rows = rows


class RowElems(Node):
    def __init__(self, rvalue, rowelems):
        self.rvalue = rvalue
        self.rowelems = rowelems


class LogExpr(Node):
    def __init__(self, expr1, op, expr2):
        self.expr1 = expr1
        self.op = op
        self.expr2 = expr2


class NumExpr(Node):
    def __init__(self, val1, op, val2):
        self.val1 = val1
        self.op = op
        self.val2 = val2


class Error(Node):
    def __init__(self):
        pass
