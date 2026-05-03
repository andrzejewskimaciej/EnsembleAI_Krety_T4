\# Moduł Detekcji i Rekonstrukcji Siatek Regularnych (Grid Detection Module)



Niniejszy komponent systemu odpowiada za matematyczną ekstrakcję, estymację parametrów oraz wizualną rekonstrukcję siatek milimetrowych i pomocniczych linii odniesienia na obrazach cyfrowych.



\## 1. Architektura i Funkcje Modułu



Moduł realizuje procesy analizy statystycznej sygnału wizyjnego w celu wyodrębnienia periodycznych struktur geometrycznych.



\*   \*\*`generate\_mm\_grid\_bw`\*\*: Implementuje algorytm detekcji oparty na projekcjach intensywności. Wykorzystuje technikę CLAHE (Contrast Limited Adaptive Histogram Equalization) do normalizacji oświetlenia przed analizą sygnału\[cite: 7].

\*   \*\*`generate\_mm\_grid\_clean`\*\*: Bardziej zaawansowana implementacja wykorzystująca estymację okresu (period) i przesunięcia (offset) w celu wygenerowania idealnej matematycznie siatki, odpornej na lokalne artefakty obrazu\[cite: 8].

\*   \*\*`overlay\_grid\_on\_image`\*\*: Funkcja realizująca proces kompozycji (alpha blending), nakładająca wygenerowaną maskę siatki na obraz źródłowy z zachowaniem transparentności linii pomocniczych\[cite: 6].



\## 2. Metodologia Analityczna



Proces ekstrakcji siatki opiera się na analizie rozkładu gęstości pikseli w rzutach ortogonalnych.



\### 2.1. Analiza Projekcji i Detekcja Szczytów

Obraz poddawany jest binaryzacji adaptacyjnej lub progowaniu, a następnie obliczane są sumy intensywności wzdłuż osi $X$ i $Y$ (Horizontal and Vertical Projections). W tak powstałym sygnale jednowymiarowym identyfikowane są piki (peaks), odpowiadające położeniu linii siatki\[cite: 7].



\### 2.2. Statystyczna Estymacja Parametrów Siatki

W celu zapewnienia odporności na szum i brakujące fragmenty linii, system wykorzystuje aparat statystyczny do wyznaczenia globalnej geometrii siatki:

\*   \*\*Estymacja Okresu ($T$):\*\* Wykorzystuje analizę histogramu różnic między szczytami (Inter-peak distances) oraz filtrację wartości odstających (IQR - Interquartile Range), aby wyznaczyć dominujący krok siatki\[cite: 8].

\*   \*\*Estymacja Offsetu ($O$):\*\* Obliczana poprzez analizę residuów (modulo period), co pozwala na idealne wyrównanie matematycznego modelu siatki do rzeczywistych danych obrazowych\[cite: 8].



\### 2.3. Interpolacja Struktur Sub-segmentowych

System automatycznie generuje zagęszczoną siatkę pomocniczą poprzez liniową interpolację punktów między głównymi węzłami siatki (sub-sampling), co pozwala na odtworzenie podziałek milimetrowych.



\## 3. Kompozycja Obrazu Wynikowego



Finalna faza wykorzystuje model mieszania kolorów w celu naniesienia siatki na obraz bez utraty informacji o teksturze tła:

\*   \*\*Linie Główne\*\*: Implementowane jako pełne nadpisanie wartości pikseli (maskowanie binarne)\[cite: 6].

\*   \*\*Linie Pomocnicze\*\*: Realizowane za pomocą algorytmu Alpha Blendingu:

&#x20;   $$C\_{out} = (1 - \\alpha) \\cdot C\_{src} + \\alpha \\cdot C\_{grid}$$

&#x20;   gdzie $\\alpha$ definiuje stopień przezroczystości linii cienkich\[cite: 6].

