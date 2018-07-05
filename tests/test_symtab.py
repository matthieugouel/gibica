"""Test: Symbol table."""

import pytest

from gibica.exceptions import SementicError


@pytest.mark.parametrize('input', [
    'let a = 1; b = a + 1;',
    'let a = 1; a = 1 + b;',
])
def test_assignment_before_declaration(evaluate, input):
    """Test assignment before declaration."""
    with pytest.raises(SementicError):
        evaluate(input)


@pytest.mark.parametrize('input', [
    'let a = 1; let a = 2;',
])
def test_redefinition_of_variable(evaluate, input):
    """Test redefinition of a variable."""
    with pytest.raises(SementicError):
        evaluate(input)
