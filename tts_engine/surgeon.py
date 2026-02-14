
# surgeon.py v8 - The Blend
from spectral_studio import SpectralStudio
import numpy as np
import librosa

studio = SpectralStudio(sr=44100)
def load_brush(name): return np.load(f"brushes/{name}.npy")

print("Surgery v8 - The Blend.")

# 1. Reuse Smart K
k_full = load_brush("K")
k_audio = librosa.istft(k_full, hop_length=studio.hop_length, n_fft=studio.n_fft)
onsets = librosa.onset.onset_detect(y=k_audio, sr=44100, units='frames')
if len(onsets) > 0:
    first_onset = onsets[0]
    # Grab just the BURST (3 frames)
    k_smart = k_full[:, max(0, first_onset-1):first_onset+2]
    k_smart = k_smart * 8.0 # Normalize/Boost
else:
    k_smart = k_full[:, 0:3] * 8.0

# 2. Ah (Attack Phase)
ah_full = load_brush("Ah")
# Extract the very start of Ah (0.02 to 0.15)
ah_head = studio.extract(ah_full, 0.02, 0.15, fade_sec=0.01)

# 3. T (Pop)
t_full = load_brush("T")
t_pop = studio.extract(t_full, 0.0, 0.04, fade_sec=0.005)
t_pop = t_pop * 3.0

# 4. Stitch
# K ends. Ah begins instantly. T begins instantly after Ah.
canvas = studio.create_canvas(0.5)

cursor = 0.05
# Paste K
canvas = studio.paste(canvas, k_smart, cursor)

# Move cursor by K width (frames -> seconds)
k_dur = librosa.frames_to_time(k_smart.shape[1], sr=44100, hop_length=studio.hop_length)
cursor += k_dur

# Paste Ah (Zero Gap)
canvas = studio.paste(canvas, ah_head, cursor)

# Move cursor by Ah width
ah_dur = librosa.frames_to_time(ah_head.shape[1], sr=44100, hop_length=studio.hop_length)
cursor += ah_dur

# Paste T
canvas = studio.paste(canvas, t_pop, cursor)

studio.save(canvas, "Surgery_CAT_v8_BLEND.wav")
print("Done: Surgery_CAT_v8_BLEND.wav")
