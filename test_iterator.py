import pytest
from iterator import FlatIterator

@pytest.mark.parametrize(
    "input_list, expected_output",
    [
        ([], []),
        ([[]], []),
        ([[], [], []], []),
        ([[1, 2, 3]], [1, 2, 3]),
        (
            [
                ['a', 'b', 'c'],
                ['d', 'e', 'f', 'h', False],
                [1, 2, None]
            ],
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
        ),
        (
            [[1, 'a', True], [None, 3.14, False]],
            [1, 'a', True, None, 3.14, False]
        ),
    ]
)
def test_flat_iterator(input_list, expected_output):
    assert list(FlatIterator(input_list)) == expected_output