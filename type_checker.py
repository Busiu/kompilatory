#!/usr/bin/python
import AST
from collections import defaultdict

types_table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

types = ['int', 'float', 'string', 'matrix']

for op in ['+', '-', '*', '/', '<', '>', '<=', '>=', '==', '!=']:
    types_table[op]['int']['int'] = 'int'

for op in ['+', '-', '*', '/']:
    types_table[op]['int']['float'] = 'float'
    types_table[op]['float']['int'] = 'float'
    types_table[op]['float']['float'] = 'float'
    types_table[op]['matrix']['int'] = 'matrix'
    types_table[op]['matrix']['float'] = 'matrix'
    if op != '/':
        types_table[op]['int']['matrix'] = 'matrix'
        types_table[op]['float']['matrix'] = 'matrix'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    types_table[op]['int']['float'] = 'int'
    types_table[op]['float']['int'] = 'int'
    types_table[op]['float']['float'] = 'int'

for op in ['.+', '.-', '.*', './']:
    types_table[op]['matrix']['matrix'] = 'matrix'

for op in ['+', '-']:
    types_table[op]['matrix']['matrix'] = 'matrix'

for op in ['+=', '-=', '*=', '/=']:
    types_table[op]['int']['float'] = 'float'
    types_table[op]['float']['int'] = 'float'
    types_table[op]['float']['float'] = 'float'
    types_table[op]['int']['int'] = 'int'
    types_table[op]['matrix']['int'] = 'matrix'
    types_table[op]['matrix']['float'] = 'matrix'

for op in ['+=', '-=']:
    types_table[op]['matrix']['matrix'] = 'matrix'

for op in ['zeros', 'eye', 'ones']:
    types_table[op]['int']['int'] = 'matrix'

types_table['==']['string']['string'] = 'int'


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class TypeChecker(NodeVisitor):

    def __init__(self):
        # id : (type, x, y)
        self.variables = {}
        self.errors = []
        self.in_loop = False

    def get_errors(self):
        return self.errors

    def visit_BinExpr(self, node):
        # alternative usage,
        # requires definition of accept method in class Node
        type1 = self.visit(node.left)  # type1 = node.left.accept(self)
        type2 = self.visit(node.right)  # type2 = node.right.accept(self)
        op = node.op
        # ...
        #

    def visit_Program(self, node):
        self.visit(node.instructions)

    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_Instruction(self, node):
        self.visit(node.val1)
        if node.val2 is not None:
            self.visit(node.val2)

    def visit_Assignment(self, node):
        ret = self.visit(node.rvalue)
        if ret is None:
            return None
        (rval_type, r_x, r_y) = ret
        var_id = node.variable.val
        if node.op == '=':
            self.variables[var_id] = (rval_type, r_x, r_y)
        else:
            try:
                (t, x, y) = self.variables[var_id]
                if t == 'matrix' and rval_type == 'matrix':
                    if x != r_x or y != r_y:
                        self.errors.append("Dimensions don't match! Left side = ({0}, {1}). Right side = ({2}, {3}"
                                           .format(x, y, r_x, r_y))
                self.variables[var_id] = (types_table[node.op][t][rval_type], x, y)
            except KeyError as e:
                self.errors.append("Variable {0} not declared in this scope! {1}".format(node.variable, e))

    def visit_Variable(self, node):
        return self.visit(node.val)

    def visit_MatrixElem(self, node):
        (type, x, y) = self.variables[node.identificator]
        if type != 'matrix':
            self.errors.append("Variable {0} is not a matrix".format(node.identificator))
        type, _, _ = self.visit(node.val1)
        if type != 'int':
            self.errors.append("Variable {0} must be an integer".format(node.val1))
        type, _, _ = self.visit(node.val2)
        if type != 'int':
            self.errors.append("Variable {0} must be an integer".format(node.val2))
        return 'float', 0, 0

    def visit_Conditional(self, node):
        self.visit(node.conditional)
        if node.condSt == 'for' or node.condSt == 'while':
            was_in_loop = self.in_loop
            self.in_loop = True
        self.visit(node.block1)
        if node.block2:
            self.visit(node.block2)
        if node.condSt == 'for' or node.condSt == 'while':
            self.in_loop = was_in_loop

    def visit_Block(self, node):
        self.visit(node.val)

    def visit_PtrValues(self, node):
        pass

    def visit_Rvalue(self, node):
        return self.visit(node.val)

    def visit_Str(self, node):
        return 'string', None, None

    def visit_ForExpr(self, node):
        self.variables[node.identificator] = 'int', None, None
        ret = self.visit(node.start)
        if ret is None:
            return
        type, x, y = ret
        if type != 'int':
            self.errors.append("Start of range must be an integer. Is {0}".format(type))
        type, x, y = self.visit(node.finish)
        if type != 'int':
            self.errors.append("End of range must be an integer. Is {0}".format(type))

    def visit_Matrix(self, node):
        pass

    def visit_Expr(self, node):
        if node.fun is None:
            return self.visit(node.val1)
        ret = self.visit(node.val1)
        if ret is None:
            return None
        type_1, x_1, y_1 = ret
        ret_x = None
        ret_y = None
        if node.val2:
            ret = self.visit(node.val2)
            if ret is None:
                return None
            type_2, x_2, y_2 = ret
            ret_type = types_table[node.fun][type_1][type_2]
            if ret_type is None:
                self.errors.append("Operation {0} not allowed for types {1} and {2}".format(node.fun, type_1, type_2))
            elif type_1 == 'matrix' and type_2 == 'matrix' and \
                        not (x_1 is None or x_2 is None or y_1 is None or y_2 is None):
                if node.fun in ['+', '-', '.+', '.-', '.*', './']:
                    if x_1 != x_2 or y_1 != y_2:
                        self.errors.append("Dimensions don't match for ({0}, {1}) and ({2}, {3})"
                                           .format(x_1, y_1, x_2, y_2))
                    else:
                        ret_x = x_1
                        ret_y = y_1

                if node.fun in ['*', '/']:
                    if x_1 != y_2:
                        self.errors.append("Dimensions don't match for ({0}, {1}) and ({2}, {3})"
                                           .format(x_1, y_1, x_2, y_2))
                    else:
                        ret_x = x_2
                        ret_y = y_1
        else:
            ret_type = types_table[node.fun][type_1][type_1]
            if node.fun in ['zeros', 'ones', 'eye'] and isinstance(node.val1, int):
                ret_x = node.val1
                ret_y = node.val1
            elif node.fun == '.T':
                ret_x = y_1
                ret_y = x_1

        return ret_type, ret_x, ret_y

    def visit_Rows(self, node):
        for i, row in enumerate(node.row_elems):
            if i == 0:
                size = self.visit(row)
            else:
                if self.visit(row) != size:
                    self.errors.append("Improper matrix definition!")


    def visit_RowElems(self, node):
        for i in node.elems:
            self.visit(i)
        return len(node.elems)

    # TODO: nie wiem czy to ma być
    def visit_Error(self, node):
        pass

    def visit_Int(self, node):
        return 'int', None, None

    def visit_Float(self, node):
        return 'float', None, None

    # This is in fact not a string but a variable id
    def visit_str(self, node):
        if node in ['break', 'continue'] and not self.in_loop:
            self.errors.append("Break and continue cannot be used outside loops")
        if node in ['print', 'break', 'continue', 'return']:
            return None
        try:
            return self.variables[node]
        except KeyError as e:
            self.errors.append("Variable {0} not declared in this scope! {1}".format(node, e))
        return None
