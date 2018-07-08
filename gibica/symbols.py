"""Symbols module."""

from collections import OrderedDict
from gibica.ast import NodeVisitor, FunctionDeclaration
from gibica.exceptions import SementicError


#
# Symbol table
#


class Symbol(object):
    """Container of a symbol."""

    def __init__(self, name):
        """Initialization of `Symbol` class."""
        self.name = name


class VariableSymbol(Symbol):
    """Container of a variable symbol."""

    def __init__(self, name, is_mutable):
        """Initialization of `VariableSymbol` class."""
        super().__init__(name)
        self.is_mutable = is_mutable

    def __str__(self):
        """String representation of a variable symbol."""
        return f"<{self.name}{':mut' if self.is_mutable else ''}>"

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()


class FunctionSymbol(Symbol):
    """Container of a function symbol."""

    def __init__(self, name, parameters):
        """Initialization of `VariableSymbol` class."""
        super().__init__(name)
        self.parameters = parameters if parameters else []

    def __str__(self):
        """String representation of a variable symbol."""
        return f"<func:{self.name}:{str(self.parameters)}>"

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()


class Table(OrderedDict):
    """Symbol table object."""

    def __init__(self, *args, **kwargs):
        """Initialization of `Table` class."""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """String representation of the symbol table."""
        return '{symbols}'.format(symbols=[value for value in self.values()])

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()


class Stack(list):
    """Stack of `Table` objects."""

    def __init__(self, *args, **kwargs):
        """Initialization of `Stack` class."""
        super().__init__(*args, **kwargs)

    @property
    def current(self):
        """Get the current frame of the stack."""
        return self[-1]


class SymbolTable(object):
    """Symbol ADT stack."""

    def __init__(self, **kwags):
        """Initialization of `Memory` class."""
        self.stack = Stack([Table(**kwags)])

    def __getitem__(self, value):
        """Get a value from the current scope in the current table."""
        return self.stack.current.get(value)

    def __setitem__(self, key, value):
        """Set a value from the current scope in the current table."""
        self.stack.current[key] = value

    def append_table(self, **kwargs):
        """Create a new table."""
        self.stack.append(Table(**kwargs))

    def pop_table(self):
        """Delete the current table."""
        self.stack.pop()

    def __str__(self):
        """String representation of the symbol table."""
        return str(self.stack)

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()


class SymbolTableBuilder(NodeVisitor):
    """Responsible for building the symbol table."""

    def __init__(self, tree):
        """Initialization of `SymbolTableBuilder` class."""
        self.tree = tree
        self.table = SymbolTable()

    def load_functions(self, tree):
        """Load the functions in the scope."""
        for child in tree.children:
            if isinstance(child, FunctionDeclaration):
                if self.table[child.identifier.name] is not None:
                    raise SementicError(
                        f"Function `{child.identifier.name}` already declared."
                    )
                self.table[child.identifier.name] = child

    def visit_Program(self, node):
        """Vsitor for `Program` AST node."""
        for child in node.children:
            if not isinstance(child, FunctionDeclaration):
                self.visit(child)

    def visit_FunctionDeclaration(self, node):
        """Visitor for `FunctionDeclaration` AST node."""
        for parameter in node.parameters:
            var_name = parameter.variable.identifier.name
            var_is_mutable = parameter.variable.is_mutable
            var_symbol = VariableSymbol(var_name, var_is_mutable)

            if self.table[var_name] is not None:
                raise SementicError(f"Duplicated `{var_name}` function parameter.")

            self.table[var_name] = var_symbol

        self.visit(node.body)

    def visit_Parameters(self, node):
        """Visitor for `Parameters` AST node."""
        pass

    def visit_FunctionBody(self, node):
        """Visitor for `FunctionBody` AST node."""
        for child in node.children:
            self.visit(child)

    def visit_FunctionCall(self, node):
        """Visitor for `FunctionCall` AST node."""
        call = self.table[node.identifier.name]
        if call is None:
            raise SementicError(f"Function `{node.identifier.name}` not declared.")

        if len(call.parameters) != len(node.parameters):
            raise SementicError("Mismatch between call and function parameters number.")

        self.table.append_table()
        self.visit(call)
        self.table.pop_table()

    def visit_VariableDeclaration(self, node):
        """Visitor for `VariableDeclaration` AST node."""
        var_name = node.assignment.left.identifier.name
        var_is_mutable = node.assignment.left.is_mutable
        var_symbol = VariableSymbol(var_name, var_is_mutable)

        if self.table[var_name] is not None:
            raise SementicError(f"Variable `{var_name}` is already declared.")

        self.table[var_symbol.name] = var_symbol

        self.visit(node.assignment.left)
        self.visit(node.assignment.right)

    def visit_Assignment(self, node):
        """Visitor for `Assignment` AST node."""
        var_name = node.left.identifier.name
        var_symbol = self.table[var_name]

        if var_symbol is not None and not var_symbol.is_mutable:
            raise SementicError(f"Re-assignment of immutable variable `{var_name}`.")

        self.visit(node.left)
        self.visit(node.right)

    def visit_Variable(self, node):
        """Visitor for `Variable` AST node."""
        var_name = node.identifier.name
        var_symbol = self.table[var_name]

        if var_symbol is None:
            raise SementicError(f"Variable `{var_name}` is not declared.")

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

    def visit_Compound(self, node):
        """Visitor for `Compound` AST node."""
        for child in node.children:
            self.visit(child)

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
        self.load_functions(self.tree)
        self.visit(self.tree)
