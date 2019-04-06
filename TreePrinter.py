from __future__ import print_function
import AST

indent_char = '|'

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator


def print_with_str(val, indent):
    if isinstance(val, str):
        return indent * indent_char + val
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

    @addToClass(AST.Rvalue)
    def print_tree(self, indent=0):
        return print_with_str(self.val, indent)

    @addToClass(AST.Error)
    def print_tree(self, indent=0):
        return "error"
        # fill in the body


    # define printTree for other classes
    # ...


