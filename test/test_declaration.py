"""Test: declaration."""
import pytest


@pytest.mark.parametrize('input, expected', [
    ('int a=4;', {'a': 4}),
    ('int a=10;', {'a': 10}),
    ('int a = 115;', {'a': 115}),
    ('int a = 2 + 2;', {'a': 4}),
    ('int a = 2 - 2;', {'a': 0}),
    ('int a = 2 * 2;', {'a': 4}),
    ('int a = 2 / 2;', {'a': 1.0}),
    ('int a = 2 // 2;', {'a': 1}),
    ('int a = 3 // 2;', {'a': 1}),

    ('int gibica = 2;', {'gibica': 2}),
    ('int GIBICA = 2 + 4;', {'GIBICA': 6}),
    ('int GiBiCa = 1;', {'GiBiCa': 1}),
    ('int gibica1 = 2;', {'gibica1': 2}),
])
def test_int_declaration(evaluate, input, expected):
    """Test `int` type variable declaration."""
    instance = evaluate(input)

    assert instance.GLOBAL_SCOPE == expected


@pytest.mark.parametrize('input, expected', [
    ('float a = 3 / 2;', {'a': 1.5}),
    ('float a = 1.5 + 2.5;', {'a': 4.0}),
    ('float a = 1.5 + 2;', {'a': 3.5}),
])
def test_float_declaration(evaluate, input, expected):
    """Test `float` type variable declaration."""
    instance = evaluate(input)

    assert instance.GLOBAL_SCOPE == expected


@pytest.mark.parametrize('input, expected', [
    ('int a = (2 + 2) * 2;', {'a': 8}),
    ('int a = (( 2+2 ) *2) / 2;', {'a': 4}),
])
def test_declaration_with_parenthesis(evaluate, input, expected):
    """Test variable declaration with parenthesis."""
    instance = evaluate(input)

    assert instance.GLOBAL_SCOPE == expected


@pytest.mark.parametrize('input, expected', [
    ('int a = -2;', {'a': -2}),
    ('int a = +3;', {'a': 3}),
    ('int a = (((-4)));', {'a': -4}),
    ('int a = ((+10));', {'a': 10}),
])
def test_unary_declaration(evaluate, input, expected):
    """Test unary variable declaration."""
    instance = evaluate(input)

    assert instance.GLOBAL_SCOPE == expected


@pytest.mark.parametrize('input, expected', [
    ('int a=2+2; int b=4*2;', {'a': 4, 'b': 8}),
    ('int a=2+2; int b=a*2;', {'a': 4, 'b': 8}),
    ('int a=1; a=2;', {'a': 2}),
    ('int a=1; a=a+1;', {'a': 2}),
])
def test_multiple_declaration(evaluate, input, expected):
    """Test multiple variable declaration."""
    instance = evaluate(input)

    assert instance.GLOBAL_SCOPE == expected
