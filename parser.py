#!/usr/bin/python

import ply.yacc as yacc


class Parser(object):

    precedence = (
        # to fill ...
        ("left", '=', '+=', '-=', '*=', '/='),
        ("left", '+', '-'),
        ("left", '*', '/')
        # to fill ...
    )


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
        else:
            print("Unexpected end of input")


    def p_program(self, p):
        """program : instructions_opt"""


    def p_instructions_opt_1(self, p):
        """instructions_opt : instructions """


    def p_instructions_opt_2(self, p):
        """instructions_opt : """


    def p_instructions_1(self, p):
        """instructions : instructions instruction """


    def p_instructions_2(self, p):
        """instructions : instruction """


    # to finish the grammar
    # ....
    def __init__(self, tokens):


    parser = yacc.yacc()
