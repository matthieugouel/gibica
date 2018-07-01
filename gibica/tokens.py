"""Tokens module."""


class Name(object):
    """Enumeration of token names."""

    ID = 'ID'

    INT_NUMBER = 'INT_NUMBER'
    FLOAT_NUMBER = 'FLOAT_NUMBER'
    TRUE = 'TRUE'
    FALSE = 'FALSE'

    LET = 'LET'
    MUT = 'MUT'

    EQ = 'EQ'
    NE = 'NE'
    LE = 'LE'
    GE = 'GE'
    LT = 'LT'
    GT = 'GT'

    OR = 'OR'
    AND = 'AND'
    NOT = 'NOT'

    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = 'MUL'
    DIV = 'DIV'
    INT_DIV = 'INT_DIV'

    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'

    LBRACKET = 'LBRACKET'
    RBRACKET = 'RBRACKET'

    ASSIGN = 'ASSIGN'

    IF = 'IF'
    ELSE = 'ELSE'

    WHILE = 'WHILE'

    DEF = 'DEF'

    RETURN = 'RETURN'

    COMMA = 'COMMA'
    SEMI = 'SEMI'
    EOF = 'EOF'


class Token(object):
    """Token container"""

    def __init__(self, name, value):
        """Initialization of `Token` class."""
        self.name = name
        self.value = value

    def __str__(self):
        """String representation of a token."""
        return f"Token({self.name}, {self.value})"

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()


# List of reserved keywords
RESERVED_KEYWORDS: dict = {
    'let': Token(Name.LET, 'let'),
    'mut': Token(Name.MUT, 'mut'),


    'true': Token(Name.TRUE, 'true'),
    'false': Token(Name.FALSE, 'false'),

    'or': Token(Name.OR, 'or'),
    'and': Token(Name.AND, 'and'),
    'not': Token(Name.NOT, 'not'),

    'if': Token(Name.IF, 'if'),
    'else': Token(Name.ELSE, 'else'),

    'while': Token(Name.WHILE, 'while'),

    'def': Token(Name.DEF, 'def'),

    'return': Token(Name.RETURN, 'return'),
}
