"""Tokens module."""

from enum import Enum


class Nature(Enum):
    """Enumeration of token natures."""

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

    def __init__(self, nature, value):
        """Initialization of `Token` class."""
        self.nature = nature
        self.value = value

    def __str__(self):
        """String representation of a token."""
        return f"Token({self.nature}, \"{self.value}\")"

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()  # pragma: no cover


# List of reserved keywords
RESERVED_KEYWORDS: dict = {
    'let': Token(Nature.LET, 'let'),
    'mut': Token(Nature.MUT, 'mut'),
    'true': Token(Nature.TRUE, 'true'),
    'false': Token(Nature.FALSE, 'false'),
    'or': Token(Nature.OR, 'or'),
    'and': Token(Nature.AND, 'and'),
    'not': Token(Nature.NOT, 'not'),
    'if': Token(Nature.IF, 'if'),
    'else': Token(Nature.ELSE, 'else'),
    'while': Token(Nature.WHILE, 'while'),
    'def': Token(Nature.DEF, 'def'),
    'return': Token(Nature.RETURN, 'return'),
}
