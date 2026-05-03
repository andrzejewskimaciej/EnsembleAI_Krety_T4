# Moduł Detekcji i Rekonstrukcji Siatek Regularnych (Grid Detection Module)

Niniejszy komponent systemu odpowiada za matematyczną ekstrakcję, estymację parametrów oraz wizualną rekonstrukcję siatek milimetrowych i pomocniczych linii odniesienia na obrazach cyfrowych.

## 1. Architektura i Funkcje Modułu

Moduł realizuje procesy analizy statystycznej sygnału wizyjnego w celu wyodrębnienia periodycznych struktur geometrycznych.

*   **`generate_mm_grid_bw`**: Implementuje algorytm detekcji oparty na projekcjach intensywności. Wykorzystuje technikę CLAHE (Contrast Limited Adaptive Histogram Equalization) do normalizacji oświetlenia przed analizą sygnału.
*   **`generate_mm_grid_clean`**: Bardziej zaawansowana implementacja wykorzystująca estymację okresu (period) i przesunięcia (offset) w celu wygenerowania idealnej matematycznie siatki, odpornej na lokalne artefakty obrazu.
*   **`overlay_grid_on_image`**: Funkcja realizująca proces kompozycji (alpha blending), nakładająca wygenerowaną maskę siatki na obraz źródłowy z zachowaniem transparentności linii pomocniczych.

## 2. Metodologia Analityczna

Proces ekstrakcji siatki opiera się na analizie rozkładu gęstości pikseli w rzutach ortogonalnych.

### 2.1. Analiza Projekcji i Detekcja Szczytów
Obraz poddawany jest binaryzacji adaptacyjnej lub progowaniu, a następnie obliczane są sumy intensywności wzdłuż osi $X$ i $Y$ (Horizontal and Vertical Projections). W tak powstałym sygnale jednowymiarowym identyfikowane są piki (peaks), odpowiadające położeniu linii siatki.

### 2.2. Statystyczna Estymacja Parametrów Siatki
W celu zapewnienia odporności na szum i brakujące fragmenty linii, system wykorzystuje aparat statystyczny do wyznaczenia globalnej geometrii siatki:

*   **Estymacja Okresu ($T$):** Wykorzystuje analizę histogramu różnic między szczytami (Inter-peak distances) oraz filtrację wartości odstających (IQR - Interquartile Range), aby wyznaczyć dominujący krok siatki.
*   **Estymacja Offsetu ($O$):** Obliczana poprzez analizę residuów (modulo period), co pozwala na idealne wyrównanie matematycznego modelu siatki do rzeczywistych danych obrazowych.

### 2.3. Interpolacja Struktur Sub-segmentowych
System automatycznie generuje zagęszczoną siatkę pomocniczą poprzez liniową interpolację punktów między głównymi węzłami siatki (sub-sampling), co pozwala na odtworzenie podziałek milimetrowych.

## 3. Kompozycja Obrazu Wynikowego

Finalna faza wykorzystuje model mieszania kolorów w celu naniesienia siatki na obraz bez utraty informacji o teksturze tła:

*   **Linie Główne**: Implementowane jako pełne nadpisanie wartości pikseli (maskowanie binarne).
*   **Linie Pomocnicze**: Realizowane za pomocą algorytmu Alpha Blendingu:
    $$C_{out} = (1 - \alpha) \cdot C_{src} + \alpha \cdot C_{grid}$$
    gdzie $\alpha$ definiuje stopień przezroczystości linii cienkich.
