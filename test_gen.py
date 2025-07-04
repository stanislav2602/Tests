import pytest
import types
from gen import flat_generator


@pytest.mark.parametrize("input_list, expected_output", [
    ([
         ['a', 'b', 'c'],
         ['d', 'e', 'f', 'h', False],
         [1, 2, None]
     ],
     ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]),

    ([[1, 2], [3, 4]], [1, 2, 3, 4]),

    ([["hello"], ["world"]], ["hello", "world"]),

    ([[], [1, 2], []], [1, 2]),
])

def test_flat_grenerator(input_list, expected_output):
    for flat_item, expected_item in zip(flat_generator(input_list), expected_output):
        assert flat_item == expected_item
    assert list(flat_generator(input_list)) == expected_output
    assert isinstance(flat_generator(input_list), types.GeneratorType)

def test_empty_input():
    assert list(flat_generator([])) == []