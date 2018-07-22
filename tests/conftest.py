"""Configuration of tests."""

import pytest

from gibica.lexer import Lexer
from gibica.parser import Parser
from gibica.ast import AST
from gibica.sementic import SymbolTableBuilder
from gibica.memory import Memory
from gibica.interpreter import Interpreter
from gibica.exceptions import ObjectError


@pytest.fixture
def evaluate():
    """Interpret a raw input."""

    def nested(raw, skip_builtins=False):
        """Actual processing."""

        # Lexical analysis
        lexer = Lexer(raw)

        # Syntax analysis
        parser = Parser(lexer)
        tree = parser.parse()

        # Sementic analysis
        symtab_builder = SymbolTableBuilder(tree)
        symtab_builder.build()

        # Program evaluation
        interpreter = Interpreter(tree)
        interpreter.interpret()

        # Skip built-in functions in the memory
        memory_without_builtins = dict()
        if skip_builtins:
            for obj in interpreter.memory:
                try:
                    if isinstance(interpreter.memory[obj]._node, AST):
                        memory_without_builtins[obj] = interpreter.memory[obj]
                except ObjectError:
                    memory_without_builtins[obj] = interpreter.memory[obj]
            interpreter.memory = Memory(**memory_without_builtins)

        # Return the instance
        return interpreter

    return nested


@pytest.fixture
def memory():
    """Provide the memory structure."""

    def nested(scope):
        """Actual processing."""
        return Memory(**scope)

    return nested
