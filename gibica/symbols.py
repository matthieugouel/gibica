"""Symbols module."""

from collections import OrderedDict
from gibica.ast import NodeVisitor
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


class VarSymbol(Symbol):
    """Container of a variable symbol."""

    def __init__(self, name, is_mutable):
        """Initialization of `VarSymbol` class."""
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

    def visit_Compound(self, node):
        """Visitor for `Compound` AST node."""
        for child in node.children:
            self.visit(child)

    def visit_VarDecl(self, node):
        """Visitor for `VarDecl` AST node."""
        var_name = node.assignment.left.value
        var_is_mutable = node.assignment.left.is_mutable
        var_symbol = VarSymbol(var_name, var_is_mutable)

        if self.SYMBOL_TABLE.get(var_name) is not None:
            raise SementicError(
                f'Variable `{var_name}` is already declared.'
            )

        self.SYMBOL_TABLE[var_symbol.name] = var_symbol

    def visit_Assign(self, node):
        """Visitor for `Assign` AST node."""
        var_name = node.left.value
        var_symbol = self.SYMBOL_TABLE.get(var_name)

        if var_symbol is not None and not var_symbol.is_mutable:
            raise SementicError(
                f'Re-assignment of immutable variable `{var_name}`.'
            )

        self.visit(node.left)
        self.visit(node.right)

    def visit_Var(self, node):
        """Visitor for `Var` AST node."""
        var_name = node.value
        var_symbol = self.SYMBOL_TABLE.get(var_name)

        if var_symbol is None:
            raise SementicError(
                f'Variable `{var_name}` is not declared.'
            )

    def visit_IfStatement(self, node):
        """Visitor for `IfStatement` AST node."""
        if_conditon, if_body = node.if_statement
        if self.visit(if_conditon):
            return self.visit(if_body)
        else:
            for else_if_statement in node.else_if_statements:
                else_if_condition, else_if_body = else_if_statement
                if self.visit(else_if_condition):
                    return self.visit(else_if_body)

            _, else_body = node.else_statement
            return self.visit(else_body)

    def visit_BinOp(self, node):
        """Visitor for `BinOp` AST node."""
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        """Visitor for `UnaryOp` AST node."""
        self.visit(node.right)

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
