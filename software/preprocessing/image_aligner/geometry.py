import numpy as np
import math
from typing import List, Tuple

def calculate_alpha(lines: List[Tuple[int, int, int, int]]) -> float:
    """Oblicza średni kąt nachylenia linii w radianach."""
    if not lines:
        return 0.0
    slopes = []
    for x1, y1, x2, y2 in lines:
        dx = x2 - x1
        slopes.append((y2 - y1) / (dx if dx != 0 else 1e-5))
    return np.arctan(np.mean(slopes))

def rad_to_deg(angle_rad: float) -> float:
    """Konwertuje radiany na stopnie."""
    return angle_rad * (180.0 / math.pi)