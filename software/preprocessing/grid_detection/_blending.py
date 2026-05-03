import cv2
import numpy as np

def overlay_grid_on_image(image: np.ndarray, grid_bw: np.ndarray, thin_alpha: float = 0.3) -> np.ndarray:
    """
    Nakłada maskę siatki na obraz oryginalny z zachowaniem kolorów i przezroczystości linii.
    
    :param image: Obraz źródłowy (RGB lub RGBA).
    :param grid_bw: Czarno-biała maska siatki.
    :param thin_alpha: Stopień przezroczystości pomocniczych linii siatki.
    """
    # Jeśli obraz ma kanał Alfa, zdejmujemy go do obliczeń, ale zachowujemy maskę
    has_alpha = image.shape[2] == 4
    base_rgb = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB) if has_alpha else image.copy()
    
    overlay = base_rgb.astype(np.float32)

    # Grube linie (wartość 0 w masce) - pełne przykrycie na czarno
    mask_thick = grid_bw == 0
    overlay[mask_thick] = 0

    # Cienkie linie (wartości pośrednie w masce) - mieszanie (alpha blending)
    mask_thin = (grid_bw > 0) & (grid_bw < 255)
    overlay[mask_thin] = (1 - thin_alpha) * overlay[mask_thin] + thin_alpha * grid_bw[mask_thin, None]

    result_rgb = overlay.astype(np.uint8)

    # Jeśli oryginał miał kanał Alfa, przywracamy go
    if has_alpha:
        return cv2.merge([*cv2.split(result_rgb), image[:, :, 3]])
    
    return result_rgb