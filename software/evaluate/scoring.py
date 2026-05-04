import numpy as np
from scipy.stats import pearsonr
from scipy.signal import correlate

# --- 1. Funkcja: Kształt (Shape) ---
def score_shape(y_true, y_pred):
    """Oblicza wynik za kształt (max 60 pkt) przy użyciu korelacji Pearsona."""
    if np.isnan(y_pred).any() or np.isinf(y_pred).any():
        return 0.0
    if np.all(y_true == y_true[0]) or np.all(y_pred == y_pred[0]):
        return 0.0  # Zabezpieczenie przed płaską linią
    r, _ = pearsonr(y_true, y_pred)
    score = max(0.0, r) * 60.0
    return score

# --- 2. Funkcja: Amplituda (Amplitude) ---
def score_amplitude(y_true, y_pred, target_snr_db=15.0):
    """Oblicza wynik za amplitudę (max 20 pkt) bazując na Signal-to-Noise Ratio (SNR)."""
    if np.isnan(y_pred).any() or np.isinf(y_pred).any():
        return 0.0
    noise = y_true - y_pred
    power_signal = np.sum(y_true ** 2)
    power_noise = np.sum(noise ** 2)
    if power_noise == 0:
        return 20.0
    snr_db = 10 * np.log10(power_signal / power_noise)
    score = np.clip(snr_db / target_snr_db, 0.0, 1.0) * 20.0
    return score

# --- 3. Funkcja: Kalibracja Czasu (Time Calibration) ---
def score_time(y_true, y_pred, fs=500, max_shift_sec=0.2):
    """Oblicza wynik za kalibrację czasu (max 20 pkt)."""
    if np.isnan(y_pred).any() or np.isinf(y_pred).any():
        return 0.0
    correlation = correlate(y_true, y_pred, mode='full')
    lags = np.arange(-len(y_pred) + 1, len(y_true))
    best_lag_idx = np.argmax(correlation)
    shift_samples = abs(lags[best_lag_idx])
    shift_sec = shift_samples / fs
    penalty_ratio = min(shift_sec / max_shift_sec, 1.0)
    score = 20.0 * (1.0 - penalty_ratio)
    return score

# --- 4. Funkcja: Wynik dla pojedynczej próbki (Single Sample) ---
def calculate_single_sample_score(y_true_dict, y_pred_dict, fs=500):
    """Oblicza łączny wynik (max 100 pkt) dla pojedynczego rekordu."""
    leads = y_true_dict.keys()
    if not leads:
        return 0.0
    total_score_sum = 0.0
    for lead in leads:
        if lead not in y_pred_dict:
            continue
        y_t = np.array(y_true_dict[lead])
        y_p = np.array(y_pred_dict[lead])
        min_len = min(len(y_t), len(y_p))
        y_t_eval = y_t[:min_len]
        y_p_eval = y_p[:min_len]
        s_shape = score_shape(y_t_eval, y_p_eval)
        s_amp = score_amplitude(y_t_eval, y_p_eval)
        s_time = score_time(y_t_eval, y_p_eval, fs=fs)
        total_score_sum += (s_shape + s_amp + s_time)
    sample_score = total_score_sum / len(leads)
    return sample_score

# --- 5. Funkcja: Wynik dla całego zbioru (Dataset) ---
def calculate_dataset_score(dataset_true, dataset_pred, fs=500):
    """Oblicza uśredniony wynik dla całego zbioru testowego/walidacyjnego."""
    records = dataset_true.keys()
    if not records:
        return 0.0
    dataset_score_sum = 0.0
    processed_records = 0
    for record_id in records:
        if record_id in dataset_pred:
            y_true_dict = dataset_true[record_id]
            y_pred_dict = dataset_pred[record_id]
            record_score = calculate_single_sample_score(y_true_dict, y_pred_dict, fs)
            dataset_score_sum += record_score
            processed_records += 1
    final_dataset_score = dataset_score_sum / len(records)
    return final_dataset_score

def load_predictions_for_scoring(npz_filepath):
    """Wczytuje plik .npz i konwertuje na format wymagany przez calculate_dataset_score."""
    loaded_npz = np.load(npz_filepath)
    dataset_pred = {}
    for key in loaded_npz.files:
        if '_' not in key:
            continue
        record_id, lead_name = key.rsplit('_', 1)
        if record_id not in dataset_pred:
            dataset_pred[record_id] = {}
        dataset_pred[record_id][lead_name] = loaded_npz[key]
    return dataset_pred