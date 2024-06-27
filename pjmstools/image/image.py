import numpy as np

def contrast_normalize(image:np.ndarray, maxpx = 255) -> np.ndarray:
    """Renormalize contrast to outer bounds. Does not change datatype! Only input np.array's!"""
    return ((image - np.min(image)) / (np.max(image) - np.min(image))) * maxpx

def autocontrast(image:np.ndarray, cliprange = 2, maxpx = 255) -> np.ndarray:
    """Autocontrast to outer bounds + cliprange in %. Does not change datatype! Only input np.array's!"""
    minval = np.percentile(image, cliprange)
    maxval = np.percentile(image, 100 - cliprange)
    pixvals = np.clip(image, minval, maxval)
    return ((pixvals - minval) / (maxval - minval)) * maxpx
