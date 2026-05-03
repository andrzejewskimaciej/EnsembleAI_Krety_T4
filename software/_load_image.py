import cv2
import numpy as np
import os
from typing import Optional

def load_image(path: str) -> np.ndarray:
    """
    Wczytuje obraz z dysku i konwertuje go do formatu RGB.
    
    :param path: Ścieżka do pliku graficznego.
    :return: Obraz jako macierz numpy w formacie RGB.
    :raises FileNotFoundError: Jeśli plik nie istnieje pod wskazaną ścieżką.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Nie znaleziono pliku: {path}")

    # Wczytanie obrazu (OpenCV domyślnie używa BGR)
    img = cv2.imread(path)
    
    if img is None:
        raise ValueError(f"Nie udało się zdekodować obrazu: {path}")

    # Konwersja BGR -> RGB dla zachowania standardu wewnątrz pakietu
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)