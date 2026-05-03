import cv2
import numpy as np
from typing import List, Tuple

def extract_long_lines(img: np.ndarray, min_lenght_ratio: float = 0.25) -> Tuple[np.ndarray, List[Tuple[int, int, int, int]]]:
    """Wykrywa długie linie proste na obrazie przy użyciu transformacji Hougha."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    max_dim = max(gray.shape)
    min_line_length = min_lenght_ratio * max_dim
    max_line_gap = 0.01 * max_dim
    
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, 
                            minLineLength=min_line_length, maxLineGap=max_line_gap)
                            
    output_image = img.copy()
    extracted_lines = []
    
    if lines is not None:
        for line in lines:
            coords = tuple(line[0])
            cv2.line(output_image, (coords[0], coords[1]), (coords[2], coords[3]), (0, 255, 0), 2)
            extracted_lines.append(coords)
            
    return output_image, extracted_lines

def filter_horizontal_lines(lines: List[Tuple[int, int, int, int]]) -> List[Tuple[int, int, int, int]]:
    """Filtruje listę linii, pozostawiając tylko te o charakterystyce poziomej."""
    return [l for l in lines if abs(l[2] - l[0]) > abs(l[3] - l[1])]