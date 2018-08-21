"""AST module."""


class NodeVisitor(object):
    """AST post-order traversal strategy."""

    def visit(self, node):
        """Visit the right method of the child class according to the node."""
        method = 'visit_' + type(node).__name__
        return getattr(self, method, self.fallback)(node)

    def fallback(self, node):
        """Fallback if the child method doesn't exist."""
        raise Exception((f"INTERPRETER ERROR: No visit_{type(node).__name__} method."))


class AST(object):
    """Parent class of all AST classes."""

    pass


class Program(AST):
    """Program AST representation."""

    def __init__(self):
        """Initialization of `Program` class."""
        self.children = []


class FunctionDeclaration(AST):
    """Function declaration AST representation."""

    def __init__(self, identifier, parameters, body):
        """Initialization of `FunctionDeclaration` class."""
        self.identifier = identifier
        self.parameters = parameters
        self.body = body

    def __str__(self):
        """String representation of a `FunctionDeclaration` node."""
        return "{id}({param})".format(
            id=self.identifier,
            param=','.join(str(parameter) for parameter in self.parameters),
        )

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()  # pragma: no cover


class Parameters(AST):
    """Parameters declaration AST representation."""

    def __init__(self, variable):
        """Initialization of `Parameters` class."""
        self.variable = variable

    def __str__(self):
        """String representation of a `Parameters` node."""
        return f"{str(self.variable)}"

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()  # pragma: no cover


class FunctionBody(AST):
    """Function body AST representation."""

    def __init__(self):
        """Initialization of `FunctionBody` class."""
        self.children = []


class FunctionCall(AST):
    """Function call AST representation."""

    def __init__(self, identifier, parameters):
        """Initialization of `FunctionCall` class."""
        self.identifier = identifier
        self.parameters = parameters


class VariableDeclaration(AST):
    """Variable declaration AST representation."""

    def __init__(self, assignment):
        """Initialization of `VariableDeclaration` class."""
        self.assignment = assignment


class Assignment(AST):
    """Assignment AST representation."""

    def __init__(self, left, op, right):
        """Initialization of `Assignment` class."""
        self.left = left
        self.token = self.op = op
        self.right = right


class Variable(AST):
    """Variable AST representation."""

    def __init__(self, identifier, is_mutable):
        """Initialization of `Variable` class."""
        self.identifier = identifier
        self.is_mutable = is_mutable

    def __str__(self):
        """String representation of a `Variable` node."""
        return f"{str(self.identifier)}"

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()  # pragma: no cover


class IfStatement(AST):
    """If statement AST representation."""

    def __init__(self, if_compound, else_if_compounds=None, else_compound=None):
        """Initialization of `IfStatement` class."""
        self.if_compound = if_compound
        if else_if_compounds is None:
            self.else_if_compounds = []
        else:
            self.else_if_compounds = else_if_compounds
        self.else_compound = else_compound


class WhileStatement(AST):
    """While statement AST representation."""

    def __init__(self, condition, compound):
        """Initialization of `WhileStatement` class."""
        self.condition = condition
        self.compound = compound


class Compound(AST):
    """Compound AST representation."""

    def __init__(self):
        """Initialization of `Compound` class."""
        self.children = []


class BinaryOperation(AST):
    """Binary operands AST representation."""

    def __init__(self, left, op, right):
        """Initialization of `BinaryOperation` class."""
        self.left = left
        self.op = self.token = op
        self.right = right


class UnaryOperation(AST):
    """Unary oprerands AST representation."""

    def __init__(self, op, right):
        """Initialization of `UnaryOperation` class."""
        self.op = self.token = op
        self.right = right


class ReturnStatement(AST):
    """Return statement AST representation."""

    def __init__(self, expression):
        """Initialization of `ReturnStatement` class."""
        self.expression = expression


class Identifier(AST):
    """Identifier AST representation."""

    def __init__(self, name):
        """Initialization of `Identifier` class."""
        self.name = name

    def __str__(self):
        """String representation of a `Identifier` node."""
        return f"{str(self.name)}"

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()  # pragma: no cover


class Integer(AST):
    """Integer number AST representation."""

    def __init__(self, token):
        """Initialization of `Integer` class."""
        self.token = token
        self.value = token.value


class FloatingPoint(AST):
    """Floating point number AST representation."""

    def __init__(self, token):
        """Initialization of `FloatingPoint` class."""
        self.token = token
        self.value = token.value


class Boolean(AST):
    """Boolean AST representation."""

    def __init__(self, token):
        """Initialization of `Boolean` class."""
        self.token = token
        self.value = token.value
