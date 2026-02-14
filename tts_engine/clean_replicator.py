
# clean_replicator.py
from spectral_studio import SpectralStudio
import numpy as np
import librosa

studio = SpectralStudio(sr=44100)
def load_brush(name): return np.load(f"brushes/{name}.npy")

print("🧹 CLEAN REPLICATOR ACTIVE")

# 1. THE K (CLEANED)
k_raw = load_brush("K")
k_sculpt = studio.extract(k_raw, 0, 0.12, fade_sec=0.01)
# REMOVE VOWEL RESIDUE (Anything below 3000Hz)
k_sculpt = studio.high_pass(k_sculpt, 3000)
# BOOST (Physics scan said K starts quiet, we boost it)
k_sculpt = k_sculpt * 8.0

# 2. THE A (NATURAL)
ah_raw = load_brush("Ah")
ah_sculpt = studio.extract(ah_raw, 0.02, 0.24, fade_sec=0.02)
# Keep it rich

# 3. THE T (CLEANED)
t_raw = load_brush("T")
t_sculpt = studio.extract(t_raw, 0, 0.08, fade_sec=0.005)
# REMOVE VOWEL RESIDUE (Anything below 4000Hz for sharpness)
t_sculpt = studio.high_pass(t_sculpt, 4000)
t_sculpt = t_sculpt * 6.0

# 4. CONSTRUCTION (Precise timings from Teacher)
canvas = studio.create_canvas(1.0)

# Placement based on your successful 'Auto Tuner' result (approx)
canvas = studio.paste(canvas, k_sculpt, 0.17)
canvas = studio.paste(canvas, ah_sculpt, 0.28) # Overlap
canvas = studio.paste(canvas, t_sculpt, 0.52) # Close

studio.save(canvas, "CLEAN_CAT.wav")
print("✅ Forensic Clean Complete: CLEAN_CAT.wav")
