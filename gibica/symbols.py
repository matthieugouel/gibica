"""Symbols module."""

from collections import OrderedDict
from gibica.ast import NodeVisitor, FuncDecl, ReturnStatement
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

    def visit_Program(self, node):
        """Vsitor for `Program` AST node."""
        for child in node.children:
            # Skip function declaration nodes
            if not isinstance(child, FuncDecl):
                self.visit(child)

    def visit_Compound(self, node):
        """Visitor for `Compound` AST node."""
        for child in node.children:
            if isinstance(child, ReturnStatement):
                return self.visit(child)
            self.visit(child)

    def visit_FuncDecl(self, node):
        """Visitor for `FuncDecl` AST node."""
        self.visit(node.body)

    def visit_Params(self, node):
        """Visitor for `Params` AST node."""
        pass

    def visit_VarDecl(self, node):
        """Visitor for `VarDecl` AST node."""
        var_name = node.assignment.left.atom.name
        var_is_mutable = node.assignment.left.is_mutable
        var_symbol = VarSymbol(var_name, var_is_mutable)

        if self.SYMBOL_TABLE.get(var_name) is not None:
            raise SementicError(
                f'Variable `{var_name}` is already declared.'
            )

        self.SYMBOL_TABLE[var_symbol.name] = var_symbol

    def visit_Assign(self, node):
        """Visitor for `Assign` AST node."""
        var_name = node.left.atom.name
        var_symbol = self.SYMBOL_TABLE.get(var_name)

        if var_symbol is not None and not var_symbol.is_mutable:
            raise SementicError(
                f'Re-assignment of immutable variable `{var_name}`.'
            )

        self.visit(node.left)
        self.visit(node.right)

    def visit_Var(self, node):
        """Visitor for `Var` AST node."""
        var_name = node.atom.name
        var_symbol = self.SYMBOL_TABLE.get(var_name)

        if var_symbol is None:
            raise SementicError(
                f'Variable `{var_name}` is not declared.'
            )

    def visit_Atom(self, node):
        """Visitor for `Atom` AST node."""
        pass

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

    def visit_BinOp(self, node):
        """Visitor for `BinOp` AST node."""
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        """Visitor for `UnaryOp` AST node."""
        self.visit(node.right)

    def visit_FuncCall(self, node):
        """Visitor for `FuncCall` AST node."""
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
