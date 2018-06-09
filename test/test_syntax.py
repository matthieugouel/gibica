"""Test: Syntax."""
import pytest


@pytest.mark.parametrize('input', [
    'a=2+2',
    'a=2-2;a=2+4',
])
def test_missing_semicolon(evaluate, input):
    """Test missing semicolon."""
    with pytest.raises(Exception):
        evaluate(input)


@pytest.mark.parametrize('input', [
    '2+2;',
    'a 2;',
    '2 1;',
    '2 a;',
    'a=;',
    'a=toto',
])
def test_invalid_statements(evaluate, input):
    """Test invalid statements."""
    with pytest.raises(Exception):
        evaluate(input)


@pytest.mark.parametrize('input', [
    'gibica=2!2;',
    'gibica=2$2;',
])
def test_invalid_operators(evaluate, input):
    """Test invalid operators"""
    with pytest.raises(Exception):
        evaluate(input)


@pytest.mark.parametrize('input', [
    'gibica* =2+2;',
    'gibica& =2+2;',
])
def test_invalid_variable_name(evaluate, input):
    """Test invalid variable name"""
    with pytest.raises(Exception):
        evaluate(input)
