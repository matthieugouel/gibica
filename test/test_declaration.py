"""Test: declaration."""

import pytest

from gibica.types import Int, Float, Bool
from gibica.exceptions import SementicError


@pytest.mark.parametrize('input, expected', [
    ('int a=4;', {'a': Int(4)}),
    ('int a=10;', {'a': Int(10)}),
    ('int a = 115;', {'a': Int(115)}),
    ('int a = 2 + 2;', {'a': Int(4)}),
    ('int a = 2 - 2;', {'a': Int(0)}),
    ('int a = 2 * 2;', {'a': Int(4)}),
    ('float a = 2 / 2;', {'a': Float(1.0)}),
    ('int a = 2 // 2;', {'a': Int(1)}),
    ('int a = 3 // 2;', {'a': Int(1)}),

    ('int gibica = 2;', {'gibica': Int(2)}),
    ('int GIBICA = 2 + 4;', {'GIBICA': Int(6)}),
    ('int GiBiCa = 1;', {'GiBiCa': Int(1)}),
    ('int gibica1 = 2;', {'gibica1': Int(2)}),

    ('int _gibica = 2;', {'_gibica': Int(2)}),
    ('int __gibica = 2;', {'__gibica': Int(2)}),
    ('int _gibi_ca = 2;', {'_gibi_ca': Int(2)}),
])
def test_int_declaration(evaluate, input, expected):
    """Test `int` type variable declaration."""
    instance = evaluate(input)

    assert instance.GLOBAL_MEMORY == expected


@pytest.mark.parametrize('input, expected', [
    ('float a = 3 / 2;', {'a': Float(1.5)}),
    ('float a = 1.5 + 2.5;', {'a': Float(4.0)}),
    ('float a = 1.5 + 2;', {'a': Float(3.5)}),
])
def test_float_declaration(evaluate, input, expected):
    """Test `float` type variable declaration."""
    instance = evaluate(input)

    assert instance.GLOBAL_MEMORY == expected


@pytest.mark.parametrize('input, expected', [
    ('bool a = true;', {'a': Bool(True)}),
    ('bool a = true == true;', {'a': Bool(True)}),
    ('bool a = true != true;', {'a': Bool(False)}),
    ('bool a = true != false;', {'a': Bool(True)}),
    ('bool a = false == false;', {'a': Bool(True)}),
    ('bool a = true == false;', {'a': Bool(False)}),
    ('bool a = true == ( 1 < 2 ) ;', {'a': Bool(True)}),
    ('bool a = true == ( 5 == 5 ) ;', {'a': Bool(True)}),
    ('bool a = false == ( 1 < 2 ) ;', {'a': Bool(False)}),
    ('bool a = true and false;', {'a': Bool(False)}),
    ('bool a = true or false;', {'a': Bool(True)}),
    ('bool a = not false;', {'a': Bool(True)}),
])
def test_bool_declaration(evaluate, input, expected):
    """Test `Bool` type variable declaration."""
    instance = evaluate(input)

    assert instance.GLOBAL_MEMORY == expected


@pytest.mark.parametrize('input, expected', [
    ('int a = (2 + 2) * 2;', {'a': Int(8)}),
    ('int a = (( 2+2 ) *2) / 2;', {'a': Int(4)}),
])
def test_declaration_with_parenthesis(evaluate, input, expected):
    """Test variable declaration with parenthesis."""
    instance = evaluate(input)

    assert instance.GLOBAL_MEMORY == expected


@pytest.mark.parametrize('input, expected', [
    ('int a = -2;', {'a': Int(-2)}),
    ('int a = +3;', {'a': Int(3)}),
    ('int a = (((-4)));', {'a': Int(-4)}),
    ('int a = ((+10));', {'a': Int(10)}),
])
def test_unary_declaration(evaluate, input, expected):
    """Test unary variable declaration."""
    instance = evaluate(input)

    assert instance.GLOBAL_MEMORY == expected


@pytest.mark.parametrize('input, expected', [
    ('int a=2+2; int b=4*2;', {'a': Int(4), 'b': Int(8)}),
    ('int a=2+2; int b=a*2;', {'a': Int(4), 'b': Int(8)}),
])
def test_multiple_declarations(evaluate, input, expected):
    """Test multiple variable declarations."""
    instance = evaluate(input)

    assert instance.GLOBAL_MEMORY == expected


@pytest.mark.parametrize('input, expected', [
    ('int mut a=2+2; int b=4*2;', {'a': Int(4), 'b': Int(8)}),
    ('int a=2+2; int mut b=a*2;', {'a': Int(4), 'b': Int(8)}),
    ('int mut a=1; a=2;', {'a': Int(2)}),
    ('int mut a=1; a=a+1;', {'a': Int(2)}),
])
def test_mutable_declaration(evaluate, input, expected):
    """Test mutable variable declaration."""
    instance = evaluate(input)

    assert instance.GLOBAL_MEMORY == expected


@pytest.mark.parametrize('input', [
    'int a = 1; a = 2;',
])
def test_reassignment_of_immutable_variable(evaluate, input):
    """Test re-assignment of immutable variable."""
    with pytest.raises(SementicError):
        evaluate(input)
