
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


class Rvalue(Node):
    def __init__(self, val):
        self.val = val

# ...
# fill out missing classes
# ...


class Error(Node):
    def __init__(self):
        pass
