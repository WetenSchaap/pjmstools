import numpy as np
import numpy.typing as npt
from .listoperations import is_listoflists

def unit_vector(vector : npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    """ 
    Returns the unit vector of the given vector.
    """
    try:
        norm = np.linalg.norm(vector.astype(float),axis=1)
        return vector / np.array([norm,norm]).T
    except np.exceptions.AxisError:
        return vector / np.linalg.norm(vector)


def angle_between(
    v1: npt.NDArray[np.float64],
    v2: npt.NDArray[np.float64] | list[npt.NDArray[np.float64]],
) -> float |npt.NDArray[np.float64]:
    """ 
    Returns the angle in radians between vectors 'v1' and 'v2'.
    v2 can be multiple vectors.
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    if is_listoflists(v2_u):
        angles = np.arctan2(v2_u.T[1],v2_u.T[0]) - np.arctan2(v1_u.T[1],v1_u.T[0])
        ch_ind_m = angles < -np.pi
        ch_ind_p = angles > np.pi
        angles[ch_ind_m] = angles[ch_ind_m] + 2*np.pi
        angles[ch_ind_p] = angles[ch_ind_p] - 2*np.pi
        return angles
    else:
        return np.arctan2(v2_u[1],v2_u[0]) - np.arctan2(v1_u[1],v1_u[0])


def transform_coordinate_system(
    u_vec: npt.NDArray[np.float64],
    O: npt.NDArray[np.float64],
    P: npt.NDArray[np.float64],
) -> npt.NDArray[np.float64]:
    """
    Convert xy coordinates of point P to uv coordinates. Note that the v-axis positive direction is shifted *clock-wise* compared to the u-axis by defintion .

    Parameters
    ----------
    u_vec : np.ndarray
        unit vector describing the 'x-axis' of the uv coordinate system
    O : np.ndarray
        vector describing the origin of the u,v-coordinate system in xy
    P : np.ndarray
        (x,y)-coordinates of point P in the regular coordinate system. Can also be an array of points.

    Returns
    -------
    np.ndarray
        (u,v)-coordinates of point P. If P is an array, an array of (u,v)-coordinates is also returned.
    """
    P_shifted = P - O
    v_vec = np.array([u_vec[1], -u_vec[0]])  # perpindicular "y-axis"
    u = np.dot(P_shifted, u_vec)
    v = np.dot(P_shifted, v_vec)
    return np.array([u, v]).T

