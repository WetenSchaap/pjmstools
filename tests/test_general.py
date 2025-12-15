import pytest
import pjmstools
import numpy as np
import matplotlib.pyplot as plt


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
    tests = np.array([
        start,
        end,
        (3,2.5), # halfway point
        (-3,4),  # straight up from start in new coordinate system
        (0,5),   # Corner point that should form a square with two points above.
    ])

    start_ed = pjmstools.transform_coordinate_system(
        pjmstools.unit_vector(end - start), start, tests
    )
    print(start_ed)
    fig,ax = plt.subplots(1,1)
    ax.plot((start[0],end[0]),(start[1],end[1]), color="black")
    ax.scatter(tests[:,0],tests[:,1],c="red")
    ax.scatter(start_ed[:,0], start_ed[:,1],c="green")
