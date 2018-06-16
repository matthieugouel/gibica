"""Parser."""

from gibica.lexer import Name


#
# Syntax Analysis
#

class AST(object):
    """Parent class of all AST classes."""
    pass


class Compound(AST):
    """Compound AST representation."""

    def __init__(self):
        """Initialization of `Compound` class."""
        self.children = []


class VarDecl(AST):
    """Variable declaration AST representation."""

    def __init__(self, var_type, assignment):
        """Initialization of `VarDecl` class."""
        self.var_type = var_type
        self.assignment = assignment


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


class VarType(AST):
    """Variable Type AST representation."""

    def __init__(self, token):
        """Initialization of `Type` class."""
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

    def _process(self, name):
        """Process the current token."""
        if self.token.name == name:
            self.token = self.lexer.next_token()
        else:
            self._error()

    def _error(self):
        """Raise a Syntax Error."""
        raise Exception(f'SYNTAX: Error processing `{self.token}`.')

    def program(self):
        """
        program: (statement)*
        """
        root = Compound()

        while self.token.name != Name.EOF:
            root.children.append(self.statement())

        return root

    def statement(self):
        """
        statement: declaration_statement
                 | expression_statement
        """
        if self.token.name in (Name.INT, Name.FLOAT):
            node = self.declaration_statement()
        elif self.token.name == Name.ID:
            node = self.expression_statement()
        else:
            node = self._error()

        return node

    def declaration_statement(self):
        """
        declaration_statement: var_type assignment SEMI
        """
        node = VarDecl(self.var_type(), self.assignment())
        self._process(Name.SEMI)
        return node

    def var_type(self):
        """
        var_type: INT
                | FLOAT
        """
        node = VarType(self.token)

        if self.token.name == Name.INT:
            self._process(Name.INT)
        elif self.token.name == Name.FLOAT:
            self._process(Name.FLOAT)
        else:
            self._error()

        return node

    def expression_statement(self):
        """
        expression_statement: assignment SEMI
        """
        node = self.assignment()
        self._process(Name.SEMI)
        return node

    def assignment(self):
        """
        assignment : variable ASSIGN expr
        """
        left = self.variable()
        token = self.token
        self._process(Name.ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        variable: ID
        """
        node = Var(self.token)
        self._process(Name.ID)
        return node

    def expr(self):
        """
        expr: term ((PLUS | MINUS) term)*
        """
        node = self.term()

        while self.token.name in (Name.PLUS, Name.MINUS):
            token = self.token
            if token.name == Name.PLUS:
                self._process(Name.PLUS)
            elif token.name == Name.MINUS:
                self._process(Name.MINUS)
            else:
                raise Exception(f'SYNTAX: Unknown operand `{token}`.')

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def term(self):
        """
        term: factor ((MUL | DIV | INT_DIV) factor)*
        """
        node = self.factor()

        while self.token.name in (Name.MUL, Name.DIV, Name.INT_DIV):
            token = self.token
            if token.name == Name.MUL:
                self._process(Name.MUL)
            elif token.name == Name.DIV:
                self._process(Name.DIV)
            elif token.name == Name.INT_DIV:
                self._process(Name.INT_DIV)
            else:
                raise Exception(f'SYNTAX: Unknown operand `{token}`.')

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        """
        factor: PLUS factor
              | MINUS factor
              | INT_NUMBER
              | FLOAT_NUMBER
              | LPAREN expr RPAREN
              | variable
        """
        token = self.token
        if token.name == Name.PLUS:
            self._process(Name.PLUS)
            return UnaryOp(op=token, right=self.factor())
        elif token.name == Name.MINUS:
            self._process(Name.MINUS)
            return UnaryOp(op=token, right=self.factor())
        elif token.name == Name.INT_NUMBER:
            self._process(Name.INT_NUMBER)
            return Num(token)
        elif token.name == Name.FLOAT_NUMBER:
            self._process(Name.FLOAT_NUMBER)
            return Num(token)
        elif token.name == Name.LPAREN:
            self._process(Name.LPAREN)
            node = self.expr()
            self._process(Name.RPAREN)
            return node
        else:
            return self.variable()

    def parse(self):
        """Generic entrypoint of the `Parser` class."""
        node = self.program()
        if self.token.name != Name.EOF:
            self._error()

        return node
