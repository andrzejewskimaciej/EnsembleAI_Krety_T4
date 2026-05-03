import cv2
import numpy as np

def rotate_image_full_alpha(image: np.ndarray, angle: float) -> np.ndarray:
    """
    Obraca obraz o zadany kąt, zachowując oryginalne kolory i dodając kanał Alpha.
    
    :param image: Obraz wejściowy (RGB lub RGBA).
    :param angle: Kąt obrotu w stopniach.
    :return: Obrócony obraz z zachowanymi kolorami i kanałem Alpha.
    """
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # Obliczanie nowych wymiarów, aby pomieścić cały obrócony obraz
    cos, sin = np.abs(M[0, 0]), np.abs(M[0, 1])
    new_w, new_h = int((h * sin) + (w * cos)), int((h * cos) + (w * sin))
    
    # Korekta macierzy o przesunięcie (translacja)
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]
    
    # PRZYGOTOWANIE KANAŁÓW (Naprawa kolorów):
    if image.shape[2] == 3:
        # Zamiast cvtColor (które zgaduje format), ręcznie dodajemy kanał Alpha
        # To gwarantuje, że jeśli obraz jest RGB, zostanie RGB
        b_channel, g_channel, r_channel = cv2.split(image)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
        image_rgba = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    else:
        image_rgba = image.copy()
        
    # Wykonanie obrotu
    return cv2.warpAffine(
        image_rgba, 
        M, 
        (new_w, new_h), 
        flags=cv2.INTER_LINEAR, 
        borderMode=cv2.BORDER_CONSTANT, 
        borderValue=(0, 0, 0, 0)
    )