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


class Compound(AST):
    """Compound AST representation."""

    def __init__(self):
        """Initialization of `Compound` class."""
        self.children = []


class VarDecl(AST):
    """Variable declaration AST representation."""

    def __init__(self, var_type, assignment):
        """Initialization of `VarDecl` class."""
        self.var_type = var_type
        self.assignment = assignment


class VarType(AST):
    """Variable Type AST representation."""

    def __init__(self, token):
        """Initialization of `VarType` class."""
        self.token = token
        self.value = token.value


class Assign(AST):
    """Assignment AST representation."""

    def __init__(self, left, op, right):
        """Initialization of `Assign` class."""
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    """Variable AST representation."""

    def __init__(self, token, is_mutable):
        """Initialization of `Var` class."""
        self.token = token
        self.value = token.value
        self.is_mutable = is_mutable


class IfStatement(AST):
    """If statement AST representation."""

    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body


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
