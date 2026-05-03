import cv2
import numpy as np
from scipy.signal import find_peaks
from scipy.stats import mode


def generate_mm_grid_clean(
    image: np.ndarray,
    threshold_ratio: float = 0.3,
    small_lines_per_segment: int = 4,
    intensity_small: int = 128,
):
    gray = cv2.cvtColor(image[:, :, :3], cv2.COLOR_RGB2GRAY)

    # 🔧 stabilniejszy preprocessing
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    bw = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        15, 2
    )

    # projekcje
    hor_proj = np.sum(bw, axis=1)
    ver_proj = np.sum(bw, axis=0)

    # piki
    hor_peaks, _ = find_peaks(hor_proj, height=threshold_ratio * np.max(hor_proj))
    ver_peaks, _ = find_peaks(ver_proj, height=threshold_ratio * np.max(ver_proj))

    # 🔥 KLUCZ: estymacja okresu
    h_period = _estimate_period(hor_peaks)
    v_period = _estimate_period(ver_peaks)

    # 🔥 KLUCZ: estymacja offsetu
    h_offset = _estimate_offset(hor_peaks, h_period)
    v_offset = _estimate_offset(ver_peaks, v_period)

    # generowanie IDEALNEJ siatki
    h_lines = np.arange(h_offset, image.shape[0], h_period)
    v_lines = np.arange(v_offset, image.shape[1], v_period)

    # dodanie cienkich linii
    h_full = _add_small_lines(h_lines, small_lines_per_segment)
    v_full = _add_small_lines(v_lines, small_lines_per_segment)

    # render
    grid = np.full(image.shape[:2], 255, dtype=np.uint8)

    # cienkie
    for y in h_full:
        if y not in h_lines and 0 <= y < grid.shape[0]:
            grid[int(y), :] = intensity_small

    for x in v_full:
        if x not in v_lines and 0 <= x < grid.shape[1]:
            grid[:, int(x)] = intensity_small

    # grube
    for y in h_lines:
        if 0 <= y < grid.shape[0]:
            grid[int(y), :] = 0

    for x in v_lines:
        if 0 <= x < grid.shape[1]:
            grid[:, int(x)] = 0

    return grid


# =========================
# 🔬 MATEMATYKA
# =========================

def _estimate_period(peaks: np.ndarray) -> int:
    if len(peaks) < 2:
        return 20

    diffs = np.diff(peaks)

    # usuwanie outlierów (IQR)
    q1, q3 = np.percentile(diffs, [25, 75])
    iqr = q3 - q1
    good = diffs[(diffs > q1 - 1.5 * iqr) & (diffs < q3 + 1.5 * iqr)]

    if len(good) == 0:
        good = diffs

    # 🔥 histogram zamiast scipy.mode
    good = np.round(good).astype(int)

    values, counts = np.unique(good, return_counts=True)

    return int(values[np.argmax(counts)])

def _estimate_offset(peaks: np.ndarray, period: int) -> int:
    if len(peaks) == 0:
        return 0

    # 🔥 sprowadzenie do modulo okresu
    residues = peaks % period

    # histogram → najczęstszy offset
    hist, bin_edges = np.histogram(residues, bins=period)
    offset = int(bin_edges[np.argmax(hist)])

    return offset


def _add_small_lines(lines: np.ndarray, n_small: int):
    if len(lines) < 2:
        return lines

    full = []

    for i in range(len(lines) - 1):
        start, end = lines[i], lines[i + 1]
        full.append(start)

        step = (end - start) / (n_small + 1)
        for j in range(1, n_small + 1):
            full.append(start + j * step)

    full.append(lines[-1])

    return np.array(full)