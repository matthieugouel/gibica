"""Interpreter."""

from gibica.lexer import Type


#
# Program Evaluation
#

class NodeVisitor(object):
    """Postorder traversal strategy."""

    def visit(self, node):
        """Visit the right method of the child class according to the node."""
        method = 'visit_' + type(node).__name__
        return getattr(self, method, self.fallback)(node)

    def fallback(self, node):
        """Fallback if the child method doesn't exist."""
        raise Exception(f'No visit_{type(node).__name__} method.')


class Interpreter(NodeVisitor):
    """Interpreter of raw input."""

    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        """Visitor for `BinOp` AST node."""
        if node.op.type == Type.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == Type.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == Type.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == Type.DIV:
            return self.visit(node.left) // self.visit(node.right)

    def visit_UnaryOp(self, node):
        """Visitor for `UnaryOp` AST node."""
        if node.op.type == Type.PLUS:
            return +self.visit(node.right)
        elif node.op.type == Type.MINUS:
            return -self.visit(node.right)

    def visit_Num(self, node):
        """Visitor for `Num` AST node."""
        return node.value

    def interpret(self):
        """Generic entrypoint of `Interpreter` class."""
        tree = self.parser.parse()
        return self.visit(tree)
