"""Test: condition."""

import pytest

from gibica.types import Bool, Int


@pytest.mark.parametrize('input, expected', [
    ("""
     bool _condition = true;
     int mut container = 0;

     if _condition {
         container = 1;
     } else {
         container = 2;
     }
    """, {'_condition': Bool(True), 'container': Int(1)}),
    ("""
     bool _condition = false;
     int mut container = 0;

     if _condition {
         container = 1;
     } else {
         container = 2;
     }
    """, {'_condition': Bool(False), 'container': Int(2)}),
])
def test_expression_comparison(evaluate, input, expected):
    """Test expression comparison."""
    instance = evaluate(input)

    assert instance.GLOBAL_MEMORY == expected
