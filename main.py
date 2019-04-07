from parser2 import Parser2

def main():
    fh = open("Text files/example2.txt", "r")
    data = fh.read()
    my_parser = Parser2()
    result = my_parser.parse(data)
    print(result)

main()
