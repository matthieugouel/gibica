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

    def visit_FuncDecl(self, node):
        """Visitor for `FuncDecl` AST node."""
        self.visit(node.body)

    def visit_Params(self, node):
        """Visitor for `Params` AST node."""
        pass

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
