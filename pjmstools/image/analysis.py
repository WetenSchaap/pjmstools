from typing import Any
from numpy._typing._array_like import NDArray
import numpy as np
import scipy.ndimage

def generate_kymograph(
    data: NDArray,
    p1: tuple[int, int],
    p2: tuple[int, int],
    x_dim: int,
    y_dim: int,
    kymo_dim: int,
    n_points: int = 100,
    order: int = 1,
    mode: str = "nearest",
) -> NDArray[Any]:
    """
    Generates a kymograph from a multidimensional array.

    Parameters:
    -----------
    data : np.ndarray
        Input array.
    p1, p2 : tuple of float
        (x, y) start and end coordinates for the line.
    x_dim, y_dim, kymo_dim : int
        Indices for the x, y, and kymograph (e.g., time) axes.
    n_points : int
        Number of points along the line.
    order : int
        Interpolation order (0=nearest, 1=linear, 3=cubic).
    mode : str
        'constant', 'nearest', 'reflect', or 'wrap'.

    Returns:
    --------
    np.ndarray
        Kymograph of shape (kymo_size, n_points, *other_dims).
    """
    # Identify dimensions
    ndim = data.ndim
    all_dims = np.arange(ndim)

    # Separate dimensions: Spatial, Time, and "Other" (Data values)
    # We fix the order for the output grid: (Kymo, Line, *Other)
    other_dims = [d for d in all_dims if d not in (x_dim, y_dim, kymo_dim)]

    # Sizes for the output grid
    kymo_size = data.shape[kymo_dim]
    other_sizes = [data.shape[d] for d in other_dims]

    # Prepare coordinate arrays for the grid
    # We use a meshgrid-like approach by creating arrays of correct shape to broadcast

    # Coordinate arrays for X and Y (vary along the line axis)
    line_coords = np.linspace(p1[0], p2[0], n_points)
    y_line_coords = np.linspace(p1[1], p2[1], n_points)

    # Reshape for broadcasting: (1, n_points, 1, ..., 1)
    # Prepending 1s for Kymo and Other dims
    line_shape = [1, n_points] + [1] * len(other_dims)
    x_grid = line_coords.reshape(line_shape)
    y_grid = y_line_coords.reshape(line_shape)

    # Coordinate array for Kymo dimension (vary along first axis)
    # Shape: (kymo_size, 1, 1, ..., 1)
    kymo_coords = np.arange(kymo_size)
    kymo_shape = [kymo_size, 1] + [1] * len(other_dims)
    kymo_grid = kymo_coords.reshape(kymo_shape)

    # Coordinate arrays for Other dimensions (vary along their respective trailing axes)
    other_grids = []
    for i, dim_idx in enumerate(other_dims):
        size = data.shape[dim_idx]
        # Shape: (1, 1, ..., size, ..., 1)
        # The 'size' is at position 2 + i
        target_shape = [1, 1] + [1] * len(other_dims)
        target_shape[2 + i] = size
        other_grids.append(np.arange(size).reshape(target_shape))

    # Assemble full coordinates array for map_coordinates
    # map_coordinates expects (ndim, *output_shape)
    # We must fill the slots corresponding to the specific axes of the input data

    full_coords = np.zeros((ndim, kymo_size, n_points, *other_sizes))

    # Assign grids to their respective coordinate indices
    full_coords[x_dim] = x_grid
    full_coords[y_dim] = y_grid
    full_coords[kymo_dim] = kymo_grid

    for i, dim_idx in enumerate(other_dims):
        full_coords[dim_idx] = other_grids[i]

    # Interpolate
    kymo = scipy.ndimage.map_coordinates(data, full_coords, order=order, mode=mode)

    return kymo
