"""Configuration of tests."""
import pytest

from gibica.lexer.lexer import Lexer
from gibica.parser.parser import Parser
from gibica.sementic.symbol import SymbolTableBuilder
from gibica.interpreter.interpreter import Interpreter


@pytest.fixture
def evaluate():
    """Interpret a raw input."""

    def nested(raw):
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

        # Return the instance
        return interpreter

    return nested
