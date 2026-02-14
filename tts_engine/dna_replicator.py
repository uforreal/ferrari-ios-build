
# dna_replicator.py v3 - Additive Blending & Overlap
from spectral_studio import SpectralStudio
import numpy as np
import librosa

studio = SpectralStudio(sr=44100)

def load_brush(name):
    return np.load(f"brushes/{name}.npy")

def apply_envelope(brush, target_env, boost=1.0):
    env = np.interp(np.linspace(0, 1, brush.shape[1]), np.linspace(0, 1, len(target_env)), target_env)
    return brush * (env * boost)

print("🧬 DNA REPLICATOR V3 - ADDITIVE BLENDING")

# 1. THE K
k_raw = load_brush("K")
# 0.12s duration
k_sculpt = studio.extract(k_raw, 0, 0.12, fade_sec=0.01)
k_env = [0.007, 0.014, 0.016, 0.018, 0.023, 0.022, 0.024]
k_sculpt = apply_envelope(k_sculpt, k_env, boost=6.0)

# 2. THE A
ah_raw = load_brush("Ah")
# 0.22s duration
ah_sculpt = studio.extract(ah_raw, 0.02, 0.24, fade_sec=0.02)
ah_env = [0.084, 0.142, 0.195, 0.176, 0.123, 0.083, 0.021]
ah_sculpt = apply_envelope(ah_sculpt, ah_env, boost=1.0)

# 3. THE T
t_raw = load_brush("T")
# 0.08s duration
t_sculpt = studio.extract(t_raw, 0, 0.08, fade_sec=0.005)
t_env = [0.018, 0.034, 0.041, 0.039, 0.027, 0.014]
t_sculpt = apply_envelope(t_sculpt, t_env, boost=4.0)

# 4. CONSTRUCTION (With Overlaps for Smooth Transitions)
canvas = studio.create_canvas(1.0)

# Timeline Strategy:
# K Start: 0.17s
# A Start: 0.27s (Overlaps K tail by 0.02s)
# T Start: 0.50s (Overlaps A tail by 0.01s)

canvas = studio.paste(canvas, k_sculpt, 0.17)
canvas = studio.paste(canvas, ah_sculpt, 0.27) # Overlap!
canvas = studio.paste(canvas, t_sculpt, 0.51) # Closure

# Final Render
studio.save(canvas, "Physics_CAT.wav")
print("✅ Additive DNA Replication Complete: Physics_CAT.wav")
