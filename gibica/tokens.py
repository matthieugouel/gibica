"""Tokens module."""


class Name(object):
    """Enumeration of token names."""

    ID = 'ID'

    INT = 'INT'
    FLOAT = 'FLOAT'
    BOOL = 'BOOL'

    INT_NUMBER = 'INT_NUMBER'
    FLOAT_NUMBER = 'FLOAT_NUMBER'
    TRUE = 'TRUE'
    FALSE = 'FALSE'

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

    ASSIGN = 'ASSIGN'

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

    def ___repr__(self):
        """String representation of the class."""
        return self.__str__()
