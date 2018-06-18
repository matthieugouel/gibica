"""Symbol module."""

from collections import OrderedDict
from gibica.parser.ast import NodeVisitor


#
# Symbol table
#

class Symbol(object):
    """Container of a symbol."""

    def __init__(self, name, type=None, is_mutable=None):
        """Initialization of `Symbol` class."""
        self.name = name
        self.type = type
        self.is_mutable = is_mutable


class BuiltinTypeSymbol(Symbol):
    """Container of a Built-in type symbol."""

    def __init__(self, name):
        """Initialization of `BuiltinTypeSymbol` class."""
        super().__init__(name)

    def __str__(self):
        """String representation of a built-in symbol."""
        return self.name

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()


class VarSymbol(Symbol):
    """Container of a variable symbol."""

    def __init__(self, name, type, is_mutable):
        """Initialization of `VarSymbol` class."""
        super().__init__(name, type, is_mutable)

    def __str__(self):
        """String representation of a variable symbol."""
        return f"<{self.name}:{self.type}{':mut' if self.is_mutable else ''}>"

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
        type_name = node.var_type.value
        type_symbol = BuiltinTypeSymbol(type_name)
        var_name = node.assignment.left.value
        var_is_mutable = node.assignment.left.is_mutable
        var_symbol = VarSymbol(var_name, type_symbol, var_is_mutable)

        if self.SYMBOL_TABLE.get(var_name) is not None:
            raise Exception(
                (f'SEMENTIC ERROR: '
                 f'Variable `{var_name}` is already declared.')
            )

        self.SYMBOL_TABLE[var_symbol.name] = var_symbol

    def visit_VarType(self, node):
        """Visitor for `VarType` AST node."""
        pass

    def visit_Assign(self, node):
        """Visitor for `Assign` AST node."""
        var_name = node.left.value
        var_symbol = self.SYMBOL_TABLE.get(var_name)

        if var_symbol is not None and not var_symbol.is_mutable:
            raise Exception(
                (f'SEMENTIC ERROR: '
                 f'Re-assignment of immutable variable `{var_name}`.')
            )

        self.visit(node.left)
        self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.SYMBOL_TABLE.get(var_name)

        if var_symbol is None:
            raise Exception(
                (f'SEMENTIC ERROR: '
                 f'Variable `{var_name}` is not declared.')
            )

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
