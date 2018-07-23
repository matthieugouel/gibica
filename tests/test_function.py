"""Test: function."""

import pytest

from gibica.types import Int, Bool, NoneType, Function
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
        def func(n) {
            return 1;
        }

        let n = 1;
        let result = func(n);
    """,
            {'func': Function('func'), 'n': Int(1), 'result': Int(1)},
        ),
        (
            """
        def func(a, b) {
            return a + b;
        }

        let result = func(1, 1);
    """,
            {'func': Function('func'), 'result': Int(2)},
        ),
        (
            """
        def func(mut n) {
            n = n + 1;
            return n;
        }

        let result = func(1);
    """,
            {'func': Function('func'), 'result': Int(2)},
        ),
        (
            """
        def func(mut n) {
            return n;
        }

        let result = func(1 > 2);
    """,
            {'func': Function('func'), 'result': Bool(False)},
        ),
        (
            """
        def func(n) {
            return n;
        }

        let result = func(true or false);
    """,
            {'func': Function('func'), 'result': Bool(True)},
        ),
        (
            """
        def func(n) {
            return n+1;
        }

        let result = func(func(1));
    """,
            {'func': Function('func'), 'result': Int(3)},
        ),
    ],
)
def test_simple_function_call(evaluate, memory, input, expected):
    """Test simple function call."""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize(
    'input, expected',
    [
        (
            """
        def func(n) {
            if n < 2 {
                return 1;
            }
            else if n < 4 {
                return 2;
            }
            else {
                return 3;
            }
        }

        let result = func(1);
    """,
            {'func': Function('func'), 'result': Int(1)},
        ),
        (
            """
        def func(n) {
            if n < 2 {
                return 1;
            }
            else if n < 4 {
                return 2;
            }
            else {
                return 3;
            }
        }

        let result = func(3);
    """,
            {'func': Function('func'), 'result': Int(2)},
        ),
        (
            """
        def func(n) {
            if n < 2 {
                return 1;
            }
            else if n < 4 {
                return 2;
            }
            else {
                return 3;
            }
        }

        let result = func(5);
    """,
            {'func': Function('func'), 'result': Int(3)},
        ),
    ],
)
def test_return_in_compound_statement(evaluate, memory, input, expected):
    """Test simple function call."""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize(
    'input, expected',
    [
        (
            """
        def zero() {
            let mut i = 5;
            while i != 0 {
                return 0;
                i = i-1;
            }
            return 1;
        }

        let result = zero();
        """,
            {'zero': Function('zero'), 'result': Int(0)},
        )
    ],
)
def test_function_return_in_while(evaluate, memory, input, expected):
    """Test a function with a return in a while."""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize(
    'input, expected',
    [
        (
            """
        def function(n) {
            let mut i = 0;
            while i < n {
                if i == 2 {
                    return i + 2;
                }
                i = i + 1;
            }
            return 0;
        }
        let result = function(5);
        """,
            {'function': Function('function'), 'result': Int(4)},
        )
    ],
)
def test_function_return_in_if_in_while(evaluate, memory, input, expected):
    """Test a function with a return in a if in a while."""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize(
    'input, expected',
    [
        (
            """
        def function(n) {
            let mut i = 0;
            if n == 5 {
                while i < 5 {
                    return 2;
                }
            }
            return 0;
        }
        let result = function(5);
        """,
            {'function': Function('function'), 'result': Int(2)},
        )
    ],
)
def test_function_return_in_while_in_if(evaluate, memory, input, expected):
    """Test a function with a return in while in a if."""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize(
    'input, expected',
    [
        (
            """
        let result = zero(3);

        def zero(n) {

            return 0;
        }

        """,
            {'zero': Function('zero'), 'result': Int(0)},
        )
    ],
)
def test_function_declared_after_call(evaluate, memory, input, expected):
    """Test function a function declared after its call."""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize(
    'input, expected',
    [
        (
            """
        def null() {
            let a = 1;
        }

        let result = null();
        """,
            {'null': Function('null'), 'result': NoneType()},
        )
    ],
)
def test_function_with_no_return(evaluate, memory, input, expected):
    """Test a function with no return"""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize(
    'input, expected',
    [
        (
            """
        def recursive(n) {
            if n < 1 {
                return 1;
            }

            return recursive(n-1);

        }

        let result = recursive(3);
        """,
            {'recursive': Function('recursive'), 'result': Int(1)},
        )
    ],
)
def test_recursive_function(evaluate, memory, input, expected):
    """Test a recursive function."""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize('input, expected', [("", {'print': Function('print')})])
def test_only_builtins(evaluate, memory, input, expected):
    """Test a program with only builtins functions."""
    instance = evaluate(input, skip_builtins=False)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize(
    'input, expected',
    [
        (
            """
        let result = print(1);
        """,
            {'result': NoneType()},
        )
    ],
)
def test_nonetype_function(evaluate, memory, input, expected):
    """Test a NoneType builtin function."""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize('input', ['let result = zero();'])
def test_function_not_declared(evaluate, input):
    """Test the call of an undeclared function."""
    with pytest.raises(SementicError):
        evaluate(input, skip_builtins=True)


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
    ],
)
def test_function_already_declared(evaluate, input):
    """Test a function already declared."""
    with pytest.raises(SementicError):
        evaluate(input, skip_builtins=True)


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
    ],
)
def test_function_same_parameters(evaluate, input):
    """Test a function which has two same parameters."""
    with pytest.raises(SementicError):
        evaluate(input, skip_builtins=True)


@pytest.mark.parametrize(
    'input',
    [
        """
        def func(n) {
            n = n + 1;
            return n;
        }

        let n = 1;
        let result = func(n);
    """
    ],
)
def test_redefinition_non_mutable_parameter(evaluate, input):
    """Test the redefinition of a non mutable parameter."""
    with pytest.raises(SementicError):
        evaluate(input, skip_builtins=True)


@pytest.mark.parametrize(
    'input',
    [
        """
        def func(8) {
            n = n + 1;
            return n;
        }

        let result = func(1);
    """,
        """
        def func(false or true) {
            return n;
        }

        let result = func(1);
    """,
        """
        def func(1 < 2) {
            return n;
        }

        let result = func(1);
    """,
        """
        def func(func(2)) {
            return n;
        }

        let result = func(1);
    """,
    ],
)
def test_invalid_function_parameter(evaluate, input):
    """Test an invalid function parameter."""
    with pytest.raises(SementicError):
        evaluate(input, skip_builtins=True)
