"""Test: Comparison."""

import pytest

from gibica.types import Int, Bool
from gibica.exceptions import TypeError


@pytest.mark.parametrize('input, expected', [
    ('let a = 1; let b = 2; let c = a == b;',
        {'a': Int(1), 'b': Int(2), 'c': Bool(False)}),
    ('let a = 1; let b = 2; let c = a != b;',
        {'a': Int(1), 'b': Int(2), 'c': Bool(True)}),
    ('let a = 1; let b = 2; let c = a <= b;',
        {'a': Int(1), 'b': Int(2), 'c': Bool(True)}),
    ('let a = 1; let b = 2; let c = a >= b;',
        {'a': Int(1), 'b': Int(2), 'c': Bool(False)}),
    ('let a = 1; let b = 2; let c = a < b;',
        {'a': Int(1), 'b': Int(2), 'c': Bool(True)}),
    ('let a = 1; let b = 2; let c = a > b;',
        {'a': Int(1), 'b': Int(2), 'c': Bool(False)}),
])
def test_expression_comparison(evaluate, input, expected):
    """Test expression comparison."""
    instance = evaluate(input)

    assert instance.GLOBAL_MEMORY == expected


@pytest.mark.parametrize('input', [
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
])
def test_invalid_operation_or_comparison(evaluate, input):
    """Test invalid operation or comparison of variables."""
    with pytest.raises(TypeError):
        evaluate(input)
