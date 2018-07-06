"""Test: Syntax."""

import pytest

from gibica.types import Int
from gibica.exceptions import LexicalError
from gibica.exceptions import SyntaxError


@pytest.mark.parametrize('input', ['let a=2+2', 'let mut a=2-2; a=2+4'])
def test_missing_semicolon(evaluate, input):
    """Test missing semicolon."""
    with pytest.raises(SyntaxError):
        evaluate(input)


@pytest.mark.parametrize('input', ['2+2;', 'a 2;', '2 1;', '2 a;', 'a=;', 'a=toto'])
def test_invalid_statements(evaluate, input):
    """Test invalid statements."""
    with pytest.raises(SyntaxError):
        evaluate(input)


@pytest.mark.parametrize('input', ['let gibica=2!2;', 'let gibica=2$2;'])
def test_invalid_operators(evaluate, input):
    """Test invalid operators."""
    with pytest.raises(LexicalError):
        evaluate(input)


@pytest.mark.parametrize('input', ['let gibica§ =2+2;', 'let gibica& =2+2;'])
def test_invalid_variable_name(evaluate, input):
    """Test invalid variable name."""
    with pytest.raises(LexicalError):
        evaluate(input)


@pytest.mark.parametrize(
    'input, expected',
    [
        ('let a = 1; # This is a comment\n', {'a': Int(1)}),
        ('let a = 1; # This is a comment', {'a': Int(1)}),
        ('# This is a comment\n let a = 1;', {'a': Int(1)}),
    ],
)
def test_with_comments(evaluate, memory, input, expected):
    """Test a comment."""
    instance = evaluate(input)

    assert instance.memory == memory(expected)