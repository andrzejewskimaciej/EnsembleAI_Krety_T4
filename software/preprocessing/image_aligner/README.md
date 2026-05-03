# Moduł Korekcji Geometrycznej i Rektyfikacji Obrazu

Niniejszy komponent stanowi dedykowany podsystem w strukturze większego projektu, odpowiadający za wstępne przetwarzanie (preprocessing) i normalizację orientacji przestrzennej danych wizualnych.

## Rola modułu w systemie

Moduł ten został zaprojektowany jako krytyczny etap pośredni między akwizycją obrazu a właściwą analizą semantyczną (np. OCR, segmentacja obiektów). Jego głównym zadaniem jest eliminacja błędu nachylenia (skewness error), co znacząco podnosi precyzję kolejnych warstw analitycznych systemu.

### Architektura plików składowych:

*   **`__init__.py`**: Definiuje interfejs programistyczny modułu, eksponując funkcję `straighten_image` jako główny punkt dostępowy.
*   **`detection.py`**: Implementuje warstwę ekstrakcji cech, wykorzystującą filtrację Canny’ego oraz transformację Hougha do izolacji prymitywów geometrycznych.
*   **`geometry.py`**: Stanowi rdzeń obliczeniowy dla estymacji parametrów rotacji na podstawie rozkładu wektorów krawędziowych.
*   **`transform.py`**: Odpowiada za operacje na macierzach obrazu, realizując transformację afiniczną w przestrzeni RGBA.
*   **`straighten_image.py`**: Pełni rolę kontrolera procesu, implementując logikę sterowania przepływem danych między podmodułami.

## Metodologia i algorytmika

Proces rektyfikacji realizowany jest przez funkcję `straighten_image` i przebiega w sposób wieloetapowy:

1.  **Analiza Hougha**: System identyfikuje zbiór linii o wysokiej ufności. Algorytm charakteryzuje się adaptacyjnością – w przypadku braku wystarczającej liczby cech horyzontalnych (min. 25% wymiaru), automatycznie rekalibruje progi detekcji do wartości 10%.
2.  **Filtracja kierunkowa**: W celu uniknięcia błędów wynikających z obecności pionowych elementów strukturalnych, system dokonuje selekcji wyłącznie tych linii, dla których $|\Delta x| > |\Delta y|$.
3.  **Estymacja $\alpha$**: Kąt rotacji wyznaczany jest poprzez uśrednienie współczynników nachylenia wyselekcjonowanych linii, co minimalizuje wpływ lokalnych zakłóceń obrazu.
4.  **Transformacja bezstratna**: Wykorzystanie macierzy rotacji 2D wraz z korektą translacji ($M[0, 2]$ i $M[1, 2]$) pozwala na zachowanie pełnego pola obrazowania bez artefaktów przycięcia.
