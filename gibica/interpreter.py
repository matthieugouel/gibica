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
        raise Exception(f'INTERPRETER: No visit_{type(node).__name__} method.')


class Interpreter(NodeVisitor):
    """Interpreter of raw input."""

    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}

    def visit_Compound(self, node):
        """Visitor for `Compound` AST node."""
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        """Visitor for `Compound` AST node."""
        self.GLOBAL_SCOPE[node.left.value] = self.visit(node.right)

    def visit_Var(self, node):
        """Visitor for `Compound` AST node."""
        variable_name = node.value
        variable_value = self.GLOBAL_SCOPE.get(variable_name)
        if variable_value is None:
            raise Exception(
                f'INTERPRETER: Unassigned variable `{variable_name}`.'
            )
        else:
            return variable_value

    def visit_BinOp(self, node):
        """Visitor for `BinOp` AST node."""
        if node.op.type == Type.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == Type.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == Type.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == Type.DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == Type.INT_DIV:
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
        if tree is None:
            return ''
        return self.visit(tree)
