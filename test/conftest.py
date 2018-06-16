"""Configuration of tests."""
import pytest

from gibica.lexer import Lexer
from gibica.parser import Parser
from gibica.interpreter import SymbolTableBuilder
from gibica.interpreter import Interpreter


@pytest.fixture
def evaluate():
    """Interpret a raw input."""

    def nested(raw):

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

        # Return the instance
        return interpreter

    return nested
