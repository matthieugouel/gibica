"""Symbols module."""

from collections import OrderedDict
from gibica.ast import NodeVisitor, FunctionDeclaration, ReturnStatement
from gibica.exceptions import SementicError


#
# Symbol table
#

class Symbol(object):
    """Container of a symbol."""

    def __init__(self, name, is_mutable):
        """Initialization of `Symbol` class."""
        self.name = name
        self.is_mutable = is_mutable


class VariableSymbol(Symbol):
    """Container of a variable symbol."""

    def __init__(self, name, is_mutable):
        """Initialization of `VariableSymbol` class."""
        super().__init__(name, is_mutable)

    def __str__(self):
        """String representation of a variable symbol."""
        return f"<{self.name}{':mut' if self.is_mutable else ''}>"

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()


class SymbolTable(OrderedDict):
    """Symbol ADT stack."""

    def __str__(self):
        """String representation of the symbol table."""
        str = '{symbols}'.format(
            symbols=[value for value in self.values()]
        )
        return str

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()


class SymbolTableBuilder(NodeVisitor):
    """Responsible for building the symbol table."""

    def __init__(self, tree):
        """Initialization of `SymbolTableBuilder` class."""
        self.tree = tree
        self.SYMBOL_TABLE = SymbolTable()

    def visit_Program(self, node):
        """Vsitor for `Program` AST node."""
        for child in node.children:
            # Skip function declaration nodes
            if not isinstance(child, FunctionDeclaration):
                self.visit(child)

    def visit_Compound(self, node):
        """Visitor for `Compound` AST node."""
        for child in node.children:
            if isinstance(child, ReturnStatement):
                return self.visit(child)
            self.visit(child)

    def visit_FunctionDeclaration(self, node):
        """Visitor for `FunctionDeclaration` AST node."""
        self.visit(node.body)

    def visit_Parameters(self, node):
        """Visitor for `Parameters` AST node."""
        pass

    def visit_VariableDeclaration(self, node):
        """Visitor for `VariableDeclaration` AST node."""
        var_name = node.assignment.left.identifier.name
        var_is_mutable = node.assignment.left.is_mutable
        var_symbol = VariableSymbol(var_name, var_is_mutable)

        if self.SYMBOL_TABLE.get(var_name) is not None:
            raise SementicError(
                f'Variable `{var_name}` is already declared.'
            )

        self.SYMBOL_TABLE[var_symbol.name] = var_symbol

    def visit_Assignment(self, node):
        """Visitor for `Assignment` AST node."""
        var_name = node.left.identifier.name
        var_symbol = self.SYMBOL_TABLE.get(var_name)

        if var_symbol is not None and not var_symbol.is_mutable:
            raise SementicError(
                f'Re-assignment of immutable variable `{var_name}`.'
            )

        self.visit(node.left)
        self.visit(node.right)

    def visit_Variable(self, node):
        """Visitor for `Variable` AST node."""
        var_name = node.identifier.name
        var_symbol = self.SYMBOL_TABLE.get(var_name)

        if var_symbol is None:
            raise SementicError(
                f'Variable `{var_name}` is not declared.'
            )

    def visit_IfStatement(self, node):
        """Visitor for `IfStatement` AST node."""
        if_conditon, if_body = node.if_compound
        if self.visit(if_conditon):
            self.visit(if_body)
        else:
            for else_if_compound in node.else_if_compounds:
                else_if_condition, else_if_body = else_if_compound
                if self.visit(else_if_condition):
                    self.visit(else_if_body)
                    break
            else:
                if node.else_compound is not None:
                    _, else_body = node.else_compound
                    self.visit(else_body)

    def visit_WhileStatement(self, node):
        """Visitor for `WhileStatement` AST node."""
        while self.visit(node.condition):
            self.visit(node.compound)

    def visit_ReturnStatement(self, node):
        """Visitor for `WhileStatement` AST node."""
        return self.visit(node.expression)

    def visit_BinaryOperation(self, node):
        """Visitor for `BinaryOperation` AST node."""
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOperation(self, node):
        """Visitor for `UnaryOperation` AST node."""
        self.visit(node.right)

    def visit_FunctionCall(self, node):
        """Visitor for `FunctionCall` AST node."""
        pass

    def visit_Identifier(self, node):
        """Visitor for `Identifier` AST node."""
        pass

    def visit_Integer(self, node):
        """Visitor for `Integer` AST node."""
        pass

    def visit_FloatingPoint(self, node):
        """Visitor for `FloatingPoint` AST node."""
        pass

    def visit_Boolean(self, node):
        """Visitor for `Boolean` AST node."""
        pass

    def build(self):
        """Generic entrypoint of `SymbolTableBuilder` class."""
        self.visit(self.tree)
