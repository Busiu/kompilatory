#!/usr/bin/python

import AST
import ply.yacc as yacc
from scanner import Scanner


reverseSignDict = {'[': ']', '(': ')', '{': '}'}

class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf

#TODO pozbyć się wszystkich warningów
#TODO matrix -> tylko dwa wymiary
#TODO forexpr -> tylko jeden wymiar
#TODO dodać uminus | '-' expr %prec UMINUS (w EXPR)
class Parser2(object):

    tokens = Scanner.tokens

    precedence = (
        # to fill ...
        ("left", "IF"),
        ("left", "ELSE"),
        ("left", ':', ','),
        ("left", '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN', 'DOTADDASSIGN', 'DOTSUBASSIGN',
         'DOTMULASSIGN', 'DOTDIVASSIGN'),
        ("left", '<', '>', 'EQ', 'LEQ', 'GEQ', 'NEQ'),
        ("left", 'UMINUS'),
        ("left", '+', '-', 'DOTADD', 'DOTSUB'),
        ("left", '*', '/', 'DOTMUL', 'DOTDIV'),
        ("left", 'TRANSPOSE')
    )
    def p_program(self, p):
        """program : instructions"""
        p[0] = AST.Program(p[1])

    def p_instructions(self, p):
        """instructions : instruction instructions
                        | instruction
                        | '{' instructions '}'"""
        if len(p) == 3:
            p[0] = AST.Instructions(p[1]) + AST.Instructions(p[2])
        elif len(p) == 2:
            p[0] = AST.Instructions(p[1])
        else:
            p[0] = AST.Instructions(p[2])


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
        """matrixelem   : ID '[' expr ',' expr ']'"""
        p[0] = AST.MatrixElem(p[1], p[3], p[5])

    def p_conditional(self, p):
        """conditional  : IF '(' expr ')' block %prec IF
                        | IF '(' expr ')' block ELSE block
                        | FOR '(' forexpr ')' block
                        | WHILE '(' expr ')' block"""
        if len(p) == 6:
            p[0] = AST.Conditional(p[1], p[3], p[5], None, None)
        else:
            p[0] = AST.Conditional(p[1], p[3], p[5], p[6], p[7])

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
        """rvalue   : expr
                    | matrixelem
                    | str"""
        p[0] = AST.Rvalue(p[1])

    def p_str(self, p):
        """str      : STRING"""
        p[0] = AST.Str(p[1])

    def p_forexpr(self, p):
        """forexpr  : ID '=' expr ':' expr"""
        p[0] = AST.ForExpr(p[1], p[3], p[5])

    def p_rows(self, p):
        """rows : rowelems ';' rows
                | rowelems"""
        if len(p) == 2:
            p[0] = AST.Rows(p[1])
        else:
            p[0] = AST.Rows(p[1]) + AST.Rows(p[3])

    def p_rowelems(self, p):
        """rowelems : rvalue ',' rowelems
                    | rvalue"""
        if len(p) == 2:
            p[0] = AST.RowElems(p[1])
        else:
            p[0] = AST.RowElems(p[1]) + AST.RowElems(p[3])

    def p_expr(self, p):
        """expr : expr '+' expr
                | expr '-' expr
                | expr '*' expr
                | expr '/' expr
                | '-' expr %prec UMINUS
                | expr DOTADD expr
                | expr DOTSUB expr
                | expr DOTMUL expr
                | expr DOTDIV expr
                | expr EQ expr
                | expr GEQ expr
                | expr LEQ expr
                | expr NEQ expr
                | expr '>' expr
                | expr '<' expr
                | '[' rows ']'
                | '(' expr ')'
                | ZEROS '(' expr ')'
                | ONES '(' expr ')'
                | EYE '(' expr ')'
                | expr TRANSPOSE
                | INTEGER
                | FLOAT
                | ID"""
        if len(p) == 4:
            if p[1] is not '(' and p[1] is not '-' and p[1] is not '[':
                p[0] = AST.Expr(p[1], p[3], p[2])
            else:
                p[0] = AST.Expr(p[2], None, p[1])
        elif len(p) == 5:
            p[0] = AST.Expr(p[3], None, p[1])
        elif len(p) == 3:
            if p[1] == '-':
                p[0] = AST.Expr(p[2], None, p[1])
            else:
                p[0] = AST.Expr(p[1], None, p[2])
        else:
            p[0] = p[1]

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
