"""Interpreter module."""

from gibica.lexer.token import Name


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
        self.visit(self.tree)
