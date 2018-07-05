"""Test: loop."""

import pytest

from gibica.types import Int


@pytest.mark.parametrize('input, expected', [
    ("""
     let mut container = 0;
     while container != 4 {
        container = container + 1;
     }
    """, {'container': Int(4)}),
    ("""
     let mut container = 0;
     let mut test = 0;

     while container != 4 {
         if container == 2 {
             test = test + 1;
         }
         container = container + 1;
     }
    """, {'container': Int(4), 'test': Int(1)}),
])
def test_loop_statement(evaluate, memory, input, expected):
    """Test loop statement."""
    instance = evaluate(input)

    assert instance.memory == memory(expected)
