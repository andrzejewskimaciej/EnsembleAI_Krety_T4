\# Moduł Korekcji Geometrycznej i Rektyfikacji Obrazu



Niniejszy komponent stanowi dedykowany podsystem w strukturze większego projektu, odpowiadający za wstępne przetwarzanie (preprocessing) i normalizację orientacji przestrzennej danych wizualnych.



\## Rola modułu w systemie



Moduł ten został zaprojektowany jako krytyczny etap pośredni między akwizycją obrazu a właściwą analizą semantyczną (np. OCR, segmentacja obiektów). Jego głównym zadaniem jest eliminacja błędu nachylenia (skewness error), co znacząco podnosi precyzję kolejnych warstw analitycznych systemu.



\### Architektura plików składowych:

\*   \*\*`\_\_init\_\_.py`\*\*: Definiuje interfejs programistyczny modułu, eksponując funkcję `straighten\_image` jako główny punkt dostępowy\[cite: 1].

\*   \*\*`detection.py`\*\*: Implementuje warstwę ekstrakcji cech, wykorzystującą filtrację Canny’ego oraz transformację Hougha do izolacji prymitywów geometrycznych\[cite: 2].

\*   \*\*`geometry.py`\*\*: Stanowi rdzeń obliczeniowy dla estymacji parametrów rotacji na podstawie rozkładu wektorów krawędziowych\[cite: 3].

\*   \*\*`transform.py`\*\*: Odpowiada za operacje na macierzach obrazu, realizując transformację afiniczną w przestrzeni RGBA.

\*   \*\*`straighten\_image.py`\*\*: Pełni rolę kontrolera procesu, implementując logikę sterowania przepływem danych między podmodułami\[cite: 4].



\## Metodologia i algorytmika



Proces rektyfikacji realizowany jest przez funkcję `straighten\_image` i przebiega w sposób wieloetapowy:



1\.  \*\*Analiza Hougha\*\*: System identyfikuje zbiór linii o wysokiej ufności. Algorytm charakteryzuje się adaptacyjnością – w przypadku braku wystarczającej liczby cech horyzontalnych (min. 25% wymiaru), automatycznie rekalibruje progi detekcji do wartości 10%\[cite: 2, 4].

2\.  \*\*Filtracja kierunkowa\*\*: W celu uniknięcia błędów wynikających z obecności pionowych elementów strukturalnych, system dokonuje selekcji wyłącznie tych linii, dla których $|\\Delta x| > |\\Delta y|$\[cite: 2].

3\.  \*\*Estymacja $\\alpha$\*\*: Kąt rotacji wyznaczany jest poprzez uśrednienie współczynników nachylenia wyselekcjonowanych linii, co minimalizuje wpływ lokalnych zakłóceń obrazu\[cite: 3].

4\.  \*\*Transformacja bezstratna\*\*: Wykorzystanie macierzy rotacji 2D wraz z korektą translacji (M\[0, 2] i M\[1, 2]) pozwala na zachowanie pełnego pola obrazowania bez artefaktów przycięcia.



