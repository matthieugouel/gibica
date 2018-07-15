"""Test: variable."""

import pytest

from gibica.types import Int, Float, Bool
from gibica.exceptions import LexicalError, SementicError


@pytest.mark.parametrize(
    'input, expected',
    [
        ('let a=4;', {'a': Int(4)}),
        ('let a=10;', {'a': Int(10)}),
        ('let a = 115;', {'a': Int(115)}),
        ('let a = 2 + 2;', {'a': Int(4)}),
        ('let a = 2 - 2;', {'a': Int(0)}),
        ('let a = 2 * 2;', {'a': Int(4)}),
        ('let a = 2 / 2;', {'a': Float(1.0)}),
        ('let a = 2 // 2;', {'a': Int(1)}),
        ('let a = 3 // 2;', {'a': Int(1)}),
        ('let gibica = 2;', {'gibica': Int(2)}),
        ('let GIBICA = 2 + 4;', {'GIBICA': Int(6)}),
        ('let GiBiCa = 1;', {'GiBiCa': Int(1)}),
        ('let gibica1 = 2;', {'gibica1': Int(2)}),
        ('let _gibica = 2;', {'_gibica': Int(2)}),
        ('let __gibica = 2;', {'__gibica': Int(2)}),
        ('let _gibi_ca = 2;', {'_gibi_ca': Int(2)}),
    ],
)
def test_int_declaration(evaluate, memory, input, expected):
    """Test `let` type variable declaration."""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize(
    'input, expected',
    [
        ('let a = 3 / 2;', {'a': Float(1.5)}),
        ('let a = 1.5 + 2.5;', {'a': Float(4.0)}),
        ('let a = 1.5 + 2;', {'a': Float(3.5)}),
    ],
)
def test_float_declaration(evaluate, memory, input, expected):
    """Test `let` type variable declaration."""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize(
    'input, expected',
    [
        ('let a = true;', {'a': Bool(True)}),
        ('let a = true == true;', {'a': Bool(True)}),
        ('let a = true != true;', {'a': Bool(False)}),
        ('let a = true != false;', {'a': Bool(True)}),
        ('let a = false == false;', {'a': Bool(True)}),
        ('let a = true == false;', {'a': Bool(False)}),
        ('let a = true == ( 1 < 2 ) ;', {'a': Bool(True)}),
        ('let a = true == ( 5 == 5 ) ;', {'a': Bool(True)}),
        ('let a = false == ( 1 < 2 ) ;', {'a': Bool(False)}),
        ('let a = true and false;', {'a': Bool(False)}),
        ('let a = true or false;', {'a': Bool(True)}),
        ('let a = not false;', {'a': Bool(True)}),
    ],
)
def test_bool_declaration(evaluate, memory, input, expected):
    """Test `Bool` type variable declaration."""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize(
    'input, expected',
    [
        ('let a = (2 + 2) * 2;', {'a': Int(8)}),
        ('let a = (( 2+2 ) *2) / 2;', {'a': Int(4)}),
    ],
)
def test_declaration_with_parenthesis(evaluate, memory, input, expected):
    """Test variable declaration with parenthesis."""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize(
    'input, expected',
    [
        ('let a = -2;', {'a': Int(-2)}),
        ('let a = +3;', {'a': Int(3)}),
        ('let a = (((-4)));', {'a': Int(-4)}),
        ('let a = ((+10));', {'a': Int(10)}),
    ],
)
def test_unary_declaration(evaluate, memory, input, expected):
    """Test unary variable declaration."""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize(
    'input, expected',
    [
        ('let a=2+2; let b=4*2;', {'a': Int(4), 'b': Int(8)}),
        ('let a=2+2; let b=a*2;', {'a': Int(4), 'b': Int(8)}),
    ],
)
def test_multiple_declarations(evaluate, memory, input, expected):
    """Test multiple variable declarations."""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize(
    'input, expected',
    [
        ('let mut a=2+2; let b=4*2;', {'a': Int(4), 'b': Int(8)}),
        ('let a=2+2; let mut b=a*2;', {'a': Int(4), 'b': Int(8)}),
        ('let mut a=1; a=2;', {'a': Int(2)}),
        ('let mut a=1; a=a+1;', {'a': Int(2)}),
    ],
)
def test_mutable_declaration(evaluate, memory, input, expected):
    """Test mutable variable declaration."""
    instance = evaluate(input, skip_builtins=True)

    assert instance.memory == memory(expected)


@pytest.mark.parametrize('input', ['let gibica§ =2+2;', 'let gibica& =2+2;'])
def test_invalid_variable_name(evaluate, input):
    """Test invalid variable name."""
    with pytest.raises(LexicalError):
        evaluate(input, skip_builtins=True)


@pytest.mark.parametrize('input', ['let a = 1; a = 2;'])
def test_reassignment_of_immutable_variable(evaluate, input):
    """Test re-assignment of immutable variable."""
    with pytest.raises(SementicError):
        evaluate(input, skip_builtins=True)


@pytest.mark.parametrize('input', ['let a = 1; b = a + 1;', 'let a = 1; a = 1 + b;'])
def test_assignment_before_declaration(evaluate, input):
    """Test assignment before declaration."""
    with pytest.raises(SementicError):
        evaluate(input, skip_builtins=True)


# Maybe it will be authorized in the future (shadowing)
@pytest.mark.parametrize('input', ['let a = 1; let a = 2;'])
def test_redefinition_of_variable(evaluate, input):
    """Test redefinition of a variable."""
    with pytest.raises(SementicError):
        evaluate(input, skip_builtins=True)
