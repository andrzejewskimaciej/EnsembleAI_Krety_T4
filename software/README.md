\### \*\*Rdzeń Pakietu (software/)\*\*

Podstawowa warstwa obsługi danych wejściowych i wyjściowych:

\*   \*\*`\_load\_image.py`\*\*: Deterministyczna akwizycja obrazów z konwersją do ustandaryzowanej przestrzeni barwnej RGB.

\*   \*\*`\_plot\_image.py`\*\*: Wielokanałowa wizualizacja diagnostyczna (obsługa Grayscale, RGB, RGBA) z automatyczną korekcją zakresu `uint8`.

\*   \*\*`\_\_init\_\_.py`\*\*: Interfejs programistyczny eksponujący funkcje ładujące i renderujące.



\---



\### \*\*Pakiet Przetwarzania Wstępnego (software/preprocessing/)\*\*

Specjalistyczne moduły rektyfikacji i segmentacji sygnału:



\#### \*\*image\_aligner (Rektyfikacja Geometryczna)\*\*

\*   Automatyczna niwelacja nachylenia obrazu na podstawie probabilistycznej transformacji Hougha.

\*   Bezstratna rotacja z dynamicznym przeliczeniem wymiarów płótna i obsługą kanału Alpha.



\#### \*\*grid\_detection (Analiza Struktur Periodycznych)\*\*

\*   Matematyczna rekonstrukcja siatek pomiarowych poprzez analizę rzutów ortogonalnych i estymację okresu.

\*   Nakładanie masek pomocniczych z wykorzystaniem techniki \*alpha blending\*.



\#### \*\*image\_cropp (Segmentacja ROI)\*\*

\*   Izolacja obszaru sygnału poprzez analizę aktywności gradientowej $G\_v$ i $G\_h$.

\*   Automatyczna eliminacja marginesów oraz artefaktów pozasygnałowych.

