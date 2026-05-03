import matplotlib.pyplot as plt
import numpy as np
import cv2

def plot_image(image: np.ndarray, title: str = "Image Preview") -> None:
    plt.figure(figsize=(8, 8))

    img = image.copy()

    # 🔥 1. Napraw zakres
    if img.dtype != np.uint8:
        img = np.clip(img, 0, 255).astype(np.uint8)

    # 🔥 2. Obsługa grayscale
    if len(img.shape) == 2:
        plt.imshow(img, cmap='gray', vmin=0, vmax=255)

    elif len(img.shape) == 3:
        # 🔥 3. RGBA
        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
            plt.imshow(img)

        # 🔥 4. RGB/BGR detection heuristic
        elif img.shape[2] == 3:
            # zakładamy że to BGR z OpenCV → konwersja
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            plt.imshow(img)

        else:
            raise ValueError("Nieobsługiwany format obrazu")

    else:
        raise ValueError("Nieobsługiwany wymiar obrazu")

    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()