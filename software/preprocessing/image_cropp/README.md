\# Moduł Automatycznej Segmentacji i Kadrowania (ECG Signal Cropping)



Komponent ten odpowiada za inteligentną redukcję wymiarów obrazu wejściowego poprzez usunięcie artefaktów brzegowych, nagłówków oraz obszarów nieprzydatnych analitycznie. System koncentruje się na izolacji regionu zainteresowania (Region of Interest - ROI), zawierającego wyłącznie przebiegi sygnału.



\## 1. Architektura Funkcjonalna



Algorytm kadrowania opiera się na analizie gęstości zmian natężenia pikseli, co pozwala na precyzyjne odróżnienie statycznego tła od dynamicznych przebiegów sygnału.



\*   \*\*`crop\_ecg`\*\*: Główna funkcja sterująca procesem segmentacji. Realizuje dwuetapową procedurę wyznaczania granic pionowych oraz jednorazową detekcję granic horyzontalnych\[cite: 9].

\*   \*\*`find\_top\_ecg\_cut`\*\*: Implementuje mechanizm detekcji górnej granicy obszaru sygnału na podstawie wertykalnej aktywności gradientowej\[cite: 10].

\*   \*\*`find\_left\_right\_ecg\_cut`\*\*: Odpowiada za lokalizację marginesów bocznych przy wykorzystaniu wygładzonej analizy gradientu poziomego\[cite: 11].



\## 2. Metodologia Detekcji Granic



\### 2.1. Analiza Aktywności Gradientowej (Gradient Activity Analysis)

Podstawą detekcji jest obliczenie bezwzględnej różnicy między sąsiednimi pikselami (gradientu), co służy jako deskryptor zmienności lokalnej:

\*   Dla granic pionowych: $G\_v = |\\frac{\\partial I}{\\partial y}|$\[cite: 10].

\*   Dla granic poziomych: $G\_h = |\\frac{\\partial I}{\\partial x}|$\[cite: 11].



Średnia wartość gradientu dla każdego rzędu lub kolumny jest normalizowana względem wartości maksymalnej, tworząc profil aktywności sygnału.



\### 2.2. Adaptacyjne Wyznaczanie ROI

Proces segmentacji przebiega według następującego rygoru:

1\.  \*\*Estymacja Górnej Granicy\*\*: Identyfikacja pierwszego indeksu wiersza, w którym znormalizowana aktywność przekracza zadany próg `threshold\_ratio`\[cite: 10]. W przypadku braku detekcji, system stosuje bezpieczny margines na poziomie 25% wysokości obrazu\[cite: 10].

2\.  \*\*Wygładzanie Sygnału (Smoothing)\*\*: Przy wyznaczaniu granic bocznych stosowana jest konwolucja z jądrem średniej kroczącej (`moving average window`), co pozwala na eliminację szumów wysokoczęstotliwościowych i stabilizację detekcji marginesów\[cite: 11].

3\.  \*\*Rekursywne Kadrowanie\*\*: Funkcja `crop\_ecg` wykonuje kaskadowe wywołania detekcji, co pozwala na precyzyjne dostrojenie obszaru roboczego po wstępnym usunięciu nagłówków\[cite: 9].



\## 3. Implementacja Techniczna



Moduł integruje się z pipeline'em przetwarzania jako etap końcowej optymalizacji danych:

```python

from .cropping\_module import crop\_ecg



\# Automatyczna izolacja obszaru sygnału

processed\_signal\_area = crop\_ecg(input\_image)



\# Wynikowy obraz zawiera wyłącznie zrektyfikowany i odszumiony geometrycznie przebieg

