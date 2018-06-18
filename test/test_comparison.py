"""Test: Comparison."""

import pytest

from gibica.interpreter.type import Int, Bool


@pytest.mark.parametrize('input, expected', [
    ('int a = 1; int b = 2; int c = a == b;',
        {'a': Int(1), 'b': Int(2), 'c': Bool(True)}),
    ('int a = 1; int b = 2; int c = a <= b;',
        {'a': Int(1), 'b': Int(2), 'c': Bool(True)}),
    ('int a = 1; int b = 2; int c = a >= b;',
        {'a': Int(1), 'b': Int(2), 'c': Bool(False)}),
    ('int a = 1; int b = 2; int c = a < b;',
        {'a': Int(1), 'b': Int(2), 'c': Bool(True)}),
    ('int a = 1; int b = 2; int c = a > b;',
        {'a': Int(1), 'b': Int(2), 'c': Bool(False)}),
])
def test_expression_comparison(evaluate, input, expected):
    """Test expression comparison."""
    instance = evaluate(input)

    assert instance.GLOBAL_MEMORY == expected
