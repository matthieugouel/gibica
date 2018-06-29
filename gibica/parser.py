"""Parser module."""

from gibica.tokens import Name
from gibica.exceptions import SyntaxError
from gibica.ast import (
    Program,
    Compound,
    FuncDecl,
    Params,
    VarDecl,
    Assign,
    Var,
    IfStatement,
    WhileStatement,
    BinOp,
    UnaryOp,
    Integer,
    FloatingPoint,
    Boolean
)


#
# Syntax Analysis
#

class Parser(object):
    """Parser returning an AST of the input."""

    def __init__(self, lexer):
        """Initialization of `Parser` class."""
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
        raise SyntaxError(
            f'Unable to process `{self.token}`.'
        )

    def program(self):
        """
        program: (statement)*
        """
        root = Program()

        while self.token.name != Name.EOF:
            root.children.append(self.statement())

        return root

    def compound_statement(self):
        """
        compound_statement: LBRACKET (statements)* RBRACKET
        """
        root = Compound()
        self._process(Name.LBRACKET)

        while self.token.name != Name.RBRACKET:
            root.children.append(self.statement())

        self._process(Name.RBRACKET)
        return root

    def statement(self):
        """
        statement: declaration_statement
                 | expression_statement
                 | if_statement
        """
        if self.token.name == Name.LET:
            node = self.declaration_statement()
        elif self.token.name == Name.ID:
            node = self.expression_statement()
        elif self.token.name == Name.IF:
            node = self.if_statement()
        elif self.token.name == Name.WHILE:
            node = self.while_statement()
        elif self.token.name == Name.DEF:
            node = self.function_definition()
        else:
            node = self._error()

        return node

    def function_definition(self):
        """
        function_definition: DEF ID parameters compound_statement
        """
        self._process(Name.DEF)
        name = self.token.value
        self._process(Name.ID)
        parameters = self.parameters()
        return FuncDecl(
            name=name,
            parameters=parameters,
            body=self.compound_statement()
        )

    def parameters(self):
        """
        parameters: LPAREN [variable] (COMMA variable)* RPAREN
        """
        nodes = []
        self._process(Name.LPAREN)

        while self.token.name != Name.RPAREN:
            nodes.append(Params(self.variable()))

            if self.token.name == Name.COMMA:
                self._process(Name.COMMA)

        self._process(Name.RPAREN)

        return nodes

    def declaration_statement(self):
        """
        declaration_statement: LET assignment SEMI
        """
        self._process(Name.LET)
        node = VarDecl(self.assignment())
        self._process(Name.SEMI)
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
        assignment : variable ASSIGN logical_or_expr
        """
        left = self.variable()
        token = self.token
        self._process(Name.ASSIGN)
        right = self.logical_or_expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        variable: [MUT] ID
        """
        is_mutable = False
        if self.token.name == Name.MUT:
            is_mutable = True
            self._process(Name.MUT)

        node = Var(self.token, is_mutable)
        self._process(Name.ID)
        return node

    def if_statement(self):
        """
        if_statement: IF logical_or_expr compound_statement
                    (ELSE IF local_or_expr compound_statement)*
                    [ELSE compound_statement]
        """
        self._process(Name.IF)
        if_condition = self.logical_or_expr()
        if_body = self.compound_statement()

        else_compound = None
        else_if_compounds = []
        while self.token.name == Name.ELSE:
            self._process(Name.ELSE)

            if self.token.name == Name.IF:
                self._process(Name.IF)
                else_if_compounds.append(
                    (self.logical_or_expr(), self.compound_statement())
                )
            else:
                else_compound = (None, self.compound_statement())

        return IfStatement(
            if_compound=(if_condition, if_body),
            else_if_compounds=else_if_compounds,
            else_compound=else_compound
        )

    def while_statement(self):
        """
        while_statement: WHILE local_or_expr compound_statement
        """
        self._process(Name.WHILE)
        condition = self.logical_or_expr()
        compound = self.compound_statement()
        return WhileStatement(condition=condition, compound=compound)

    def logical_or_expr(self):
        """
        logical_or_expr: logical_and_expr (OR logical_and_expr)*
        """
        node = self.logical_and_expr()

        while self.token.name == Name.OR:
            token = self.token
            self._process(Name.OR)

            node = BinOp(left=node, op=token, right=self.logical_and_expr())

        return node

    def logical_and_expr(self):
        """
        logical_and_expr: logical_not_expr (AND logical_not_expr)*
        """
        node = self.logical_not_expr()

        while self.token.name == Name.AND:
            token = self.token
            self._process(Name.AND)

            node = BinOp(left=node, op=token, right=self.logical_not_expr())

        return node

    def logical_not_expr(self):
        """
        logical_not_expr: NOT logical_not_expr
                        | comparison
        """
        if self.token.name == Name.NOT:
            token = self.token
            self._process(Name.NOT)
            return UnaryOp(op=token, right=self.logical_not_expr())
        else:
            return self.comparison()

    def comparison(self):
        """
        comparison: expr ((EQ | NE | LE | GE | LT | GT) expr)*
        """
        node = self.expr()

        while self.token.name in (
                Name.EQ, Name.NE, Name.LE, Name.GE, Name.LT, Name.GT
        ):
            token = self.token
            if token.name == Name.EQ:
                self._process(Name.EQ)
            elif token.name == Name.NE:
                self._process(Name.NE)
            elif token.name == Name.LE:
                self._process(Name.LE)
            elif token.name == Name.GE:
                self._process(Name.GE)
            elif token.name == Name.LT:
                self._process(Name.LT)
            elif token.name == Name.GT:
                self._process(Name.GT)
            else:
                self.error()

            node = BinOp(left=node, op=token, right=self.expr())

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
                self._error()

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
                self._error()

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        """
        factor: PLUS factor
              | MINUS factor
              | INT_NUMBER
              | FLOAT_NUMBER
              | LPAREN logical_or_expr RPAREN
              | TRUE
              | FALSE
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
            return Integer(token)
        elif token.name == Name.FLOAT_NUMBER:
            self._process(Name.FLOAT_NUMBER)
            return FloatingPoint(token)
        elif token.name == Name.LPAREN:
            self._process(Name.LPAREN)
            node = self.logical_or_expr()
            self._process(Name.RPAREN)
            return node
        elif token.name == Name.TRUE:
            self._process(Name.TRUE)
            return Boolean(token)
        elif token.name == Name.FALSE:
            self._process(Name.FALSE)
            return Boolean(token)
        else:
            return self.variable()

    def parse(self):
        """Generic entrypoint of the `Parser` class."""
        node = self.program()
        if self.token.name != Name.EOF:
            self._error()

        return node
