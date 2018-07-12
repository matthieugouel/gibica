"""Interpreter module."""

from gibica.tokens import Name
from gibica.ast import (
    NodeVisitor,
    FunctionDeclaration,
    IfStatement,
    WhileStatement,
    ReturnStatement,
)
from gibica.types import Int, Float, Bool, Function
from gibica.memory import Memory

from itertools import islice


#
# Program Evaluation
#


class Interpreter(NodeVisitor):
    """Evaluation of raw input."""

    def __init__(self, tree):
        """Initialization of `Interpreter` class."""
        self.tree = tree
        self.memory = Memory()

    def load_functions(self, tree):
        """Load the functions in the scope."""
        for child in tree.children:
            if isinstance(child, FunctionDeclaration):
                function_name = child.identifier.name
                self.memory[function_name] = Function(function_name, child)

    def visit_Program(self, node):
        """Vsitor for `Program` AST node."""
        for child in node.children:
            if not isinstance(child, FunctionDeclaration):
                self.visit(child)

    def visit_FunctionDeclaration(self, node):
        """Visitor for `FunctionDeclaration` AST node."""
        scope = self.memory.stack.current.current.copy()
        args = [parameter.variable.identifier.name for parameter in node.parameters]

        for i in islice(scope, len(args)):
            self.memory.stack.current.current.pop(i)
            self.memory[args[i]] = scope[i]

        return self.visit(node.body)

    def visit_Parameters(self, node):
        """Visitor for `Parameters` AST node."""
        return self.visit(node.variable)

    def visit_FunctionBody(self, node):
        """Visitor for `FunctionBody` AST node."""
        for child in node.children:
            return_value = self.visit(child)

            if isinstance(child, ReturnStatement):
                return return_value

            if isinstance(child, (IfStatement, WhileStatement)):
                if return_value is not None:
                    return return_value

    def visit_FunctionCall(self, node):
        """Visitor for `FunctionCall` AST node."""
        call = self.memory[node.identifier.name]._node
        if call is not None:

            args = [self.visit(parameter) for parameter in node.parameters]

            curent_scope = self.memory.stack.current.current
            memory_functions = {
                key: curent_scope[key]
                for key in curent_scope
                if isinstance(curent_scope[key], Function)
            }

            self.memory.append_frame()
            for i, arg in enumerate(args):
                self.memory[i] = arg

            for function in memory_functions:
                self.memory[function] = memory_functions[function]

            function_result = self.visit(call)

            self.memory.pop_frame()
            return function_result

    def visit_VariableDeclaration(self, node):
        """Visitor for `VariableDeclaration` AST node."""
        self.visit(node.assignment)

    def visit_Assignment(self, node):
        """Visitor for `Assignment` AST node."""
        self.memory[node.left.identifier.name] = self.visit(node.right)

    def visit_Variable(self, node):
        """Visitor for `Variable` AST node."""
        return self.visit(node.identifier)

    def visit_IfStatement(self, node):
        """Visitor for `IfStatement` AST node."""
        if_conditon, if_body = node.if_compound
        if self.visit(if_conditon):
            return self.visit(if_body)
        else:
            for else_if_compound in node.else_if_compounds:
                else_if_condition, else_if_body = else_if_compound
                if self.visit(else_if_condition):
                    result = self.visit(else_if_body)
                    if result is not None:
                        return result
                    break
            else:
                if node.else_compound is not None:
                    _, else_body = node.else_compound
                    return self.visit(else_body)

    def visit_WhileStatement(self, node):
        """Visitor for `WhileStatement` AST node."""
        while self.visit(node.condition):
            result = self.visit(node.compound)
            if result is not None:
                return result

    def visit_Compound(self, node):
        """Visitor for `Compound` AST node."""
        self.memory.append_scope()
        for child in node.children:
            if isinstance(child, ReturnStatement):
                return self.visit(child)
            self.visit(child)
        self.memory.pop_scope()

    def visit_ReturnStatement(self, node):
        """Visitor for `WhileStatement` AST node."""
        return self.visit(node.expression)

    def visit_BinaryOperation(self, node):
        """Visitor for `BinaryOperation` AST node."""
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

    def visit_UnaryOperation(self, node):
        """Visitor for `UnaryOperation` AST node."""
        if node.op.name == Name.PLUS:
            return +self.visit(node.right)
        elif node.op.name == Name.MINUS:
            return -self.visit(node.right)
        elif node.op.name == Name.NOT:
            return Bool(not self.visit(node.right))

    def visit_Identifier(self, node):
        """Visitor for `Identifier` AST node."""
        return self.memory[node.name]

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
        self.load_functions(self.tree)
        self.visit(self.tree)
