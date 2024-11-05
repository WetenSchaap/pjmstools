import numpy as np

def closest_entry(target: float, my_dict: dict) -> tuple[float,any]:
    """
    Find the key in a dict closest in numerical value to the target

    Parameters
    ----------
    target : float
    my_dict : dict

    Returns
    -------
    tuple[float,any]
        tuple with closest key, value pair.
    """
    closest_key_distance = np.inf
    for k in my_dict.keys(): # probably can be vectorized, burt don't feel like doing that now.
        if abs(k-target) < closest_key_distance:
            closest_key = k
            closest_key_distance = abs(k - target)
    closest_value = my_dict[closest_key]
    return closest_key, closest_value

def inverse_dict_lists(to_invert : dict) -> dict[list]:
    """
    Generate the inverse dict of the given dict. The values become keys, meaning they *must* be hashable and unique. The keys in the original dict are added to a list of their corresponding values. So there is *always* a list of values, even if there is only 1. Has all kinds of further weird limitations, so *always* test this on your particular usecase.

    Parameters
    ----------
    to_invert : dict

    Returns
    -------
    dict[list]
    """
    inverse = {}
    for k,v in to_invert.items():
        for x in v:
            inverse.setdefault(x, []).append(k)

    return inverse

def binedges_to_bincenters(bins : list|np.ndarray|tuple) -> np.ndarray:
    """
    Converts edges of bins of histogram to centers. Is a secret alias for running_average. Just throw in the binedges as you get them from np.histogram() or others, and you get the centers back.
    """
    return running_average(bins,2)

def running_average(x : list|np.ndarray|tuple, N : int) -> np.ndarray:
    """
    Calculates running average (or rolling mean) of data x, with meansize N.
    See also: https://stackoverflow.com/questions/13728392/moving-average-or-running-mean
    
    Parameters
    ----------
    x : list-like
        Data
    N : int
        Number of datapoints to average over

    Returns
    -------
    np.array
        Averaged data. Will miss the first N/2 datapoints.
    """
    return np.convolve(x, np.ones(N)/N, mode='valid')

def is_iter(it) -> bool:
    '''Check if input is an iterable'''
    try:
        _ = iter(it)
        return True
    except TypeError:
        return False
    
if __name__ == "__main__":
    dict = {
        1: [1],
        2: [2],
        3: [3],
        4: "4",
        5: "5",
        6: "six",
        7: 7,
        8: 8,
        9: 9,
    }
    print( closest_entry(4.231,dict) )