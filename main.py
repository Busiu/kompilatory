from parser2 import Parser2


def main():
    fh = open("Tekscicho 3", "r")
    data = fh.read()
    my_parser = Parser2()
    result = my_parser.parse(data)
    print(result)

main()
