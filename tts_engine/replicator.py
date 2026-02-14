
# replicator.py
from spectral_studio import SpectralStudio
import numpy as np

studio = SpectralStudio(sr=44100)
def load_brush(name): return np.load(f"brushes/{name}.npy")

print("📠 Replicator Online.")

# Recipe derived from Teacher Analysis
# K volume: 0.012 -> Normalize to 1.0
# T volume: 0.028 -> Is 2.3x louder than K
# A duration: 0.37s

print("   Configuring DNA from Blueprint...")
duration_k = 0.05
duration_a = 0.37
duration_t = 0.05

gap_ka = 0.00 # Zero gap
gap_at = 0.00 # Zero gap

# 1. K (Standardized)
k_full = load_brush("K")
# Smart Slice (first 5 frames)
k_brush = k_full[:, 0:5] 
# Normalize volume
k_brush = k_brush / (np.max(np.abs(k_brush)) + 1e-6)

# 2. A (Stretched?)
ah_full = load_brush("Ah")
# We need 0.37s of A.
# Is our brush long enough?
# Check length
ah_len_sec = (ah_full.shape[1] * 512) / 44100
print(f"   Ah Brush Length: {ah_len_sec:.2f}s (Needed: {duration_a:.2f}s)")

if ah_len_sec < duration_a:
    print("   Extension required (Looping Ah)...")
    # Take the stable center and repeat it?
    # Or just use what we have.
    ah_brush = studio.extract(ah_full, 0.0, ah_len_sec, fade_sec=0.01)
else:
    ah_brush = studio.extract(ah_full, 0.05, duration_a + 0.05, fade_sec=0.01)

# Normalize A to be louder than K (Vowels are usually louder)
ah_brush = ah_brush / (np.max(np.abs(ah_brush)) + 1e-6)
ah_brush = ah_brush * 2.0 # Vowel dominance

# 3. T (Boosted)
t_full = load_brush("T")
t_brush = studio.extract(t_full, 0.0, 0.04, fade_sec=0.005)
t_brush = t_brush / (np.max(np.abs(t_brush)) + 1e-6)
t_brush = t_brush * 2.3 # Match Teacher ratio (ish)

# 4. Stitch
canvas = studio.create_canvas(0.6)

cursor = 0.05
canvas = studio.paste(canvas, k_brush, cursor)
cursor += 0.05 # K duration (approx)

canvas = studio.paste(canvas, ah_brush, cursor)
cursor += duration_a # The Blueprint Duration

canvas = studio.paste(canvas, t_brush, cursor)

studio.save(canvas, "Replica_CAT.wav")
print("Done: Replica_CAT.wav")
