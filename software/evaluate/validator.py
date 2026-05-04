import numpy as np

def validate_submission(npz_filepath):
    print(f"--- Sprawdzanie pliku: {npz_filepath} ---")
    try:
        data = np.load(npz_filepath)
    except Exception as e:
        print(f"❌ Błąd wczytywania pliku: {e}")
        return False

    keys = data.files
    print(f"Znaleziono {len(keys)} wektorów sygnałów.\n")

    if len(keys) == 0:
        print("❌ Plik jest pusty!")
        return False

    errors = 0
    for i, key in enumerate(keys):
        signal = data[key]

        # 1. Sprawdzenie nazewnictwa kluczy
        if '_' not in key:
            print(f"❌ Błąd w kluczu '{key}': Brak znaku podkreślenia.")
            errors += 1

        # 2. Sprawdzenie kształtu (musi być 1D)
        if len(signal.shape) != 1:
            print(f"❌ Błąd w kluczu '{key}': Sygnał nie jest jednowymiarowy!")
            errors += 1

        # 3. Sprawdzenie typu danych
        if not np.issubdtype(signal.dtype, np.floating):
            print(f"❌ Błąd w kluczu '{key}': Dane to nie float (mV), lecz {signal.dtype}")
            errors += 1

    if errors == 0:
        print("\n🎉 Sukces! Struktura pliku wygląda na w 100% poprawną.")
        return True
    else:
        print(f"\n⚠️ Znaleziono {errors} błędów w strukturze. Popraw je przed wysłaniem.")
        return False