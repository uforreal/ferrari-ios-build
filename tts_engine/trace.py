
"""
DEEP SIGNAL TRACE - Follow the signal through each processing stage.
"""

import numpy as np
from tts.source import glottal_pulse
from tts.filters import apply_formants
from tts.phoneme_bank import PHONEMES

sample_rate = 22050
duration = 0.4
pitch = 130

def analyze(name, signal):
    peak = np.max(np.abs(signal))
    rms = np.sqrt(np.mean(signal**2))
    print(f"  {name}: Peak={peak:.4f}, RMS={rms:.4f}")
    return signal

print("="*60)
print("TRACING /i/ (PROBLEM PHONEME - Low F1, High F2)")
print("="*60)

# Step 1: Source
source = glottal_pulse(duration, pitch, sample_rate, jitter=0)
analyze("1. Glottal Source", source)

# Step 2: Formants for /i/
p = PHONEMES["i"]
print(f"   Formants: {p['f']}, Bandwidths: {p['b']}")
filtered = apply_formants(source, p["f"], p["b"], sample_rate)
analyze("2. After Formants", filtered)

# Step 3: Normalization
peak = np.max(np.abs(filtered))
if peak > 0.001:
    normalized = filtered / peak
else:
    normalized = filtered
    print("   ⚠️ PEAK TOO LOW TO NORMALIZE!")
analyze("3. After Normalize", normalized)

# Step 4: Lip Radiation
radiated = np.append(normalized[0], normalized[1:] - 0.95 * normalized[:-1])
analyze("4. After Lip Radiation", radiated)

print("\n" + "="*60)
print("TRACING /ɑ/ (GOOD PHONEME - High F1, Low F2)")
print("="*60)

source = glottal_pulse(duration, pitch, sample_rate, jitter=0)
analyze("1. Glottal Source", source)

p = PHONEMES["ɑ"]
print(f"   Formants: {p['f']}, Bandwidths: {p['b']}")
filtered = apply_formants(source, p["f"], p["b"], sample_rate)
analyze("2. After Formants", filtered)

peak = np.max(np.abs(filtered))
if peak > 0.001:
    normalized = filtered / peak
else:
    normalized = filtered
    print("   ⚠️ PEAK TOO LOW!")
analyze("3. After Normalize", normalized)

radiated = np.append(normalized[0], normalized[1:] - 0.95 * normalized[:-1])
analyze("4. After Lip Radiation", radiated)
