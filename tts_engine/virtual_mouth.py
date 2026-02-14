
# virtual_mouth.py
import librosa
import numpy as np
import scipy.signal as signal
from spectral_studio import SpectralStudio

studio = SpectralStudio(sr=44100)

def create_vocal_filter(mag, f1, f2, f3, bandwidth=100):
    """Creates a 'Human Mouth' filter shape at a specific moment"""
    freqs = librosa.fft_frequencies(sr=44100, n_fft=2048)
    # Start with a baseline 'Identity' (Rachel's raw energy)
    # We apply resonant peaks (Formants) to the magnitude
    filter_shape = np.ones_like(freqs)
    
    for f in [f1, f2, f3]:
        # Simple Gaussian resonant peak
        peak = np.exp(-((freqs - f)**2) / (2 * bandwidth**2))
        filter_shape += peak * 10.0 # Boost the resonance
        
    return mag * filter_shape

print("🧬 VIRTUAL MOUTH ENGINE: PHYSICAL TRAJECTORY MODE")

# 1. LOAD RACHEL'S SOUL (The raw vibration)
# We use 'Ah' as the base for the whole word
ah_raw = np.load("brushes/Ah.npy")
mag_ah = np.abs(ah_raw)
phase_ah = np.angle(ah_raw)

# 2. DESIGN THE 'CAT' TRAJECTORY
# Words are defined by Formant F1, F2, F3 movements
# For 'CAT':
# - K start: F1=300, F2=2000 (Pinched)
# - Anchor A: F1=800, F2=1300 (Open)
# - T end: F1=400, F2=1800 (Closed)

frames = 80 # Total duration of the word (approx 0.8s)
new_spec = np.zeros((1025, frames), dtype=complex)

print("   [!] Simulating Physical Transitions...")

for i in range(frames):
    progress = i / frames
    
    # DYNAMIC MOUTH MOVEMENT (The Slide)
    if progress < 0.2: # THE K BURST (Constriction)
        f1, f2, f3 = 200, 2400, 3000
        vol = progress * 2 # Rising energy
    elif progress < 0.7: # THE A VOWEL (Opening)
        # Morphs from 0.2 to 0.7
        sub_p = (progress - 0.2) / 0.5
        f1 = 300 + (500 * sub_p) # F1 opens up
        f2 = 2400 - (1000 * sub_p) # F2 drops
        f3 = 3000
        vol = 1.0
    else: # THE T STOP (Closing)
        sub_p = (progress - 0.7) / 0.3
        f1 = 800 - (400 * sub_p)
        f2 = 1400 + (400 * sub_p)
        f3 = 3000
        vol = (1.0 - sub_p) # Fading out for the closure
        
    # APPLY RACHEL'S IDENTITY TO THE FILTER
    # Take a snippet of Rachel's Ah and shape it with the mouth
    rachel_sample = mag_ah[:, i % mag_ah.shape[1]]
    shaped_mag = create_vocal_filter(rachel_sample, f1, f2, f3)
    
    # Recombine with identity phase
    new_spec[:, i] = (shaped_mag * vol) * np.exp(1j * phase_ah[:, i % phase_ah.shape[1]])

# 3. RENDER THE EXPERIMENT
studio.save(new_spec, "VIRTUAL_CAT.wav")
print("✅ First 'Living' Reconstruction Complete: VIRTUAL_CAT.wav")
