from parser2 import Parser2
import TreePrinter
from type_checker import TypeChecker
from Interpreter import Interpreter
from matrix_operations import *


def main():
    fh = open("Text Files/Task 5/example3.txt", "r")
    data = fh.read()

    my_parser = Parser2()
    ast = my_parser.parse(data)

    if ast is not None:
        checker = TypeChecker()
        checker.visit(ast)

        errors = checker.get_errors()

        if len(errors) > 0:
            for err in errors:
                print(err)
        else:
            interpreter = Interpreter()
            result = interpreter.visit(ast)

            print(ast)
            print(result)


def test():
    lol = ones(4)
    lol2 = zeros(4)
    lol3 = eye(4)
    print(lol, lol2, lol3)

    print(lol + lol3)

    print(lol * lol3)

    mul1 = Matrix([[1, 1, 1],
            [1, 1, 1]])
    mul2 = Matrix([[2, 2],
            [3, 3],
            [4, 4]])

    print(mul1 * mul2)


main()
