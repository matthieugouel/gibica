"""Interpreter module."""

from gibica.tokens import Name
from gibica.ast import NodeVisitor
from gibica.types import Int, Float, Bool


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

    def visit_VarType(self, node):
        """Visitor for `VarType` AST node."""
        pass

    def visit_Assign(self, node):
        """Visitor for `Assign` AST node."""
        self.GLOBAL_MEMORY[node.left.value] = self.visit(node.right)

    def visit_Var(self, node):
        """Visitor for `Var` AST node."""
        variable_name = node.value
        variable_value = self.GLOBAL_MEMORY.get(variable_name)
        return variable_value

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
        elif node.op.name == Name.EQ:
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.name == Name.NE:
            return self.visit(node.left) != self.visit(node.right)
        elif node.op.name == Name.LE:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.op.name == Name.GE:
            return self.visit(node.left) >= self.visit(node.right)
        elif node.op.name == Name.LT:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.name == Name.GT:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.name == Name.OR:
            return self.visit(node.left) or self.visit(node.right)
        elif node.op.name == Name.AND:
            return self.visit(node.left) and self.visit(node.right)

    def visit_UnaryOp(self, node):
        """Visitor for `UnaryOp` AST node."""
        if node.op.name == Name.PLUS:
            return +self.visit(node.right)
        elif node.op.name == Name.MINUS:
            return -self.visit(node.right)
        elif node.op.name == Name.NOT:
            return Bool(not self.visit(node.right))

    def visit_Integer(self, node):
        """Visitor for `Integer` AST node."""
        return Int(node.value)

    def visit_FloatingPoint(self, node):
        """Visitor for `FloatingPoint` AST node."""
        return Float(node.value)

    def visit_Boolean(self, node):
        """Visitor for `Boolean` AST node."""
        if node.value == 'true':
            return Bool(True)
        elif node.value == 'false':
            return Bool(False)

    def interpret(self):
        """Generic entrypoint of `Interpreter` class."""
        self.visit(self.tree)
