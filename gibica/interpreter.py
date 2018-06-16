"""Interpreter."""

from collections import OrderedDict
from gibica.lexer import Name


class NodeVisitor(object):
    """Postorder traversal strategy."""

    def visit(self, node):
        """Visit the right method of the child class according to the node."""
        method = 'visit_' + type(node).__name__
        return getattr(self, method, self.fallback)(node)

    def fallback(self, node):
        """Fallback if the child method doesn't exist."""
        raise Exception(f'INTERPRETER: No visit_{type(node).__name__} method.')


#
# Symbol table
#

class Symbol(object):
    """Container of a symbol."""

    def __init__(self, name, type=None):
        """Initialization of `Symbol` class."""
        self.name = name
        self.type = type


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

    def __init__(self, name, type):
        """Initialization of `VarSymbol` class."""
        super().__init__(name, type)

    def __str__(self):
        """String representation of a variable symbol."""
        return f'<{self.name}:{self.type}>'

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
        var_symbol = VarSymbol(var_name, type_symbol)
        self.SYMBOL_TABLE[var_symbol.name] = var_symbol
        self.visit(node.assignment)

    def visit_Assign(self, node):
        """Visitor for `Assign` AST node."""
        var_name = node.left.value
        var_symbol = self.SYMBOL_TABLE.get(var_name)
        if var_symbol is None:
            raise Exception(
                f'SYMBOL TABLE: Variable {repr(var_name)} not declared.'
            )
        self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.SYMBOL_TABLE.get(var_name)

        if var_symbol is None:
            raise Exception(
                f'SYMBOL TABLE: Variable {repr(var_name)} not declared.'
            )

    def visit_BinOp(self, node):
        """Visitor for `BinOp` AST node."""
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        """Visitor for `UnaryOp` AST node."""
        self.visit(node.right)

    def visit_Num(self, node):
        """Visitor for `Num` AST node."""
        pass

    def build(self):
        """Generic entrypoint of `SymbolTableBuilder` class."""
        self.visit(self.tree)


#
# Program Evaluation
#

class Interpreter(NodeVisitor):
    """Evaluation of raw input."""

    def __init__(self, tree):
        """Initialization of `Interpreter` class."""
        self.tree = tree
        self.GLOBAL_MEMORY = {}

    def visit_Compound(self, node):
        """Visitor for `Compound` AST node."""
        for child in node.children:
            self.visit(child)

    def visit_VarDecl(self, node):
        """Visitor for `VarDecl` AST node."""
        self.visit(node.assignment)

    def visit_Assign(self, node):
        """Visitor for `Assign` AST node."""
        self.GLOBAL_MEMORY[node.left.value] = self.visit(node.right)

    def visit_Var(self, node):
        """Visitor for `Var` AST node."""
        variable_name = node.value
        variable_value = self.GLOBAL_MEMORY.get(variable_name)
        return variable_value

    def visit_VarType(self, node):
        """Visitor for `VarType` AST node."""
        pass

    def visit_BinOp(self, node):
        """Visitor for `BinOp` AST node."""
        if node.op.name == Name.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.name == Name.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.name == Name.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.name == Name.DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.name == Name.INT_DIV:
            return self.visit(node.left) // self.visit(node.right)

    def visit_UnaryOp(self, node):
        """Visitor for `UnaryOp` AST node."""
        if node.op.name == Name.PLUS:
            return +self.visit(node.right)
        elif node.op.name == Name.MINUS:
            return -self.visit(node.right)

    def visit_Num(self, node):
        """Visitor for `Num` AST node."""
        return node.value

    def interpret(self):
        """Generic entrypoint of `Interpreter` class."""
        if self.tree is None:
            return ''
        return self.visit(self.tree)
