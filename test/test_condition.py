"""Test: condition."""

import pytest

from gibica.types import Int


@pytest.mark.parametrize('input, expected', [
    ("""
     let _condition = 3;
     let mut container = 0;

     if _condition < 5 {
         container = 1;
     } else if _condition == 5 {
         container = 2;
     } else {
         container = 3;
     }
    """, {'_condition': Int(3), 'container': Int(1)}),
    ("""
     let _condition = 5;
     let mut container = 0;

     if _condition < 5 {
         container = 1;
     } else if _condition == 5 {
         container = 2;
     } else {
         container = 3;
     }
    """, {'_condition': Int(5), 'container': Int(2)}),
    ("""
     let _condition = 6;
     let mut container = 0;

     if _condition < 5 {
         container = 1;
     } else if _condition == 5 {
         container = 2;
     } else {
         container = 3;
     }
    """, {'_condition': Int(6), 'container': Int(3)}),
])
def test_condition_statement(evaluate, memory, input, expected):
    """Test condition statement."""
    instance = evaluate(input)

    assert instance.memory == memory(expected)
