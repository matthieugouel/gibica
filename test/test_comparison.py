"""Test: Comparison."""

import pytest

from gibica.types import Int, Bool
from gibica.exceptions import TypeError


@pytest.mark.parametrize('input, expected', [
    ('int a = 1; int b = 2; int c = a == b;',
        {'a': Int(1), 'b': Int(2), 'c': Bool(False)}),
    ('int a = 1; int b = 2; int c = a != b;',
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


@pytest.mark.parametrize('input', [
    'int a = true + 1;',
    'int a = true + 5;',
    'int a = false + 1;',
    'float a = true + 1.0;',
    'float a = false + 1.0;',
    'bool a = false + false;',
    'bool a = true < false;',
    'bool a = true > false;',
    'bool a = true <= false;',
    'bool a = true >= false;',
    'bool a = true == 1;',
    'bool a = false == 0;',
    'bool a = false != 0;',
    'bool a = false == 5;',
    'bool a = true != 5;',
])
def test_invalid_operation_or_comparison(evaluate, input):
    """Test invalid operation or comparison of variables."""
    with pytest.raises(TypeError):
        evaluate(input)
