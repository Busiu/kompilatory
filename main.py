from parser2 import Parser2
import TreePrinter

def main():
    fh = open("Text Files/Task 3/example3.txt", "r")
    data = fh.read()
    my_parser = Parser2()
    result = my_parser.parse(data)
    print(result)

main()
