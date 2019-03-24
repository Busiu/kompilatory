from parser2 import Parser2


def main():
    fh = open("text.txt", "r")
    data = fh.read()
    my_parser = Parser2()
    print(my_parser.parse("a=3;"))


main()
