
class Node(object):
    def __str__(self):
        return self.print_tree()


class Program(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class Instructions(Node):
    def __init__(self, arg):
        if isinstance(arg, Instruction):
            self.instructions = [arg]
        elif isinstance(arg, Instructions):
            self.instructions = arg.instructions
        elif isinstance(arg, list):
            self.instructions = arg

    def __add__(self, other):
        return Instructions(self.instructions + other.instructions)


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


class Block(Node):
    def __init__(self, val):
        self.val = val


class PtrValues(Node):
    def __init__(self, vals):
        self.vals = vals


class Rvalue(Node):
    def __init__(self, val, is_string=False):
        self.val = val
        self.is_string = is_string

class Str(Node):
    def __init__(self, val):
        self.val = val

class ForExpr(Node):
    def __init__(self, identificator, start, finish):
        self.identificator = identificator
        self.start = start
        self.finish = finish


class Matrix(Node):
    def __init__(self, fun, val1, val2):
        self.fun = fun
        self.val1 = val1
        self.val2 = val2


class Expr(Node):
    def __init__(self, val1, val2, fun):
        self.val1 = val1
        self.val2 = val2
        self.fun = fun


class Rows(Node):
    def __init__(self, arg):
        if isinstance(arg, RowElems):
            self.row_elems = [arg]
        elif isinstance(arg, Rows):
            self.row_elems = arg.row_elems
        elif isinstance(arg, list):
            self.row_elems = arg

    def __add__(self, other):
        return Rows(self.row_elems + other.row_elems)


class RowElems(Node):
    def __init__(self, arg):
        if isinstance(arg, Rvalue):
            self.elems = [arg]
        elif isinstance(arg, RowElems):
            self.elems = arg.elems
        elif isinstance(arg, list):
            self.elems = arg

    def __add__(self, other):
        return RowElems(self.elems + other.elems)


class Error(Node):
    def __init__(self):
        pass
