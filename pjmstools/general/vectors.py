import numpy as np
from .listoperations import is_listoflists

def unit_vector(vector : np.ndarray) -> np.ndarray:
    """ 
    Returns the unit vector of the given vector.
    """
    try:
        norm = np.linalg.norm(vector.astype(float),axis=1)
        return vector / np.array([norm,norm]).T
    except np.exceptions.AxisError:
        return vector / np.linalg.norm(vector)
    
def angle_between(v1 : np.ndarray, v2 : np.ndarray|list[np.ndarray]) -> float|np.ndarray:
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
