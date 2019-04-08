from __future__ import print_function
import AST

indent_char = '| '


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
    if isinstance(val, int):
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
        ret = self.instruction.print_tree(indent)
        if self.instructions is not None:
            ret += self.instructions.print_tree(indent)
        return ret

    @addToClass(AST.Instruction)
    def print_tree(self, indent=0):
        ret = ""
        if self.val2 is None:
            ret += print_with_str(self.val1, indent)
            ret += '\n'
        else:
            ret += print_with_str(self.val1, indent)
            ret += '\n'
            ret += print_with_str(self.val2, indent + 1)
            ret += '\n'
        return ret

    @addToClass(AST.Assignment)
    def print_tree(self, indent=0):
        ret = print_with_str(self.op, indent)
        ret += '\n'
        ret += print_with_str(self.variable, indent + 1)
        ret += '\n'
        ret += print_with_str(self.rvalue, indent + 1)
        return ret

    @addToClass(AST.Variable)
    def print_tree(self, indent=0):
        return print_with_str(self.val, indent)

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

    @addToClass(AST.Cond)
    def print_tree(self, indent=0):
        return print_with_str(self.val, indent)

    @addToClass(AST.Block)
    def print_tree(self, indent=0):
        return print_with_str(self.val, indent)

    @addToClass(AST.PtrValues)
    def print_tree(self, indent=0):
        return print_with_str(self.vals, indent)

    @addToClass(AST.Rvalue)
    def print_tree(self, indent=0):
        return print_with_str(self.val, indent)

    @addToClass(AST.ForExpr)
    def print_tree(self, indent=0):
        ret = print_with_str(self.identificator, indent)
        ret += '\n'
        ret += print_with_str("range", indent)
        ret += '\n'
        ret += print_with_str(self.val, indent + 1)
        return ret

    @addToClass(AST.Matrix)
    def print_tree(self, indent=0):
        if self.val2 is not None:
            ret = print_with_str(self.val1, indent)
            ret += '\n'
            ret += print_with_str(self.val2, indent)
            return ret
        elif(self.fun == "zeros" or self.fun == "ones" or self.fun == "eye" or self.fun == ".T"):
            ret = print_with_str(self.fun, indent)
            ret += '\n'
            ret += print_with_str(self.val1, indent + 1)
            return ret
        elif self.fun == '[':
            ret = print_with_str("VECTOR", indent)
            ret += '\n'
            ret += print_with_str(self.val1, indent + 1)
            return ret
        else:
            return print_with_str(self.val1, indent + 1)

    @addToClass(AST.Rows)
    def print_tree(self, indent=0):
        ret = ""
        if self.rows is None:
            ret += print_with_str(self.rowelems, indent)
            return ret
        else:
            ret += print_with_str(self.rowelems, indent)
            ret += '\n'
            ret += print_with_str(self.rows, indent)
            return ret

    @addToClass(AST.RowElems)
    def print_tree(self, indent=0):
        if self.rowelems is None:
            return print_with_str(self.rvalue, indent)
        else:
            ret = print_with_str(self.rvalue, indent)
            ret += '\n'
            ret += print_with_str(self.rowelems, indent)
            return ret

    @addToClass(AST.LogExpr)
    def print_tree(self, indent=0):
        ret = print_with_str(self.op, indent)
        ret += '\n'
        ret += print_with_str(self.expr1, indent + 1)
        ret += '\n'
        ret += print_with_str(self.expr2, indent + 1)
        return ret

    @addToClass(AST.NumExpr)
    def print_tree(self, indent=0):
        if self.op is None:
            return print_with_str(self.val1, indent)
        ret = print_with_str(self.op, indent)
        ret += '\n'
        ret += print_with_str(self.val1, indent + 1)
        if self.val2 is not None:
            ret += '\n'
            ret += print_with_str(self.val2, indent + 1)
        return ret

    @addToClass(AST.Error)
    def print_tree(self, indent=0):
        raise Exception("Something went wrong...")