"""Test: expression."""

import pytest

from gibica.types import Int, Bool
from gibica.exceptions import SyntaxError, TypeError, LexicalError


@pytest.mark.parametrize(
    'input, expected',
    [
        (
            'let a = 1; let b = 2; let c = a == b;',
            {'a': Int(1), 'b': Int(2), 'c': Bool(False)},
        ),
        (
            'let a = 1; let b = 2; let c = a != b;',
            {'a': Int(1), 'b': Int(2), 'c': Bool(True)},
        ),
        (
            'let a = 1; let b = 2; let c = a <= b;',
            {'a': Int(1), 'b': Int(2), 'c': Bool(True)},
        ),
        (
            'let a = 1; let b = 2; let c = a >= b;',
            {'a': Int(1), 'b': Int(2), 'c': Bool(False)},
        ),
        (
            'let a = 1; let b = 2; let c = a < b;',
            {'a': Int(1), 'b': Int(2), 'c': Bool(True)},
        ),
        (
            'let a = 1; let b = 2; let c = a > b;',
            {'a': Int(1), 'b': Int(2), 'c': Bool(False)},
        ),
    ],
)
def test_expression_comparison(evaluate, memory, input, expected):
    """Test expression comparison."""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize(
    'input',
    [
        'let a = true + 1;',
        'let a = true + 5;',
        'let a = false + 1;',
        'let a = true + 1.0;',
        'let a = false + 1.0;',
        'let a = false + false;',
        'let a = true < false;',
        'let a = true > false;',
        'let a = true <= false;',
        'let a = true >= false;',
        'let a = true == 1;',
        'let a = false == 0;',
        'let a = false != 0;',
        'let a = false == 5;',
        'let a = true != 5;',
    ],
)
def test_invalid_operation_or_comparison(evaluate, input):
    """Test invalid operation or comparison of variables."""
    with pytest.raises(TypeError):
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
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize('input', ['let a = 1/0;', 'let a = 1//0;'])
def test_zero_division_error(evaluate, input):
    """Test a division by zero."""
    with pytest.raises(TypeError):
        evaluate(input, skip_builtins=True)


@pytest.mark.parametrize('input', ['2+2;', 'a 2;', '2 1;', '2 a;', 'a=;', 'a=toto'])
def test_invalid_statements(evaluate, input):
    """Test invalid statements."""
    with pytest.raises(SyntaxError):
        evaluate(input, skip_builtins=True)


@pytest.mark.parametrize('input', ['let a=2+2', 'let mut a=2-2; a=2+4'])
def test_missing_semicolon(evaluate, input):
    """Test missing semicolon."""
    with pytest.raises(SyntaxError):
        evaluate(input, skip_builtins=True)


@pytest.mark.parametrize('input', ['let gibica=2!2;', 'let gibica=2$2;'])
def test_invalid_operators(evaluate, input):
    """Test invalid operators."""
    with pytest.raises(LexicalError):
        evaluate(input, skip_builtins=True)
