import numpy as np
import cv2


def find_left_right_ecg_cut(img, threshold_ratio=0.15, smooth_window=25): # type: ignore
    """
    Finds left and right boundaries of the ECG signal area using horizontal gradient activity.

    Parameters
    ----------
    img : np.ndarray
        Input BGR image.
    threshold_ratio : float
        Normalized threshold for detecting signal region.
    smooth_window : int
        Moving average window for smoothing column activity.

    Returns
    -------
    tuple[int, int]
        Left and right pixel indices of ECG content.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # type: ignore

    grad = np.abs(np.diff(gray, axis=1)) # type: ignore
    col_activity = grad.mean(axis=0)

    col_activity = col_activity / (col_activity.max() + 1e-8)

    kernel = np.ones(smooth_window) / smooth_window
    smooth = np.convolve(col_activity, kernel, mode='same') # type: ignore

    idx = np.where(smooth > threshold_ratio)[0] # type: ignore

    if len(idx) == 0:
        return 0, img.shape[1] # type: ignore

    left = max(0, idx[0] - 10)
    right = min(img.shape[1], idx[-1] + 10) # type: ignore

    return left, right