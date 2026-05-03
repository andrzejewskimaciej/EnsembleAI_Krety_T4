import numpy as np
import cv2


def find_top_ecg_cut(img, threshold_ratio=0.15): # type: ignore
    """
    Finds the top boundary of the ECG signal area using vertical gradient activity.

    Parameters
    ----------
    img : np.ndarray
        Input BGR image.
    threshold_ratio : float
        Normalized threshold for detecting signal start.

    Returns
    -------
    int
        Top pixel index of ECG content.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # type: ignore

    grad = np.abs(np.diff(gray, axis=0)) # type: ignore
    row_activity = grad.mean(axis=1)

    row_activity = row_activity / (row_activity.max() + 1e-8)

    idx = np.where(row_activity > threshold_ratio)[0]

    if len(idx) == 0:
        return int(0.25 * img.shape[0]) # type: ignore

    return max(0, idx[0] - 10)