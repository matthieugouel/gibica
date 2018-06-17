"""Test: Comparison."""
import pytest


@pytest.mark.parametrize('input, expected', [
    ('int a = 1; int b = 2; int c = a == b;', {'a': 1, 'b': 2, 'c': False}),
    ('int a = 1; int b = 2; int c = a <= b;', {'a': 1, 'b': 2, 'c': True}),
    ('int a = 1; int b = 2; int c = a >= b;', {'a': 1, 'b': 2, 'c': False}),
    ('int a = 1; int b = 2; int c = a < b;', {'a': 1, 'b': 2, 'c': True}),
    ('int a = 1; int b = 2; int c = a > b;', {'a': 1, 'b': 2, 'c': False}),
])
def test_expression_comparison(evaluate, input, expected):
    """Test expression comparison."""
    instance = evaluate(input)

    assert instance.GLOBAL_MEMORY == expected
