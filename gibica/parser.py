"""Parser."""

from gibica.lexer import Type


#
# Syntax Analysis
#

class AST(object):
    """Parent class of all AST classes."""
    pass


class Compound(AST):
    """Bloc AST representation."""

    def __init__(self):
        """Initialization of `Compound` class."""
        self.children = []


class Assign(AST):
    """Assignment AST representation."""

    def __init__(self, left, op, right):
        """Initialization of `Assign` class."""
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    """Variable AST representation."""

    def __init__(self, token):
        """Initialization of `Var` class."""
        self.token = token
        self.value = token.value


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

    def _process(self, type):
        """Process the current token. Protected."""
        if self.token.type == type:
            self.token = self.lexer.next_token()
        else:
            self._error()

    def _error(self):
        """Raise a Syntax Error."""
        raise Exception(f'SYNTAX: Error processing `{self.token}`.')

    def program(self):
        """Rule: `(program: statement SEMI)*`."""
        root = Compound()

        while self.token.type != Type.EOF:
            root.children.append(self.statement())
            self._process(Type.SEMI)

        return root

    def statement(self):
        """Rule: `statement: assignment_statement`."""
        if self.token.type == Type.ID:
            node = self.assignment_statement()
        else:
            node = self._error()

        return node

    def assignment_statement(self):
        """Rule: `assignment_statement : variable ASSIGN expr`."""
        left = self.variable()
        token = self.token
        self._process(Type.ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def expr(self):
        """Rule: `expr: term ((PLUS | MINUS) term)*`."""
        node = self.term()

        while self.token.type in (Type.PLUS, Type.MINUS):
            token = self.token
            if token.type == Type.PLUS:
                self._process(Type.PLUS)
            elif token.type == Type.MINUS:
                self._process(Type.MINUS)
            else:
                raise Exception(f'SYNTAX: Unknown operand `{token}`.')

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def term(self):
        """Rule: `factor:  factor ((MUL | DIV) factor)*`."""
        node = self.factor()

        while self.token.type in (Type.MUL, Type.DIV):
            token = self.token
            if token.type == Type.MUL:
                self._process(Type.MUL)
            elif token.type == Type.DIV:
                self._process(Type.DIV)
            else:
                raise Exception(f'SYNTAX: Unknown operand `{token}`.')

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        """
        Rule: `term: (PLUS | MINUS) INTEGER | INTEGER | LPAREN expr RPAREN`.
        """
        token = self.token
        if token.type == Type.PLUS:
            self._process(Type.PLUS)
            return UnaryOp(op=token, right=self.factor())
        elif token.type == Type.MINUS:
            self._process(Type.MINUS)
            return UnaryOp(op=token, right=self.factor())
        elif token.type == Type.INTEGER:
            self._process(Type.INTEGER)
            return Num(token)
        elif token.type == Type.LPAREN:
            self._process(Type.LPAREN)
            node = self.expr()
            self._process(Type.RPAREN)
            return node
        else:
            return self.variable()

    def variable(self):
        """Rule: `variable: ID`."""
        node = Var(self.token)
        self._process(Type.ID)
        return node

    def parse(self):
        """Generic entrypoint of the `Parser` class."""
        node = self.program()
        if self.token.type != Type.EOF:
            self._error()

        return node
