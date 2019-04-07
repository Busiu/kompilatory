#!/usr/bin/python

import AST
import ply.yacc as yacc
from scanner import Scanner


class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf


class Parser2(object):

    tokens = Scanner.tokens

    precedence = (
        # to fill ...
        ("left", '<', '>', 'EQ', 'LEQ', 'GEQ', 'NEQ'),
        ("left", '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN', 'DOTADDASSIGN', 'DOTSUBASSIGN',
            'DOTMULASSIGN', 'DOTDIVASSIGN'),
        ("left", '+', '-', 'DOTADD', 'DOTSUB'),
        ("left", '*', '/', 'DOTMUL', 'DOTDIV'),
        ("left", 'TRANSPOSE'),
        ("left", '[', ']', '('),
        ("left", '{', '}', 'BREAK', 'CONTINUE', 'RETURN', 'PRINT', 'WHILE',
         'FOR', 'ONES', 'ZEROS', 'EYE', 'IF', 'ELSE'),
        ("left", ';', ',')
        # to fill ...
    )
    def p_program(self, p):
        """program : instructions"""
        p[0] = AST.Program(p[1])

    def p_instructions(self, p):
        """instructions : instruction instructions
                        | instruction
                        | '{' instructions '}'"""
        if len(p) == 3:
            p[0] = AST.Instructions(p[1], p[2])
        elif len(p) == 2:
            p[0] = AST.Instructions(p[1], None)
        else:
            p[0] = AST.Instructions(p[2], None)


    def p_instruction(self, p):
        """instruction  : assignment ';'
                        | conditional
                        | BREAK ';'
                        | CONTINUE ';'
                        | RETURN rvalue ';'
                        | RETURN ';'
                        | PRINT '(' prtvalues ')' ';' """
        if len(p) == 2 or len(p) == 3:
            p[0] = AST.Instruction(p[1], None)
        elif len(p) == 4:
            p[0] = AST.Instruction(p[1], p[2])
        else:
            p[0] = AST.Instruction(p[1], p[3])

    def p_assignment(self, p):
        """assignment   : variable '=' rvalue
                        | variable DOTADDASSIGN rvalue
                        | variable DOTSUBASSIGN rvalue
                        | variable DOTMULASSIGN rvalue
                        | variable DOTDIVASSIGN rvalue
                        | variable ADDASSIGN rvalue
                        | variable SUBASSIGN rvalue
                        | variable MULASSIGN rvalue
                        | variable DIVASSIGN rvalue"""
        p[0] = AST.Assignment(p[1], p[2], p[3])

    def p_variable(self, p):
        """variable : ID
                    | matrixelem"""
        p[0] = AST.Variable(p[1])

    def p_matrixelem(self, p):
        """matrixelem   : ID '[' numexpr ',' numexpr ']'"""
        p[0] = AST.MatrixElem(p[1], p[3], p[5])

    def p_conditional(self, p):
        """conditional  : IF '(' cond ')' block
                        | IF '(' cond ')' block ELSE block
                        | FOR '(' forexpr ')' block
                        | WHILE '(' cond ')' block"""
        if len(p) == 6:
            p[0] = AST.Conditional(p[1], p[3], p[5], None, None)
        else:
            p[0] = AST.Conditional(p[1], p[3], p[5], p[6], p[7])

    def p_cond(self, p):
        """cond : logexpr
                | ID"""
        p[0] = AST.Cond(p[1])

    def p_block(self, p):
        """block : instruction
                 | '{' instructions '}' """
        if len(p) == 2:
            p[0] = AST.Block(p[1])
        else:
            p[0] = AST.Block(p[2])

    def p_prtvalues(self, p):
        """prtvalues    : rvalue ',' prtvalues
                        | rvalue"""
        if len(p) == 2:
            p[0] = AST.PtrValues([p[1]])
        else:
            p[0] = AST.PtrValues([p[1]] + p[3].vals)

    def p_rvalue(self, p):
        """rvalue   : numexpr
                    | matrix
                    | logexpr
                    | STRING
                    | ID"""
        p[0] = AST.Rvalue(p[1])

    def p_forexpr(self, p):
        """forexpr  : ID '=' matrix"""
        p[0] = AST.ForExpr(p[1], p[3])

    def p_matrix(self, p):
        """matrix   : numexpr ':' numexpr
                    | '[' rows ']'
                    | '(' matrix ')'
                    | ZEROS '(' numexpr ')'
                    | ONES '(' numexpr ')'
                    | EYE '(' numexpr ')'
                    | matrix TRANSPOSE
                    | ID"""
        if len(p) == 3:
            if p[2] == ':':
                p[0] = AST.Matrix(p[1], p[2], p[3])
            else:
                p[0] = AST.Matrix(p[2], 'VECTOR', None)
        if len(p) == 4:
            p[0] = AST.Matrix(p[3], p[1], None)
        else:
            p[0] = AST.Matrix(p[1], None, None)

    def p_rows(self, p):
        """rows : rowelems ';' rows
                | rowelems"""
        if len(p) == 2:
            p[0] = AST.Rows(p[1], None)
        else:
            p[0] = AST.Rows(p[1], p[3])

    def p_rowelems(self, p):
        """rowelems : rvalue ',' rowelems
                    | rvalue"""
        if len(p) == 2:
            p[0] = AST.Rows(p[1], None)
        else:
            p[0] = AST.Rows(p[1], p[3])

    def p_logexpr(self, p):
        """logexpr  : numexpr EQ numexpr
                    | numexpr GEQ numexpr
                    | numexpr LEQ numexpr
                    | numexpr NEQ numexpr
                    | numexpr '>' numexpr
                    | numexpr '<' numexpr"""
        p[0] = AST.LogExpr(p[1], p[2], p[3])
#        if p[2] == '==':
#            value = (p[1] == p[3])
#        elif p[2] == '>=':
#            value = (p[1] >= p[3])
#        elif p[2] == '<=':
#            value = (p[1] <= p[3])
#        elif p[2] == '!=':
#            value = (p[1] != p[3])
#        elif p[2] == '>':
#            value = (p[1] > p[3])
#        elif p[2] == '<':
#            value = (p[1] < p[3])
#        else:
#            raise AssertionError('Unknown operator: {}'.format(p[2]))
#        p[0] = value

    def p_numexpr(self, p):
        """numexpr  : numexpr '+' numexpr
                    | numexpr '-' numexpr
                    | numexpr '*' numexpr
                    | numexpr '/' numexpr
                    | numexpr DOTADD numexpr
                    | numexpr DOTSUB numexpr
                    | numexpr DOTMUL numexpr
                    | numexpr DOTDIV numexpr
                    | '(' numexpr ')'
                    | '-' numexpr
                    | ID
                    | INTEGER
                    | FLOAT
                    | matrix"""
        if len(p) == 4:
            if p[1] == '(':
                p[0] = AST.NumExpr(p[2], None, None)  # '(' numexpr ')'
            else:
                p[0] = AST.NumExpr(p[1], p[2], p[3])  # numexpr op numexpr
        elif len(p) == 3:
            p[0] = AST.NumExpr(p[2], p[1], None)  # -numexpr
        else:
            p[0] = AST.NumExpr(p[1], None, None)  # numexpr

    def p_error(self, p):
        if p:
            print(p)
            print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
        else:
            print("Unexpected end of input")
        AST.Error()

    def __init__(self):
        self.lexer = Scanner()
        self.parser = yacc.yacc(module=self)

    def parse(self, data):
        return self.parser.parse(data)
