from parser2 import Parser2
import TreePrinter
from type_checker import TypeChecker


def main():
    fh = open("Text Files/Task 2/example1.txt", "r")
    data = fh.read()
    my_parser = Parser2()
    result = my_parser.parse(data)
    checker = TypeChecker()
    checker.visit(result)

    print(result)
    print(checker.get_errors())

main()
