"""
Functions acting on, or replacing parts of numpy.
"""
import builtins
import numpy as np
import scipy
import scipy.stats
from operator import index
from collections import namedtuple

def binned_statistic_dd(sample, values, statistic='mean',
                        bins=10, range=None, expand_binnumbers=False,
                        binned_statistic_result=None):
    """
    Compute a multidimensional binned statistic for a set of data.

    This is a generalization of a histogramdd function.  A histogram divides
    the space into bins, and returns the count of the number of points in
    each bin.  This function allows the computation of the sum, mean, median,
    or other statistic of the values within each bin.

    Parameters
    ----------
    sample : array_like
        Data to histogram passed as a sequence of N arrays of length D, or
        as an (N,D) array.
    values : (N,) array_like or list of (N,) array_like
        The data on which the statistic will be computed.  This must be
        the same shape as `sample`, or a list of sequences - each with the
        same shape as `sample`.  If `values` is such a list, the statistic
        will be computed on each independently.
    statistic : string or callable, optional
        The statistic to compute (default is 'mean').
        The following statistics are available:

          * 'mean' : compute the mean of values for points within each bin.
            Empty bins will be represented by NaN.
          * 'median' : compute the median of values for points within each
            bin. Empty bins will be represented by NaN.
          * 'count' : compute the count of points within each bin.  This is
            identical to an unweighted histogram.  `values` array is not
            referenced.
          * 'sum' : compute the sum of values for points within each bin.
            This is identical to a weighted histogram.
          * 'std' : compute the standard deviation within each bin. This
            is implicitly calculated with ddof=0. If the number of values
            within a given bin is 0 or 1, the computed standard deviation value
            will be 0 for the bin.
          * 'min' : compute the minimum of values for points within each bin.
            Empty bins will be represented by NaN.
          * 'max' : compute the maximum of values for point within each bin.
            Empty bins will be represented by NaN.
          * function : a user-defined function which takes a 1D array of
            values, and outputs a single numerical statistic. This function
            will be called on the values in each bin.  Empty bins will be
            represented by function([]), or NaN if this returns an error.

    bins : sequence or positive int, optional
        The bin specification must be in one of the following forms:

          * A sequence of arrays describing the bin edges along each dimension.
          * The number of bins for each dimension (nx, ny, ... = bins).
          * The number of bins for all dimensions (nx = ny = ... = bins).
    range : sequence, optional
        A sequence of lower and upper bin edges to be used if the edges are
        not given explicitly in `bins`. Defaults to the minimum and maximum
        values along each dimension.
    expand_binnumbers : bool, optional
        'False' (default): the returned `binnumber` is a shape (N,) array of
        linearized bin indices.
        'True': the returned `binnumber` is 'unraveled' into a shape (D,N)
        ndarray, where each row gives the bin numbers in the corresponding
        dimension.
        See the `binnumber` returned value, and the `Examples` section of
        `binned_statistic_2d`.
    binned_statistic_result : binnedStatisticddResult
        Result of a previous call to the function in order to reuse bin edges
        and bin numbers with new values and/or a different statistic.
        To reuse bin numbers, `expand_binnumbers` must have been set to False
        (the default)

        .. versionadded:: 0.17.0

    Returns
    -------
    statistic : ndarray, shape(nx1, nx2, nx3,...)
        The values of the selected statistic in each two-dimensional bin.
    bin_edges : list of ndarrays
        A list of D arrays describing the (nxi + 1) bin edges for each
        dimension.
    binnumber : (N,) array of ints or (D,N) ndarray of ints
        This assigns to each element of `sample` an integer that represents the
        bin in which this observation falls.  The representation depends on the
        `expand_binnumbers` argument.  See `Notes` for details.


    See Also
    --------
    numpy.digitize, numpy.histogramdd, binned_statistic, binned_statistic_2d

    Notes
    -----
    Binedges:
    All but the last (righthand-most) bin is half-open in each dimension.  In
    other words, if `bins` is ``[1, 2, 3, 4]``, then the first bin is
    ``[1, 2)`` (including 1, but excluding 2) and the second ``[2, 3)``.  The
    last bin, however, is ``[3, 4]``, which *includes* 4.

    `binnumber`:
    This returned argument assigns to each element of `sample` an integer that
    represents the bin in which it belongs.  The representation depends on the
    `expand_binnumbers` argument. If 'False' (default): The returned
    `binnumber` is a shape (N,) array of linearized indices mapping each
    element of `sample` to its corresponding bin (using row-major ordering).
    If 'True': The returned `binnumber` is a shape (D,N) ndarray where
    each row indicates bin placements for each dimension respectively.  In each
    dimension, a binnumber of `i` means the corresponding value is between
    (bin_edges[D][i-1], bin_edges[D][i]), for each dimension 'D'.

    .. versionadded:: 0.11.0

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> import matplotlib.pyplot as plt
    >>> from mpl_toolkits.mplot3d import Axes3D

    Take an array of 600 (x, y) coordinates as an example.
    `binned_statistic_dd` can handle arrays of higher dimension `D`. But a plot
    of dimension `D+1` is required.

    >>> mu = np.array([0., 1.])
    >>> sigma = np.array([[1., -0.5],[-0.5, 1.5]])
    >>> multinormal = stats.multivariate_normal(mu, sigma)
    >>> data = multinormal.rvs(size=600, random_state=235412)
    >>> data.shape
    (600, 2)

    Create bins and count how many arrays fall in each bin:

    >>> N = 60
    >>> x = np.linspace(-3, 3, N)
    >>> y = np.linspace(-3, 4, N)
    >>> ret = stats.binned_statistic_dd(data, np.arange(600), bins=[x, y],
    ...                                 statistic='count')
    >>> bincounts = ret.statistic

    Set the volume and the location of bars:

    >>> dx = x[1] - x[0]
    >>> dy = y[1] - y[0]
    >>> x, y = np.meshgrid(x[:-1]+dx/2, y[:-1]+dy/2)
    >>> z = 0

    >>> bincounts = bincounts.ravel()
    >>> x = x.ravel()
    >>> y = y.ravel()

    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111, projection='3d')
    >>> with np.errstate(divide='ignore'):   # silence random axes3d warning
    ...     ax.bar3d(x, y, z, dx, dy, bincounts)

    Reuse bin numbers and bin edges with new values:

    >>> ret2 = stats.binned_statistic_dd(data, -np.arange(600),
    ...                                  binned_statistic_result=ret,
    ...                                  statistic='mean')
    """
    known_stats = ['mean', 'nanmean', 'median', 'count', 'sum', 'std', 'min', 'max']
    if not callable(statistic) and statistic not in known_stats:
        raise ValueError(f'invalid statistic {statistic!r}')

    try:
        bins = index(bins)
    except TypeError:
        # bins is not an integer
        pass
    # If bins was an integer-like object, now it is an actual Python int.

    # NOTE: for _bin_edges(), see e.g. gh-11365
    if isinstance(bins, int) and not np.isfinite(sample).all():
        raise ValueError(f'{sample!r} contains non-finite values.')

    # `Ndim` is the number of dimensions (e.g. `2` for `binned_statistic_2d`)
    # `Dlen` is the length of elements along each dimension.
    # This code is based on np.histogramdd
    try:
        # `sample` is an ND-array.
        Dlen, Ndim = sample.shape
    except (AttributeError, ValueError):
        # `sample` is a sequence of 1D arrays.
        sample = np.atleast_2d(sample).T
        Dlen, Ndim = sample.shape

    # Store initial shape of `values` to preserve it in the output
    values = np.asarray(values)
    input_shape = list(values.shape)
    # Make sure that `values` is 2D to iterate over rows
    values = np.atleast_2d(values)
    Vdim, Vlen = values.shape

    # Make sure `values` match `sample`
    if statistic != 'count' and Vlen != Dlen:
        raise AttributeError('The number of `values` elements must match the '
                             'length of each `sample` dimension.')

    try:
        M = len(bins)
        if M != Ndim:
            raise AttributeError('The dimension of bins must be equal '
                                 'to the dimension of the sample x.')
    except TypeError:
        bins = Ndim * [bins]

    if binned_statistic_result is None:
        nbin, edges, dedges = np._bin_edges(sample, bins, range)
        binnumbers = np._bin_numbers(sample, nbin, edges, dedges)
    else:
        edges = binned_statistic_result.bin_edges
        nbin = np.array([len(edges[i]) + 1 for i in builtins.range(Ndim)])
        # +1 for outlier bins
        dedges = [np.diff(edges[i]) for i in builtins.range(Ndim)]
        binnumbers = binned_statistic_result.binnumber

    # Avoid overflow with double precision. Complex `values` -> `complex128`.
    result_type = np.result_type(values, np.float64)
    result = np.empty([Vdim, nbin.prod()], dtype=result_type)

    if statistic in {'mean', np.mean}:
        result.fill(np.nan)
        flatcount = np._bincount(binnumbers, None)
        a = flatcount.nonzero()
        for vv in builtins.range(Vdim):
            flatsum = np._bincount(binnumbers, values[vv])
            result[vv, a] = flatsum[a] / flatcount[a]
    elif statistic in {'std', np.std}:
        result.fill(np.nan)
        flatcount = np._bincount(binnumbers, None)
        a = flatcount.nonzero()
        for vv in builtins.range(Vdim):
            flatsum = np._bincount(binnumbers, values[vv])
            delta = values[vv] - flatsum[binnumbers] / flatcount[binnumbers]
            std = np.sqrt(
                np_bincount(binnumbers, delta*np.conj(delta))[a] / flatcount[a]
            )
            result[vv, a] = std
        result = np.real(result)
    elif statistic == 'count':
        result = np.empty([Vdim, nbin.prod()], dtype=np.float64)
        result.fill(0)
        flatcount = np._bincount(binnumbers, None)
        a = np.arange(len(flatcount))
        result[:, a] = flatcount[np.newaxis, :]
    elif statistic in {'sum', np.sum}:
        result.fill(0)
        for vv in builtins.range(Vdim):
            flatsum = np._bincount(binnumbers, values[vv])
            a = np.arange(len(flatsum))
            result[vv, a] = flatsum
    elif statistic in {'median', np.median}:
        result.fill(np.nan)
        for vv in builtins.range(Vdim):
            i = np.lexsort((values[vv], binnumbers))
            _, j, counts = np.unique(binnumbers[i],
                                     return_index=True, return_counts=True)
            mid = j + (counts - 1) / 2
            mid_a = values[vv, i][np.floor(mid).astype(int)]
            mid_b = values[vv, i][np.ceil(mid).astype(int)]
            medians = (mid_a + mid_b) / 2
            result[vv, binnumbers[i][j]] = medians
    elif statistic in {'min', np.min}:
        result.fill(np.nan)
        for vv in builtins.range(Vdim):
            i = np.argsort(values[vv])[::-1]  # Reversed so the min is last
            result[vv, binnumbers[i]] = values[vv, i]
    elif statistic in {'max', np.max}:
        result.fill(np.nan)
        for vv in builtins.range(Vdim):
            i = np.argsort(values[vv])
            result[vv, binnumbers[i]] = values[vv, i]
    elif statistic in {np.nanmean, "nanmean"}:
        result.fill(np.nan)
        for i in np.unique(binnumbers):
            for vv in builtins.range(Vdim):
                result[vv, i] = np.nanmean(values[vv, binnumbers == i])
    elif callable(statistic):
        with np.errstate(invalid='ignore'), catch_warnings():
            simplefilter("ignore", RuntimeWarning)
            try:
                null = statistic([])
            except Exception:
                null = np.nan
        if np.iscomplexobj(null):
            result = result.astype(np.complex128)
        result.fill(null)
        try:
            np._calc_binned_statistic(
                Vdim, binnumbers, result, values, statistic
            )
        except ValueError:
            result = result.astype(np.complex128)
            np._calc_binned_statistic(
                Vdim, binnumbers, result, values, statistic
            )

    # Shape into a proper matrix
    result = result.reshape(np.append(Vdim, nbin))

    # Remove outliers (indices 0 and -1 for each bin-dimension).
    core = tuple([slice(None)] + Ndim * [slice(1, -1)])
    result = result[core]

    # Unravel binnumbers into an ndarray, each row the bins for each dimension
    if expand_binnumbers and Ndim > 1:
        binnumbers = np.asarray(np.unravel_index(binnumbers, nbin))

    if np.any(result.shape[1:] != nbin - 2):
        raise RuntimeError('Internal Shape Error')

    # Reshape to have output (`result`) match input (`values`) shape
    result = result.reshape(input_shape[:-1] + list(nbin-2))

    return np.BinnedStatisticddResult(result, edges, binnumbers)

