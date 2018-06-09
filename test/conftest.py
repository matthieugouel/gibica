"""Configuration of tests."""
import pytest

from gibica.lexer import Lexer
from gibica.parser import Parser
from gibica.interpreter import Interpreter


@pytest.fixture
def evaluate():
    """Interpret a raw input."""

    def nested(raw):

        # Instantiate the interpreter
        lexer = Lexer(raw)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)

        # Evaluate the input
        interpreter.interpret()

        # Return the instance
        return interpreter

    return nested
