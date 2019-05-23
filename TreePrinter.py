from __future__ import print_function
import AST

indent_char = '| '
reverseSignDict = {'[': ']', '(': ')', '{': '}'}


def addToClass(cls):

    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


def print_with_str(val, indent):
    if isinstance(val, str):
        return indent * indent_char + val
    if isinstance(val, list):
        ret = ""
        for (i, v) in enumerate(val):
            if i != 0:
                ret += '\n'
            ret += print_with_str(v, indent)
        return ret
    if isinstance(val, (int, float)):
        return indent * indent_char + str(val)
    else:
        return val.print_tree(indent)


class TreePrinter:

    @addToClass(AST.Node)
    def print_tree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def print_tree(self, indent=0):
        return self.instructions.print_tree(indent)

    @addToClass(AST.Instructions)
    def print_tree(self, indent=0):
        ret = ""
        for i, instruction in enumerate(self.instructions):
            if i != 0:
                ret += '\n'
            ret += print_with_str(instruction, indent)

        return ret
        # return print_with_str(self.instructions, indent)

    @addToClass(AST.Instruction)
    def print_tree(self, indent=0):
        ret = ""
        if self.val2 is None:
            ret += print_with_str(self.val1, indent)
        else:
            ret += print_with_str(self.val1, indent)
            ret += '\n'
            ret += print_with_str(self.val2, indent + 1)
        return ret

    @addToClass(AST.Assignment)
    def print_tree(self, indent=0):
        ret = print_with_str(self.op, indent)
        ret += '\n'
        ret += print_with_str(self.variable, indent + 1)
        ret += '\n'
        ret += print_with_str(self.rvalue, indent + 1)
        return ret
    
    @addToClass(AST.MatrixElem)
    def print_tree(self, indent=0):
        ret = print_with_str(self.identificator, indent)
        ret += '\n'
        ret += print_with_str(self.val1, indent + 1)
        ret += '\n'
        ret += print_with_str(self.val2, indent + 1)
        return ret

    @addToClass(AST.Conditional)
    def print_tree(self, indent=0):
        ret = print_with_str(self.condSt, indent)
        ret += '\n'
        ret += print_with_str(self.conditional, indent + 1)
        if self.condSt == "if":
            ret += '\n'
            ret += print_with_str("then", indent)
        ret += '\n'
        ret += print_with_str(self.block1, indent + 1)
        if self.block2 is not None:
            ret += '\n'
            ret += print_with_str(self.elseSt, indent)
            ret += '\n'
            ret += print_with_str(self.block2, indent + 1)
        return ret

    @addToClass(AST.Block)
    def print_tree(self, indent=0):
        return print_with_str(self.val, indent)

    @addToClass(AST.PtrValues)
    def print_tree(self, indent=0):
        return print_with_str(self.vals, indent)

    @addToClass(AST.Rvalue)
    def print_tree(self, indent=0):
        return print_with_str(self.val, indent)

    @addToClass(AST.Str)
    def print_tree(self, indent=0):
        return print_with_str(self.val, indent)

    @addToClass(AST.ForExpr)
    def print_tree(self, indent=0):
        ret = print_with_str(self.identificator, indent)
        ret += '\n'
        ret += print_with_str("range", indent)
        ret += '\n'
        ret += print_with_str(self.start, indent + 1)
        ret += '\n'
        ret += print_with_str(self.finish, indent + 1)
        return ret

    @addToClass(AST.Expr)
    def print_tree(self, indent=0):
        if self.val2 is not None and self.fun is not None:
            ret = print_with_str(self.fun, indent)
            ret += '\n'
            ret += print_with_str(self.val1, indent + 1)
            ret += '\n'
            ret += print_with_str(self.val2, indent + 1)
            return ret
        else:
            ret = print_with_str(self.fun, indent)
            ret += '\n'
            ret += print_with_str(self.val1, indent + 1)
            if self.fun in reverseSignDict.keys():
                ret += '\n'
                ret += print_with_str(reverseSignDict[self.fun], indent)
            return ret

    @addToClass(AST.Rows)
    def print_tree(self, indent=0):
        ret = ""
        for i, elem in enumerate(self.row_elems):
            if i != 0:
                ret += '\n'
            ret += print_with_str(elem, indent)
        return ret

    @addToClass(AST.RowElems)
    def print_tree(self, indent=0):
        ret = ""
        for i, elem in enumerate(self.elems):
            if i != 0:
                ret += '\n'
            ret += print_with_str(elem, indent)
        return ret

    @addToClass(AST.Int)
    def print_tree(self, indent=0):
        return print_with_str(self.val, indent)

    @addToClass(AST.Float)
    def print_tree(self, indent=0):
        return print_with_str(self.val, indent)

    @addToClass(AST.Id)
    def print_tree(self, indent=0):
        return print_with_str(self.name, indent)

    @addToClass(AST.Error)
    def print_tree(self, indent=0):
        raise Exception("Something went wrong...")