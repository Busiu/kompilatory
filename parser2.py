#!/usr/bin/python

import ply.yacc as yacc
from scanner import Scanner


class Parser2(object):

    tokens = Scanner.tokens

    precedence = (
        # to fill ...
        ("left", '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN', 'DOTADDASSIGN', 'DOTSUBASSIGN',
            'DOTMULASSIGN', 'DOTDIVASSIGN'),
        ("left", '+', '-'),
        ("left", '*', '/'),
        ("left", 'TRANSPOSE')
        # to fill ...
    )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
        else:
            print("Unexpected end of input")

    def p_program(self, p):
        """program : instructions"""
        return p

    def p_instructions(self, p):
        """instructions : instruction
                        | instruction instructions"""
        return p

    def p_instruction(self, p):
        """instruction : assignment ';'
                       | conditional
                       | BREAK ';'
                       | CONTINUE ';'
                       | RETURN ';'
                       | prt ';' """

    def p_assignment(self, p):
        """assignment : ID '=' rvalue
                      | ID DOTADDASSIGN rvalue
                      | ID DOTSUBASSIGN rvalue
                      | ID DOTMULASSIGN rvalue
                      | ID DOTDIVASSIGN rvalue
                      | ID ADDASSIGN rvalue
                      | ID SUBASSIGN rvalue
                      | ID MULASSIGN rvalue
                      | ID DIVASSIGN rvalue"""
        return p[3]

    def p_conditional(self, p):
        """conditional : IF '(' logexpr ')' '{' instructions '}'
                       | IF '(' logexpr ')' instruction
                       | IF '(' logexpr ')' '{' instructions '}' ELSE '{' instructions '}'
                       | IF '(' logexpr ')' instruction ELSE '{' instructions '}'
                       | IF '(' logexpr ')' '{' instructions '}' ELSE instruction
                       | IF '(' logexpr ')' instruction ELSE instruction
                       | FOR '(' forexpr ')' '{' instructions '}'
                       | FOR '(' forexpr ')' instructions
                       | WHILE '(' logexpr ')' '{' instructions '}'
                       | WHILE '(' logexpr ')' instruction """

    def p_prt(self, p):
        """prt : PRINT '(' ID ')'
               | PRINT '(' rvalue ')' """

    def p_rvalue(self, p):
        """rvalue : numexpr
                  | matrix
                  | logexpr
                  | STRING"""
        p[0] = p[1]

    def p_forexpr(self, p):
        """forexpr : matrix
                   | ID '=' matrix
                   | ID"""

    def p_matrix(self, p):
        """matrix : numexpr ':' numexpr
                  | '(' matrix ')'
                  | ZEROS '(' numexpr ')'
                  | ONES '(' numexpr ')'
                  | EYE '(' numexpr ')'
                  | matrix TRANSPOSE
                  | ID """

    def p_logexpr(self, p):
        """logexpr : numexpr EQ numexpr
                   | numexpr GEQ numexpr
                   | numexpr LEQ numexpr
                   | numexpr NEQ numexpr
                   | numexpr '>' numexpr
                   | numexpr '<' numexpr
                   | ID"""
        if p[2] == '==':
            value = (p[1] == p[3])
        elif p[2] == '>=':
            value = (p[1] >= p[3])
        elif p[2] == '<=':
            value = (p[1] <= p[3])
        elif p[2] == '!=':
            value = (p[1] != p[3])
        elif p[2] == '>':
            value = (p[1] > p[3])
        elif p[2] == '<':
            value = (p[1] < p[3])
        else:
            raise AssertionError('Unknown operator: {}'.format(p[2]))
        p[0] = value

    def p_numexpr(self, p):
        """numexpr : numexpr '+' numexpr
                   | numexpr '-' numexpr
                   | numexpr '*' numexpr
                   | numexpr '/' numexpr
                   | numexpr DOTADD numexpr
                   | numexpr DOTSUB numexpr
                   | numexpr DOTMUL numexpr
                   | numexpr DOTDIV numexpr
                   | '(' numexpr ')'
                   | '-' numexpr
                   | INTEGER
                   | FLOAT
                   | ID"""
        if len(p) == 2:
            value = p[1]
        elif p[2] == '+':
            value = p[1] + p[3]
        elif p[2] == '-':
            value = p[1] - p[3]
        elif p[2] == '*':
            value = p[1] * p[3]
        elif p[2] == '/':
            value = p[1] / p[3]
        elif p[1] == '(' and p[3] == ')':
            value = p[2]
        elif p[1] == '-':
            value = -p[2]
        else:
            raise AssertionError('Unknown operator: {}'.format(p[2]))
        p[0] = value

    def __init__(self):
        self.lexer = Scanner()
        self.parser = yacc.yacc(module=self)


    def parse(self, data):
        return self.parser.parse(data)