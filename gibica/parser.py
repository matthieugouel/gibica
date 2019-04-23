"""Parser module."""

from gibica.tokens import Nature
from gibica.exceptions import SyntaxError
from gibica.ast import (
    Program,
    Compound,
    FunctionDeclaration,
    Parameters,
    FunctionBody,
    FunctionCall,
    VariableDeclaration,
    Assignment,
    Variable,
    IfStatement,
    WhileStatement,
    ReturnStatement,
    BinaryOperation,
    UnaryOperation,
    Identifier,
    Integer,
    FloatingPoint,
    Boolean,
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
        if self.token.nature == name:
            self.token = self.lexer.next_token()
        else:
            self._error()

    def _error(self):
        """Raise a Syntax Error."""
        raise SyntaxError(f"Unable to process `{self.token}`.")

    def program(self):
        """
        program: (statement)*
        """
        root = Program()

        while self.token.nature != Nature.EOF:
            root.children.append(self.statement())

        return root

    def statement(self):
        """
        statement: function_declaration
                 | variable_declaration
                 | expression_statement
                 | if_statement
                 | while_statement
                 | jump_statement
        """
        if self.token.nature == Nature.DEF:
            node = self.function_declaration()
        elif self.token.nature == Nature.LET:
            node = self.variable_declaration()
        elif self.token.nature in (Nature.MUT, Nature.ID):
            node = self.expression_statement()
        elif self.token.nature == Nature.IF:
            node = self.if_statement()
        elif self.token.nature == Nature.WHILE:
            node = self.while_statement()
        elif self.token.nature == Nature.RETURN:
            node = self.jump_statement()
        else:
            node = self._error()

        return node

    def function_declaration(self):
        """
        function_declaration: 'def' ID parameters compound
        """
        self._process(Nature.DEF)

        identifier = Identifier(self.token.value)
        self._process(Nature.ID)

        parameters = self.parameters()
        return FunctionDeclaration(
            identifier=identifier, parameters=parameters, body=self.function_body()
        )

    def parameters(self):
        """
        parameters: '(' logical_or_expr (',' logical_or_expr)* ')'
        """
        nodes = []
        self._process(Nature.LPAREN)

        while self.token.nature != Nature.RPAREN:

            nodes.append(Parameters(variable=self.logical_or_expr()))

            if self.token.nature == Nature.COMMA:
                self._process(Nature.COMMA)

        self._process(Nature.RPAREN)
        return nodes

    def function_body(self):
        """
        function_body: '{' (statement)* '}'
        """
        root = FunctionBody()
        self._process(Nature.LBRACKET)

        while self.token.nature != Nature.RBRACKET:
            root.children.append(self.statement())

        self._process(Nature.RBRACKET)
        return root

    def variable_declaration(self):
        """
        variable_declaration: 'let' assignment ';'
        """
        self._process(Nature.LET)
        node = VariableDeclaration(assignment=self.assignment())
        self._process(Nature.SEMI)
        return node

    def expression_statement(self):
        """
        expression_statement: assignment ';'
        """
        node = self.assignment()
        self._process(Nature.SEMI)
        return node

    def assignment(self):
        """
        assignment: logical_or_expr ['=' logical_or_expr]
        """
        node = self.logical_or_expr()
        if self.token.nature == Nature.ASSIGN:
            token = self.token
            self._process(Nature.ASSIGN)
            right = self.logical_or_expr()
            return Assignment(left=node, op=token, right=right)
        else:
            return node

    def if_statement(self):
        """
        if_statement: 'if' logical_or_expr compound
                    ('else' 'if' local_or_expr compound)*
                    ['else' compound]
        """
        self._process(Nature.IF)
        if_condition = self.logical_or_expr()
        if_body = self.compound()

        else_compound = None
        else_if_compounds = []
        while self.token.nature == Nature.ELSE:
            self._process(Nature.ELSE)

            if self.token.nature == Nature.IF:
                self._process(Nature.IF)
                else_if_compounds.append((self.logical_or_expr(), self.compound()))
            else:
                else_compound = (None, self.compound())

        return IfStatement(
            if_compound=(if_condition, if_body),
            else_if_compounds=else_if_compounds,
            else_compound=else_compound,
        )

    def while_statement(self):
        """
        while_statement: 'while' local_or_expr compound
        """
        self._process(Nature.WHILE)
        condition = self.logical_or_expr()
        compound = self.compound()
        return WhileStatement(condition=condition, compound=compound)

    def compound(self):
        """
        compound: '{' (statement)* '}'
        """
        root = Compound()
        self._process(Nature.LBRACKET)

        while self.token.nature != Nature.RBRACKET:
            root.children.append(self.statement())

        self._process(Nature.RBRACKET)
        return root

    def jump_statement(self):
        """
        jump_statement: 'return' expression_statement
        """
        self._process(Nature.RETURN)
        return ReturnStatement(expression=self.expression_statement())

    def logical_or_expr(self):
        """
        logical_or_expr: logical_and_expr ('or' logical_and_expr)*
        """
        node = self.logical_and_expr()

        while self.token.nature == Nature.OR:
            token = self.token
            self._process(Nature.OR)

            node = BinaryOperation(left=node, op=token, right=self.logical_and_expr())

        return node

    def logical_and_expr(self):
        """
        logical_and_expr: logical_not_expr ('and' logical_not_expr)*
        """
        node = self.logical_not_expr()

        while self.token.nature == Nature.AND:
            token = self.token
            self._process(Nature.AND)

            node = BinaryOperation(left=node, op=token, right=self.logical_not_expr())

        return node

    def logical_not_expr(self):
        """
        logical_not_expr: 'not' logical_not_expr
                        | comparison
        """
        if self.token.nature == Nature.NOT:
            token = self.token
            self._process(Nature.NOT)
            return UnaryOperation(op=token, right=self.logical_not_expr())
        else:
            return self.comparison()

    def comparison(self):
        """
        comparison: expr (('==' | '!=' | '<=' | '>=' | '<' | '>') expr)*
        """
        node = self.expr()

        while self.token.nature in (
            Nature.EQ,
            Nature.NE,
            Nature.LE,
            Nature.GE,
            Nature.LT,
            Nature.GT,
        ):
            token = self.token
            if token.nature == Nature.EQ:
                self._process(Nature.EQ)
            elif token.nature == Nature.NE:
                self._process(Nature.NE)
            elif token.nature == Nature.LE:
                self._process(Nature.LE)
            elif token.nature == Nature.GE:
                self._process(Nature.GE)
            elif token.nature == Nature.LT:
                self._process(Nature.LT)
            elif token.nature == Nature.GT:
                self._process(Nature.GT)
            else:
                self.error()

            node = BinaryOperation(left=node, op=token, right=self.expr())

        return node

    def expr(self):
        """
        expr: term (('+' | '-') term)*
        """
        node = self.term()

        while self.token.nature in (Nature.PLUS, Nature.MINUS):
            token = self.token
            if token.nature == Nature.PLUS:
                self._process(Nature.PLUS)
            elif token.nature == Nature.MINUS:
                self._process(Nature.MINUS)
            else:
                self._error()

            node = BinaryOperation(left=node, op=token, right=self.term())

        return node

    def term(self):
        """
        term: atom (('*' | '/' | '//') atom)*
        """
        node = self.atom()

        while self.token.nature in (Nature.MUL, Nature.DIV, Nature.INT_DIV):
            token = self.token
            if token.nature == Nature.MUL:
                self._process(Nature.MUL)
            elif token.nature == Nature.DIV:
                self._process(Nature.DIV)
            elif token.nature == Nature.INT_DIV:
                self._process(Nature.INT_DIV)
            else:
                self._error()

            node = BinaryOperation(left=node, op=token, right=self.atom())

        return node

    def call(self):
        """
        call: ['mut'] ID [parameters]
        """
        is_mutable = False
        if self.token.nature == Nature.MUT:
            is_mutable = True
            self._process(Nature.MUT)

        identifier = Identifier(name=self.token.value)
        self._process(Nature.ID)

        if self.token.nature == Nature.LPAREN:
            return FunctionCall(identifier=identifier, parameters=self.parameters())
        else:
            return Variable(identifier=identifier, is_mutable=is_mutable)

    def atom(self):
        """
        atom: '+' atom
            | '-' atom
            | call
            | INT_NUMBER
            | FLOAT_NUMBER
            | '(' logical_or_expr ')'
            | TRUE
            | FALSE
        """
        token = self.token
        if token.nature == Nature.PLUS:
            self._process(Nature.PLUS)
            return UnaryOperation(op=token, right=self.atom())
        elif token.nature == Nature.MINUS:
            self._process(Nature.MINUS)
            return UnaryOperation(op=token, right=self.atom())
        elif token.nature in (Nature.MUT, Nature.ID):
            return self.call()
        elif token.nature == Nature.INT_NUMBER:
            self._process(Nature.INT_NUMBER)
            return Integer(token)
        elif token.nature == Nature.FLOAT_NUMBER:
            self._process(Nature.FLOAT_NUMBER)
            return FloatingPoint(token)
        elif token.nature == Nature.LPAREN:
            self._process(Nature.LPAREN)
            node = self.logical_or_expr()
            self._process(Nature.RPAREN)
            return node
        elif token.nature == Nature.TRUE:
            self._process(Nature.TRUE)
            return Boolean(token)
        elif token.nature == Nature.FALSE:
            self._process(Nature.FALSE)
            return Boolean(token)
        else:
            self._error()

    def parse(self):
        """Generic entrypoint of the `Parser` class."""
        node = self.program()
        if self.token.nature != Nature.EOF:
            self._error()

        return node
