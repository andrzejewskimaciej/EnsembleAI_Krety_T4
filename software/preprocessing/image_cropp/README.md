# Moduł Automatycznej Segmentacji i Kadrowania (ECG Signal Cropping)

Komponent ten odpowiada za inteligentną redukcję wymiarów obrazu wejściowego poprzez usunięcie artefaktów brzegowych, nagłówków oraz obszarów nieprzydatnych analitycznie. System koncentruje się na izolacji regionu zainteresowania (Region of Interest - ROI), zawierającego wyłącznie przebiegi sygnału.

## 1. Architektura Funkcjonalna

Algorytm kadrowania opiera się na analizie gęstości zmian natężenia pikseli, co pozwala na precyzyjne odróżnienie statycznego tła od dynamicznych przebiegów sygnału.

*   **`crop_ecg`**: Główna funkcja sterująca procesem segmentacji. Realizuje dwuetapową procedurę wyznaczania granic pionowych oraz jednorazową detekcję granic horyzontalnych.
*   **`find_top_ecg_cut`**: Implementuje mechanizm detekcji górnej granicy obszaru sygnału na podstawie wertykalnej aktywności gradientowej.
*   **`find_left_right_ecg_cut`**: Odpowiada za lokalizację marginesów bocznych przy wykorzystaniu wygładzonej analizy gradientu poziomego.

## 2. Metodologia Detekcji Granic

### 2.1. Analiza Aktywności Gradientowej (Gradient Activity Analysis)

Podstawą detekcji jest obliczenie bezwzględnej różnicy między sąsiednimi pikselami (gradientu), co służy jako deskryptor zmienności lokalnej:

*   Dla granic pionowych: $G_v = |\frac{\partial I}{\partial y}|$.
*   Dla granic poziomych: $G_h = |\frac{\partial I}{\partial x}|$.

Średnia wartość gradientu dla każdego rzędu lub kolumny jest normalizowana względem wartości maksymalnej, tworząc profil aktywności sygnału.

### 2.2. Adaptacyjne Wyznaczanie ROI

Proces segmentacji przebiega według następującego rygoru:

1.  **Estymacja Górnej Granicy**: Identyfikacja pierwszego indeksu wiersza, w którym znormalizowana aktywność przekracza zadany próg `threshold_ratio`. W przypadku braku detekcji, system stosuje bezpieczny margines na poziomie 25% wysokości obrazu.
2.  **Wygładzanie Sygnału (Smoothing)**: Przy wyznaczaniu granic bocznych stosowana jest konwolucja z jądrem średniej kroczącej (`moving average window`), co pozwala na eliminację szumów wysokoczęstotliwościowych i stabilizację detekcji marginesów.
3.  **Rekursywne Kadrowanie**: Funkcja `crop_ecg` wykonuje kaskadowe wywołania detekcji, co pozwala na precyzyjne dostrojenie obszaru roboczego po wstępnym usunięciu nagłówków.
