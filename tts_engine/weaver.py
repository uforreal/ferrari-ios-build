
# weaver.py v8 - THE HUMAN VERSION
from spectral_studio import SpectralStudio
import numpy as np
import librosa

studio = SpectralStudio(sr=44100)
def load_brush(name): return np.load(f"brushes/{name}.npy")

print("🧶 VOCAL WEAVER V8 - THE HUMAN VERSION (3500Hz Target)")

# 1. THE K (Burst at 0.012s)
k_raw = load_brush("K")
# Precise extraction of the real burst
k_sculpt = studio.extract(k_raw, 0.012, 0.08, fade_sec=0.005)
# NATURAL BOOST (15x to overcome Rachel's low recording volume)
k_sculpt = k_sculpt * 15.0 

# 2. THE A (The Bridge)
ah_raw = load_brush("Ah")
# Stable core
ah_sculpt = studio.extract(ah_raw, 0.05, 0.22, fade_sec=0.02)

# 3. THE T (The Cap)
t_raw = load_brush("T")
t_sculpt = studio.extract(t_raw, 0, 0.06, fade_sec=0.005)
t_sculpt = t_sculpt * 10.0

# 4. CONSTRUCTION
canvas = studio.create_canvas(0.6)

# We use a tight timeline (0.1s start)
cursor = 0.1
canvas = studio.paste(canvas, k_sculpt, cursor)

# A starts exactly when K ends for 'Cat'
# 0.1s + 0.08s = 0.18s. Let's overlap by 10ms for glue.
canvas = studio.paste(canvas, ah_sculpt, 0.17, fade_in_sec=0.02)

# T with closure (0.17 + 0.22 = 0.39. 40ms closure = 0.43)
canvas = studio.paste(canvas, t_sculpt, 0.43)

# SAVE - NO VACUUM! Reconstruct phase naturally.
studio.save(canvas, "PURE_CAT.wav")
print("✅ Human Alignment Complete: PURE_CAT.wav")
