"""Test: condition."""

import pytest

from gibica.types import Int


@pytest.mark.parametrize('input, expected', [
    ("""
     bool _condition = 3;
     int mut container = 0;

     if _condition < 5 {
         container = 1;
     } else if _condition == 5 {
         container = 2;
     } else {
         container = 3;
     }
    """, {'_condition': Int(3), 'container': Int(1)}),
    ("""
     bool _condition = 5;
     int mut container = 0;

     if _condition < 5 {
         container = 1;
     } else if _condition == 5 {
         container = 2;
     } else {
         container = 3;
     }
    """, {'_condition': Int(5), 'container': Int(2)}),
    ("""
     bool _condition = 6;
     int mut container = 0;

     if _condition < 5 {
         container = 1;
     } else if _condition == 5 {
         container = 2;
     } else {
         container = 3;
     }
    """, {'_condition': Int(6), 'container': Int(3)}),
])
def test_expression_comparison(evaluate, input, expected):
    """Test expression comparison."""
    instance = evaluate(input)

    assert instance.GLOBAL_MEMORY == expected
