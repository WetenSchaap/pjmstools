import numpy as np

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