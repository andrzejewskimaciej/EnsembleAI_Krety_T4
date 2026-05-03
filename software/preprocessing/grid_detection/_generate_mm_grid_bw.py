import cv2
import numpy as np
from scipy.signal import find_peaks
from typing import List, Union

def generate_mm_grid_bw(
    image: np.ndarray, 
    threshold_ratio: float = 0.3, 
    small_lines_per_segment: int = 4, 
    intensity_small: int = 128, 
    min_segment_for_small: int = 9
) -> np.ndarray:
    """
    Analizuje obraz i generuje czarno-białą maskę siatki milimetrowej.
    
    Wykorzystuje rzuty intensywności pikseli do znalezienia regularnych odstępów linii.
    """
    # Obsługa obrazu z kanałem Alfa lub bez
    working_img = image[:, :, :3] if image.shape[2] == 4 else image
    
    # Preprocessing sygnału
    gray = cv2.cvtColor(working_img, cv2.COLOR_RGB2GRAY)
    enhanced = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)).apply(gray)

    # Projekcje i detekcja szczytów
    hor_proj = np.sum(255 - enhanced, axis=1)
    ver_proj = np.sum(255 - enhanced, axis=0)

    hor_peaks, _ = find_peaks(hor_proj, height=threshold_ratio * np.max(hor_proj))
    ver_peaks, _ = find_peaks(ver_proj, height=threshold_ratio * np.max(ver_proj))

    # Obliczanie typowych odstępów
    typical_h = int(np.median(np.diff(hor_peaks))) if len(hor_peaks) > 1 else 20
    typical_v = int(np.median(np.diff(ver_peaks))) if len(ver_peaks) > 1 else 20

    h_lines = np.arange(hor_peaks[0] if len(hor_peaks) > 0 else 0, 
                        hor_peaks[-1] + typical_h if len(hor_peaks) > 0 else image.shape[0], typical_h)
    v_lines = np.arange(ver_peaks[0] if len(ver_peaks) > 0 else 0, 
                        ver_peaks[-1] + typical_v if len(ver_peaks) > 0 else image.shape[1], typical_v)

    h_full = _add_small_lines(h_lines, small_lines_per_segment, min_segment_for_small)
    v_full = _add_small_lines(v_lines, small_lines_per_segment, min_segment_for_small)

    # Budowanie maski siatki
    grid_bw = np.full(image.shape[:2], 255, dtype=np.uint8)

    # Rysowanie cienkich linii
    for y in h_full:
        if 0 <= y < grid_bw.shape[0] and y not in h_lines: grid_bw[y, :] = intensity_small
    for x in v_full:
        if 0 <= x < grid_bw.shape[1] and x not in v_lines: grid_bw[:, x] = intensity_small

    # Rysowanie głównych linii (grubsze/ciemniejsze)
    for y in h_lines:
        if 0 <= y < grid_bw.shape[0]: grid_bw[int(y), :] = 0
    for x in v_lines:
        if 0 <= x < grid_bw.shape[1]: grid_bw[:, int(x)] = 0

    return grid_bw

def _add_small_lines(lines: np.ndarray, n_small: int, min_dist: int) -> np.ndarray:
    """Funkcja pomocnicza do interpolacji gęstszej siatki między głównymi liniami."""
    if len(lines) == 0: return np.array([])
    full = [lines[0]]
    for i in range(1, len(lines)):
        start, end = lines[i-1], lines[i]
        if end - start >= min_dist:
            step = (end - start) / (n_small + 1)
            for j in range(1, n_small + 1):
                full.append(int(round(start + j * step)))
        full.append(end)
    return np.unique(full)