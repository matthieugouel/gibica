"""Test: Symbol table."""
import pytest


@pytest.mark.parametrize('input', [
    'int a = 1; b = a + 1;',
    'int a = 1; a = 1 + b;',
])
def test_assignment_before_declaration(evaluate, input):
    """Test assignment before declaration."""
    with pytest.raises(Exception):
        evaluate(input)
