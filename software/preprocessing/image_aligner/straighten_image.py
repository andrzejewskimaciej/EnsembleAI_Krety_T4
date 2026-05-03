import numpy as np
from .detection import extract_long_lines, filter_horizontal_lines
from .geometry import calculate_alpha, rad_to_deg
from .transform import rotate_image_full_alpha

def straighten_image(img: np.ndarray) -> np.ndarray:
    """
    Automatycznie wykrywa nachylenie i prostuje obraz.
    
    Proces: Detekcja linii -> Obliczenie średniego kąta -> Rotacja z zachowaniem brzegów.
    """
    _, lines = extract_long_lines(img)
    filtered = filter_horizontal_lines(lines)

    if not filtered:
        _, lines = extract_long_lines(img, min_lenght_ratio=0.1)
        filtered = filter_horizontal_lines(lines)
    
    angle = rad_to_deg(calculate_alpha(filtered))
    return rotate_image_full_alpha(img, angle)