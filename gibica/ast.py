"""AST module."""


class NodeVisitor(object):
    """AST Postorder traversal strategy."""

    def visit(self, node):
        """Visit the right method of the child class according to the node."""
        method = 'visit_' + type(node).__name__
        return getattr(self, method, self.fallback)(node)

    def fallback(self, node):
        """Fallback if the child method doesn't exist."""
        raise Exception(
            (f'INTERPRETER ERROR: '
             f'No visit_{type(node).__name__} method.')
        )


class AST(object):
    """Parent class of all AST classes."""
    pass


class Program(AST):
    """Program AST representation."""

    def __init__(self):
        """Initialization of `Program` class."""
        self.children = []


class Compound(AST):
    """Compound AST representation."""

    def __init__(self):
        """Initialization of `Compound` class."""
        self.children = []


class FuncDecl(AST):
    """Function declaration AST representation."""

    def __init__(self, name, parameters, body):
        """Initialization of `FuncDecl` class."""
        self.name = name
        self.parameters = parameters
        self.body = body

    def __str__(self):
        """String representation of a `FuncDecl` node."""
        return "{name}({param})".format(
            name=self.name,
            param=','.join(
                str(parameter) for parameter in self.parameters
            )
        )

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()


class Params(AST):
    """Parameters declaration AST representation."""

    def __init__(self, variable):
        """Initialization of `Params` class."""
        self.variable = variable

    def __str__(self):
        """String representation of a `Params` node."""
        return f"{str(self.variable)}"

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()


class VarDecl(AST):
    """Variable declaration AST representation."""

    def __init__(self, assignment):
        """Initialization of `VarDecl` class."""
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

    def __init__(self, atom, is_mutable):
        """Initialization of `Var` class."""
        self.atom = atom
        self.is_mutable = is_mutable

    def __str__(self):
        """String representation of a `Var` node."""
        return f"{str(self.atom)}"

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()


class Atom(AST):
    """Atom AST representation."""

    def __init__(self, name):
        """Initialization of `Atom` class."""
        self.name = name

    def __str__(self):
        """String representation of a `Var` node."""
        return f"{str(self.name)}"

    def __repr__(self):
        """String representation of the class."""
        return self.__str__()


class IfStatement(AST):
    """If statement AST representation."""

    def __init__(self, if_compound,
                 else_if_compounds=None,
                 else_compound=None):
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


class FuncCall(AST):
    """Function call AST representation."""

    def __init__(self, name, parameters):
        """Initialization of `FuncCall` class."""
        self.name = name
        self.parameters = parameters


class ReturnStatement(AST):
    """Return statement AST representation."""

    def __init__(self, expression):
        """Initialization of `ReturnStatement` class."""
        self.expression = expression


class Integer(AST):
    """Integer AST representation."""

    def __init__(self, token):
        """Initialization of `Integer` class."""
        self.token = token
        self.value = token.value


class FloatingPoint(AST):
    """Floating Point AST representation."""

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
