import ply.lex as lex

# TODO zamienić floata na takiego jak trzeba


class Scanner(object):
    tokens = (
        'DOTADD',
        'DOTSUB',
        'DOTMUL',
        'DOTDIV',
        'ADDASSIGN',
        'SUBASSIGN',
        'MULASSIGN',
        'DIVASSIGN',
        'DOTADDASSIGN',
        'DOTSUBASSIGN',
        'DOTMULASSIGN',
        'DOTDIVASSIGN',
        'LEQ',
        'GEQ',
        'NEQ',
        'EQ',
        'IF',
        'ELSE',
        'FOR',
        'WHILE',
        'BREAK',
        'CONTINUE',
        'RETURN',
        'ONES',
        'ZEROS',
        'EYE',
        'TRANSPOSE',
        'PRINT',
        'FLOAT',
        'INTEGER',
        'STRING',
        'ID',
        'COMMENT'
        )
    literals = "+-*/=<>()[]{}:,;_#"

    t_DOTADD = r'\.\+'
    t_DOTSUB = r'\.-'
    t_DOTMUL = r'\.\*'
    t_DOTDIV = r'\./'
    t_ADDASSIGN = r'\+='
    t_SUBASSIGN = r'-='
    t_MULASSIGN = r'\*='
    t_DIVASSIGN = r'/='
    t_DOTADDASSIGN = r'\.\+='
    t_DOTSUBASSIGN = r'\.-='
    t_DOTMULASSIGN = r'\.\*='
    t_DOTDIVASSIGN = r'\./='
    t_TRANSPOSE = r'.T'
    t_LEQ = r'<='
    t_GEQ = r'>='
    t_NEQ = r'!='
    t_EQ = r'=='
    t_ignore = '  \t'

    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'for': 'FOR',
        'while': 'WHILE',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        'return': 'RETURN',
        'ones': 'ONES',
        'zeros': 'ZEROS',
        'eye': 'EYE',
        'print': 'PRINT'
    }

    def t_ID(self, t):
        '[a-z_A-Z]\w*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_FLOAT(self, t):
        r'[0-9]*\.([0-9]+([eE](-)?[0-9]+)?)?'
        t.value = float(t.value)
        return t

    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        '\".*\"'
        return t

    def t_COMMENT(self, t):
        r'\#.*'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def __init__(self):
        # build the lexer
        self.lexer = lex.lex(module=self)

    def scan(self, data):
        self.lexer.input(data)
        return self.lexer.lextokens

