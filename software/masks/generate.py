import json
import numpy as np
import cv2

def create_mask_from_json(json_path: str, target_shape: tuple, apply_angle: float) -> np.ndarray:
    with open(json_path, 'r') as f:
        data = json.load(f)

    w_json = int(data.get('width', 2200))
    h_json = int(data.get('height', 1700))
    crop_ratio = float(data.get('crop', 0.0))

    # KROK 1: Rysowanie (XY)
    mask = np.zeros((h_json, w_json), dtype=np.uint8)
    for lead in data.get('leads', []):
        pixels = np.array(lead['plotted_pixels'], dtype=np.float32)
        if pixels.size == 0: continue
        pixels_xy = pixels[:, [1, 0]].reshape((-1, 1, 2))
        cv2.polylines(mask, [np.int32(pixels_xy)], False, 255, 2)

    # KROK 2: Rotacja o kąt WYKRYTY, a nie z JSON-a
    # Używamy ujemnego kąta wykrytego, aby "skrzywić" maskę tak jak obraz
    if apply_angle != 0.0:
        center = (w_json / 2, h_json / 2)
        M = cv2.getRotationMatrix2D(center, -apply_angle, 1.0)
        mask = cv2.warpAffine(mask, M, (w_json, h_json), flags=cv2.INTER_NEAREST)

    # KROK 3: Crop i Resize[cite: 1, 3]
    if crop_ratio > 0:
        dy, dx = int(h_json * crop_ratio), int(w_json * crop_ratio)
        mask = mask[dy:h_json - dy, dx:w_json - dx]

    return cv2.resize(mask, (target_shape[1], target_shape[0]), interpolation=cv2.INTER_NEAREST)