import itertools
from typing import Any
from collections.abc import Iterable
import numpy.typing as npt
import numpy as np
import collections
from .general import is_iter

def flatten(nested_list : list[list[Any]]) -> list[Any]:
    """
    Flatten a list of lists. 
    See [this stackoverflow topic](https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists).
    """
    return list(itertools.chain(*nested_list))

def nested_to_listoflist( l : list[list[list[Any]]], remove_duplicates:bool=False) -> list[list[Any]]:
    '''
    Go from a nested list to a list of lists
    https://stackoverflow.com/questions/57217633/convert-an-irregular-list-with-multiple-levels-of-nested-lists-to-a-list-of-list'
    If remove_duplicates is True, will remove duplicate entries. This turns out to be very convenient.
    '''
    if not is_listoflists(l):
        if is_iter(l):
            return l
        else:
            raise TypeError("nested_to_listoflist only accepts iters.")
    l = [el for el in flatten(l)]
    if remove_duplicates:
        l = _merge_identical_listoflist(l)
    return l

def merge_identical_items(l : list[Any]) -> list[Any]:
    '''shrink a list if some of the elements are identical. Set is normally better, but this will work for non-hashables (I think). But normally use a set!'''
    counter = collections.Counter(l)
    return list(counter.keys())

def is_listoflists(l : list[list[Any]]|list[tuple[Any]]|tuple[tuple[Any],...]|tuple[list[Any],...]) -> bool:
    '''
    Checks wheter l is a list of lists or not. Will also accept list of tuples and stuff
    '''
    if not is_iter(l) and not np.ndarray:
        return False
    if len(l) == 0:
        return False
    elif sum([1 for i in l if is_iter(i)]) == len(l):
        return True
    else:
        return False

def closest_in_list(l : list[float|int], item: float|int) -> int:
    """
    Returns the index of the closest item in a list to the given item.
    If there are multiple items equally close, returns the first one.
    """
    return min(range(len(l)), key=lambda i: abs(l[i] - item))

def _merge_identical_listoflist(l : list[Any], upwards:bool=False) -> list[Any]:
    """Helper for nested_to_listoflist, probably not usefull alone"""
    l.sort()
    l = list(l for l,_ in itertools.groupby(l))
    if len(l) == 1 and upwards:
        l = l[0]
    return l


def grouper(
    iterable: Iterable[Any], n: int, fillvalue: Any = None
) -> itertools.zip_longest:

    """
    Split data in iterable into fixed-length chunks or blocks. For instance, grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx". Note that the output is an iter thing, so call list before usig in most cases.

    Parameters
    ----------
    iterable : iterable
        iterable to regroup (str, list, tuple, etc.)
    n : int
        in how many groups to regroup
    fillvalue : any, optional
        What to fill the leftover groups with, by default None

    Returns
    -------
    itertools.zip_longest
        grouped iter
    """
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)
