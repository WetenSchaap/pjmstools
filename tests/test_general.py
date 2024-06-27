import pytest
import pjmstools

def test_flatten():
    assert pjmstools.flatten(
        [
            [1,2,3],
            [6,5,4],
            [0,0,0,0,0,0,0,0],
            ["oi","you","bastard"]
        ]
    ) == [1,2,3,6,5,4,0,0,0,0,0,0,0,0,"oi","you","bastard"]