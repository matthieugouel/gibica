"""Test: function."""

import pytest

from gibica.types import Int, Function
from gibica.exceptions import SementicError


@pytest.mark.parametrize(
    'input, expected',
    [
        (
            """
        def zero() {
            return 0;
        }

        let result = zero();
    """,
            {'zero': Function('zero'), 'result': Int(0)},
        ),
        (
            """
        def zero(n) {
            return 1;
        }

        let n = 1;
        let result = zero(n);
    """,
            {'zero': Function('zero'), 'n': Int(1), 'result': Int(1)},
        ),
        (
            """
        def zero(a, b) {
            return a + b;
        }

        let n = 1;
        let m = 1;
        let result = zero(n, m);
    """,
            {'zero': Function('zero'), 'n': Int(1), 'm': Int(1), 'result': Int(2)},
        ),
        (
            """
        def zero(mut n) {
            n = n + 1;
            return n;
        }

        let n = 1;
        let result = zero(n);
    """,
            {'zero': Function('zero'), 'n': Int(1), 'result': Int(2)},
        ),
    ],
)
def test_simple_function_call(evaluate, memory, input, expected):
    """Test simple function call."""
    instance = evaluate(input)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize('input', ['let result = zero();'])
def test_function_not_declared(evaluate, input):
    """Test the call of an undeclared function."""
    with pytest.raises(SementicError):
        evaluate(input)


@pytest.mark.parametrize(
    'input',
    [
        """
    def zero() {
        return 0;
    }

    def zero() {
        return 1;
    }

    let n = 1;
    let m = 1;
    let result = zero();
    """
    ]
)
def test_function_already_declared(evaluate, input):
    """Test a function already declared."""
    with pytest.raises(SementicError):
        evaluate(input)


@pytest.mark.parametrize(
    'input',
    [
        """
    def zero(n, n) {
        return 0;
    }


    let n = 1;
    let m = 1;
    let result = zero(n, m);
    """
    ]
)
def test_function_same_parameters(evaluate, input):
    """Test a function which has two same parameters."""
    with pytest.raises(SementicError):
        evaluate(input)


@pytest.mark.parametrize(
    'input',
    [
        """
        def zero(n) {
            n = n + 1;
            return n;
        }

        let n = 1;
        let result = zero(n);
    """
    ]
)
def test_redefinition_non_mutable_parameter(evaluate, input):
    """Test the redefinition of a non mutable parameter."""
    with pytest.raises(SementicError):
        evaluate(input)