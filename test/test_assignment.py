"""Test: assignment."""
import pytest


@pytest.mark.parametrize('input, expected', [
    ('a=4;', {'a': 4}),
    ('a=10;', {'a': 10}),
    ('a=2+2;', {'a': 4}),
    ('a=2-2;', {'a': 0}),
    ('a=2*2;', {'a': 4}),
    ('a=2/2;', {'a': 1}),

    ('gibica=2;', {'gibica': 2}),
    ('GIBICA=2+4;', {'GIBICA': 6}),
    ('GiBiCa=1;', {'GiBiCa': 1}),
    ('gibica1=2;', {'gibica1': 2}),
])
def test_simple_assignments(evaluate, input, expected):
    """Test simple variable assignments."""
    instance = evaluate(input)

    assert instance.GLOBAL_SCOPE == expected


@pytest.mark.parametrize('input, expected', [
    ('a=2 + 2;', {'a': 4}),
    ('a=2 /   2 ;', {'a': 1}),
])
def test_assignments_with_whitespaces(evaluate, input, expected):
    """Test variable assignments with whitespaces."""
    instance = evaluate(input)

    assert instance.GLOBAL_SCOPE == expected


@pytest.mark.parametrize('input, expected', [
    ('a=(2+2)*2;', {'a': 8}),
    ('a=((2+2)*2)/2;', {'a': 4}),
])
def test_assignments_with_parenthesis(evaluate, input, expected):
    """Test variable assignments with parenthesis."""
    instance = evaluate(input)

    assert instance.GLOBAL_SCOPE == expected


@pytest.mark.parametrize('input, expected', [
    ('a=-2;', {'a': -2}),
    ('a=+3;', {'a': 3}),
    ('a=(((-4)));', {'a': -4}),
    ('a=((+10));', {'a': 10}),
])
def test_unary_assignments(evaluate, input, expected):
    """Test unary variable assignments."""
    instance = evaluate(input)

    assert instance.GLOBAL_SCOPE == expected


@pytest.mark.parametrize('input, expected', [
    ('a=2+2;b=4*2;', {'a': 4, 'b': 8}),
    ('a=2+2;b=a*2;', {'a': 4, 'b': 8}),
])
def test_multiple_assignments(evaluate, input, expected):
    """Test multiple variable assignments."""
    instance = evaluate(input)

    assert instance.GLOBAL_SCOPE == expected
