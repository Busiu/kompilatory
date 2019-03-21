from scanner import Scanner


def main():
    fh = open("text.txt", "r")
    data = fh.read()
    my_scanner = Scanner()
    for token in my_scanner.scan(data):
        print("(%d, %d): %s(%s)" % (token.lineno, token.lexpos, token.type, token.value))


main()
