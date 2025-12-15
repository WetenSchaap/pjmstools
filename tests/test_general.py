import pytest
import pjmstools
import numpy as np

def test_flatten() -> None:
    assert pjmstools.flatten(
        [
            [1,2,3],
            [6,5,4],
            [0,0,0,0,0,0,0,0],
            ["oi","you","bastard"]
        ]
    ) == [1,2,3,6,5,4,0,0,0,0,0,0,0,0,"oi","you","bastard"]

def test_transform_coordinate_system() -> None:
    # TODO: Actually include assert (with fuzzy matching to account for 1e-16 values you get often)
    start = np.array((1,1))
    end = np.array((5,4))
    # this combination is nice since they are exactly 5 points from each other
    tests = [
        start,
        end,
        (3,2.5), # halfway point
        (5,4),
        (0,0),
        (3,4)
    ]

    start_ed = pjmstools.transform_coordinate_system(
        pjmstools.unit_vector(end - start), start, tests
    )
    print(start_ed)
