import itertools
import numpy as np
import collections
from general import is_iter

def flatten(nested_list : list[list]) -> list:
    """
    Flatten a list of lists. 
    See [this stackoverflow topic](https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists).
    """
    return list(itertools.chain(*nested_list))

def nested_to_listoflist( l : list[list[list]], remove_duplicates=False) -> list[list]:
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

def merge_identical_items(l : list) -> list:
    '''shrink a list if some of the elements are identical. Set is normally better, but this will work for non-hashables (I think). But normally use a set!'''
    counter = collections.Counter(l)
    return list(counter.keys())

def is_listoflists(l : list[list]|list[tuple]|tuple[tuple,...]|tuple[list,...]) -> bool:
    '''
    Checks wheter l is a list of lists or not. Will also accept list of tuples and stuff
    '''
    if not is_iter(l) and not np.array:
        return False
    if len(l) == 0:
        return False
    elif sum([1 for i in l if is_iter(i)]) == len(l):
        return True
    else:
        return False

def _merge_identical_listoflist(l : list, upwards=False) -> list:
    """Helper for nested_to_listoflist, probably not usefull alone"""
    l.sort()
    l = list(l for l,_ in itertools.groupby(l))
    if len(l) == 1 and upwards:
        l = l[0]
    return l