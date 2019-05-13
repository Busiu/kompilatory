from parser2 import Parser2
import TreePrinter
from type_checker import TypeChecker
from Interpreter import Interpreter


def main():
    fh = open("Text Files/Task 5/example2.txt", "r")
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

main()
