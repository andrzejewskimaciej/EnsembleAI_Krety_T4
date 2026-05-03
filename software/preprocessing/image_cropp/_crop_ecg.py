from ._find_top_ecg_cut import find_top_ecg_cut # type: ignore
from ._fing_left_right_ecg_cut import find_left_right_ecg_cut # type: ignore

def crop_ecg(img): # type: ignore
    """
    Automatically crops an ECG image to the region containing signal data.

    Parameters
    ----------
    img : np.ndarray
        Input BGR image.

    Returns
    -------
    np.ndarray
        Cropped image containing ECG signal only.
    """
    top = find_top_ecg_cut(img, threshold_ratio=0.5) # type: ignore

    img = img[top:, ...] # type: ignore

    top = find_top_ecg_cut(img, threshold_ratio=2) # type: ignore

    left, right = find_left_right_ecg_cut( # type: ignore
        img[top:, ...], # type: ignore
        threshold_ratio=1e-2
    )

    return img[top:, left:right, ...]# type: ignore