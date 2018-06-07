"""Parser."""

from gibica.lexer import Type


#
# Syntax Analysis
#

class AST(object):
    """Parent class of all AST classes."""
    pass


class BinOp(AST):
    """Binary operands AST representation."""

    def __init__(self, left, op, right):
        """Initialization of `BinOp` class."""
        self.left = left
        self.op = self.token = op
        self.right = right


class UnaryOp(AST):
    """Unary oprerands AST representation."""

    def __init__(self, op, right):
        """Initialization of `UnaryOp` class."""
        self.op = self.token = op
        self.right = right


class Num(AST):
    """Numeric AST representation."""

    def __init__(self, token):
        """Initialization of `Num` class."""
        self.token = token
        self.value = token.value


class Parser(object):
    """Parser returning an AST of the input."""

    def __init__(self, lexer):
        """Initialization of `Interpreter` class."""
        self.lexer = lexer
        self.token = self.lexer.next_token()

    def process(self, type):
        """Process the current token."""
        if self.token.type == type:
            self.token = self.lexer.next_token()
        else:
            raise Exception(f'SYNTAX: Error processing `{self.token}`.')

    def factor(self):
        """
        Rule: `term: (PLUS | MINUS) INTEGER | INTEGER | LPAREN expr RPAREN`.
        """
        token = self.token
        if token.type == Type.PLUS:
            self.process(Type.PLUS)
            return UnaryOp(op=token, right=self.factor())
        elif token.type == Type.MINUS:
            self.process(Type.MINUS)
            return UnaryOp(op=token, right=self.factor())
        elif token.type == Type.INTEGER:
            self.process(Type.INTEGER)
            return Num(token)
        elif token.type == Type.LPAREN:
            self.process(Type.LPAREN)
            node = self.expr()
            self.process(Type.RPAREN)
            return node

    def term(self):
        """Rule: `factor:  term ((MUL | DIV) term )*`."""
        node = self.factor()

        while self.token.type in (Type.MUL, Type.DIV):
            token = self.token
            if token.type == Type.MUL:
                self.process(Type.MUL)
            elif token.type == Type.DIV:
                self.process(Type.DIV)
            else:
                raise Exception(f'SYNTAX: Unknown operande `{token}`.')

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """Rule: `expr: factor((PLUS | MINUS) factor )*`."""
        node = self.term()

        while self.token.type in (Type.PLUS, Type.MINUS):
            token = self.token
            if token.type == Type.PLUS:
                self.process(Type.PLUS)
            elif token.type == Type.MINUS:
                self.process(Type.MINUS)
            else:
                raise Exception(f'SYNTAX: Unknown operande `{token}`.')

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        """Generic entrypoint of the `Parse` class."""
        return self.expr()
