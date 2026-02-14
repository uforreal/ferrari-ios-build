
# auto_tuner.py
from spectral_studio import SpectralStudio
import numpy as np
import librosa
import os

studio = SpectralStudio(sr=44100)

def load_brush(name):
    return np.load(f"brushes/{name}.npy")

def get_target_spectrogram(path):
    y, sr = librosa.load(path, sr=44100)
    y, _ = librosa.effects.trim(y)
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    return S

def synthesize_candidate(params):
    # params: k_boost, a_boost, t_boost, ka_start, at_start
    k_boost, a_boost, t_boost, ka_start, at_start = params
    
    # 1. Prepare Brushes
    k_raw = load_brush("K")
    k_sculpt = studio.extract(k_raw, 0, 0.12, fade_sec=0.01) * k_boost
    
    ah_raw = load_brush("Ah")
    ah_sculpt = studio.extract(ah_raw, 0.02, 0.24, fade_sec=0.02) * a_boost
    
    t_raw = load_brush("T")
    t_sculpt = studio.extract(t_raw, 0, 0.08, fade_sec=0.005) * t_boost
    
    # 2. Build Canvas
    canvas = studio.create_canvas(1.0)
    
    # K Baseline at 0.17
    canvas = studio.paste(canvas, k_sculpt, 0.17)
    # A relative to K
    canvas = studio.paste(canvas, ah_sculpt, ka_start)
    # T relative to A
    canvas = studio.paste(canvas, t_sculpt, at_start)
    
    return np.abs(canvas)

def calculate_loss(candidate_S, target_S):
    # Match shapes by padding/clipping
    min_w = min(candidate_S.shape[1], target_S.shape[1])
    # Compare energy distribution
    diff = np.mean((candidate_S[:, :min_w] - target_S[:, :min_w])**2)
    return diff

print("🚀 STARTING GENETIC AUTO-TUNER")
target_S = get_target_spectrogram("Teacher_CAT.wav")

best_loss = float('inf')
best_params = None

# Grid Search / Random Walk
# We search for the perfect placement
for i in range(100):
    # params: k_boost, a_boost, t_boost, ka_start, at_start
    p = [
        np.random.uniform(4, 10),    # k_boost
        np.random.uniform(0.5, 2),   # a_boost
        np.random.uniform(2, 8),     # t_boost
        np.random.uniform(0.20, 0.35), # ka_start (Teacher was 0.27)
        np.random.uniform(0.45, 0.65)  # at_start (Teacher was 0.56)
    ]
    
    cand_S = synthesize_candidate(p)
    loss = calculate_loss(cand_S, target_S)
    
    if loss < best_loss:
        best_loss = loss
        best_params = p
        print(f"   Iteration {i}: New Best Loss! ({loss:.4f})")

print("\n🏆 OPTIMIZATION COMPLETE")
print(f"Optimal Timing: K -> {best_params[3]:.3f}s, A -> {best_params[4]:.3f}s")

# Final Synthesis with winner
k_raw = load_brush("K")
k_sculpt = studio.extract(k_raw, 0, 0.12, fade_sec=0.01) * best_params[0]
ah_raw = load_brush("Ah")
ah_sculpt = studio.extract(ah_raw, 0.02, 0.24, fade_sec=0.02) * best_params[1]
t_raw = load_brush("T")
t_sculpt = studio.extract(t_raw, 0, 0.08, fade_sec=0.005) * best_params[2]

final_canvas = studio.create_canvas(1.0)
studio.paste(final_canvas, k_sculpt, 0.17)
studio.paste(final_canvas, ah_sculpt, best_params[3])
studio.paste(final_canvas, t_sculpt, best_params[4])

studio.save(final_canvas, "Physics_CAT_FINAL.wav")
print("✅ Best version saved as Physics_CAT_FINAL.wav")
