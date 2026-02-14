
# organic_cat.py
from spectral_studio import SpectralStudio
import numpy as np
import librosa

studio = SpectralStudio(sr=44100)
def load_brush(name): return np.load(f"brushes/{name}.npy")

print("🐈 ORGANIC CAT REPLICATOR")

# 1. THE K (Natural - No Filter)
k_raw = load_brush("K")
# Precise timing from our DNA scan
k_sculpt = studio.extract(k_raw, 0, 0.12, fade_sec=0.01)
# No filter here - we want the full spectrum. Griffin-Lim will fix the phase.
k_sculpt = k_sculpt * 8.0

# 2. THE A (Natural)
ah_raw = load_brush("Ah")
ah_sculpt = studio.extract(ah_raw, 0.02, 0.24, fade_sec=0.02)

# 3. THE T (Natural)
t_raw = load_brush("T")
t_sculpt = studio.extract(t_raw, 0, 0.08, fade_sec=0.005)
t_sculpt = t_sculpt * 6.0

# 4. CONSTRUCTION (Precise Overlap)
canvas = studio.create_canvas(1.0)

# Timings from DNA scan
canvas = studio.paste(canvas, k_sculpt, 0.17)
canvas = studio.paste(canvas, ah_sculpt, 0.28) # 10ms Overlap
canvas = studio.paste(canvas, t_sculpt, 0.52) 

# This will trigger Griffin-Lim Phase Reconstruction
studio.save(canvas, "ORGANIC_CAT.wav")
print("✅ Organic Reconstruction Complete: ORGANIC_CAT.wav")
