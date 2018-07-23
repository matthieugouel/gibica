"""Interpreter module."""

from gibica import builtins
from gibica.tokens import Nature
from gibica.ast import (
    NodeVisitor,
    AST,
    FunctionDeclaration,
    IfStatement,
    WhileStatement,
    ReturnStatement,
)
from gibica.types import bind_type, NoneType, Int, Float, Bool, Function
from gibica.memory import Memory

from itertools import islice


#
# Program Evaluation
#


class Interpreter(NodeVisitor):
    """Evaluation of the parsed input."""

    def __init__(self, tree):
        """Initialization of `Interpreter` class."""
        self.tree = tree
        self.memory = Memory()

    def load_builtins(self):
        """Load the built-in functions into the scope."""
        for raw_name in dir(builtins):
            if not raw_name.startswith('__'):

                if raw_name.startswith('_'):
                    function_name = raw_name[1:]
                else:
                    function_name = raw_name

                builtin_function = Function(function_name, getattr(builtins, raw_name))
                self.memory[function_name] = builtin_function

    def load_functions(self, tree):
        """Load the functions into the scope."""
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

        return NoneType()

    def visit_FunctionCall(self, node):
        """Visitor for `FunctionCall` AST node."""
        call = self.memory[node.identifier.name]._node
        args = [self.visit(parameter) for parameter in node.parameters]

        if isinstance(call, AST):
            current_scope = self.memory.stack.current.current
            memory_functions = {
                key: current_scope[key]
                for key in current_scope
                if isinstance(current_scope[key], Function)
            }

            self.memory.append_frame()
            for i, arg in enumerate(args):
                self.memory[i] = arg

            for function in memory_functions:
                self.memory[function] = memory_functions[function]

            function_result = self.visit(call)

            self.memory.pop_frame()
            return function_result
        else:
            return bind_type(call(*args))

    def visit_VariableDeclaration(self, node):
        """Visitor for `VariableDeclaration` AST node."""
        self.visit(node.assignment)

    def visit_Assignment(self, node):
        """Visitor for `Assignment` AST node."""
        obj_memory = self.memory[node.left.identifier.name]
        obj_program = self.visit(node.right)
        if obj_memory is not None:
            obj_program_value = obj_program.value
            obj_program = obj_memory
            obj_program.value = obj_program_value

        self.memory[node.left.identifier.name] = obj_program

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
            return_value = self.visit(child)

            if isinstance(child, ReturnStatement):
                return return_value

            if isinstance(child, (IfStatement, WhileStatement)):
                if return_value is not None:
                    return return_value
        self.memory.pop_scope()

    def visit_ReturnStatement(self, node):
        """Visitor for `WhileStatement` AST node."""
        return self.visit(node.expression)

    def visit_BinaryOperation(self, node):
        """Visitor for `BinaryOperation` AST node."""
        if node.op.nature == Nature.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.nature == Nature.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.nature == Nature.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.nature == Nature.DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.nature == Nature.INT_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.nature == Nature.EQ:
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.nature == Nature.NE:
            return self.visit(node.left) != self.visit(node.right)
        elif node.op.nature == Nature.LE:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.op.nature == Nature.GE:
            return self.visit(node.left) >= self.visit(node.right)
        elif node.op.nature == Nature.LT:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.nature == Nature.GT:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.nature == Nature.OR:
            return self.visit(node.left) or self.visit(node.right)
        elif node.op.nature == Nature.AND:
            return self.visit(node.left) and self.visit(node.right)

    def visit_UnaryOperation(self, node):
        """Visitor for `UnaryOperation` AST node."""
        if node.op.nature == Nature.PLUS:
            return +self.visit(node.right)
        elif node.op.nature == Nature.MINUS:
            return -self.visit(node.right)
        elif node.op.nature == Nature.NOT:
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
        self.load_builtins()
        self.load_functions(self.tree)
        self.visit(self.tree)
