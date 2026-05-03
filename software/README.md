### **I. Warstwa Bazowa Systemu (Katalog `software/`)**

Niniejszy moduł implementuje mechanizmy niskopoziomowej obsługi danych wejściowych i wyjściowych, stanowiąc fundament dla dalszych etapów potoku przetwarzania obrazów:

*   **`_load_image.py`**: Realizuje proces deterministycznej akwizycji danych wizualnych z automatyczną konwersją do ustandaryzowanej przestrzeni barwnej RGB.
*   **`_plot_image.py`**: Moduł diagnostyczny umożliwiający wielokanałową wizualizację (obsługa skali szarości, RGB oraz RGBA) wraz z procedurą automatycznej korekcji zakresu dynamicznego do standardu `uint8`.
*   **`__init__.py`**: Definiuje interfejs programistyczny (API), eksponując kluczowe funkcje ładujące i renderujące na poziomie pakietu.

---

### **II. Pakiet Przetwarzania Wstępnego (Katalog `software/preprocessing/`)**

Zbiór specjalistycznych podsystemów dedykowanych rektyfikacji geometrycznej oraz precyzyjnej segmentacji sygnału pomiarowego:

#### **1. Moduł `image_aligner` (Rektyfikacja Geometryczna)**
*   **Detekcja orientacji**: Implementuje algorytm automatycznej niwelacji nachylenia obrazu, wykorzystujący probabilistyczną transformację Hougha do identyfikacji struktur liniowych.
*   **Transformacja afiniczna**: Realizuje operację bezstratnej rotacji z dynamicznym wyznaczaniem wymiarów płótna operacyjnego oraz natywną obsługą kanału Alpha.

#### **2. Moduł `grid_detection` (Analiza Struktur Periodycznych)**
*   **Rekonstrukcja matematyczna**: Dokonuje ekstrakcji siatek milimetrowych poprzez analizę rzutów ortogonalnych i statystyczną estymację okresu sygnału.
*   **Kompozycja wizualna**: Umożliwia nakładanie pomocniczych masek geometrycznych na obraz źródłowy przy zastosowaniu techniki mieszania kanałów (*alpha blending*).

#### **3. Moduł `image_cropp` (Segmentacja ROI)**
*   **Izolacja obszaru zainteresowania**: Wyznacza granice użyteczne sygnału na podstawie analizy wektorów aktywności gradientowej $G_v$ oraz $G_h$.
*   **Redukcja artefaktów**: Zapewnia automatyczną eliminację marginesów oraz komponentów pozasygnałowych, optymalizując dane do dalszej analizy strukturalnej.
