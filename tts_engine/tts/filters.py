
import numpy as np
from scipy.signal import lfilter

def get_resonator_coeffs(F, B, sample_rate):
    """
    Calculate coefficients for a 2-pole resonator.
    Returns bandpass-like filter centered at F with bandwidth B.
    """
    # Pole radius (determines bandwidth)
    r = np.exp(-np.pi * B / sample_rate)
    
    # Pole angle (determines center frequency)
    theta = 2 * np.pi * F / sample_rate
    
    # Coefficients for IIR filter
    a1 = 2 * r * np.cos(theta)
    a2 = -r * r
    
    # Gain normalization for unity peak at center frequency
    # For a resonator, gain at F should be 1.0
    # Simplified: use (1 - r*r) as a rough gain factor
    b0 = (1 - r * r) * 0.5
    
    return [b0], [1, -a1, -a2]

def apply_formants(signal, formants, bandwidths, sample_rate):
    """
    Apply PARALLEL formant filters (sum of resonators).
    This preserves energy across the spectrum unlike cascade.
    
    formants: [F1, F2, F3, ...]
    bandwidths: [B1, B2, B3, ...]
    """
    if len(signal) == 0:
        return signal
    
    # Parallel: sum the outputs of each formant filter
    result = np.zeros_like(signal)
    
    # Weights: F1 is loudest, F2/F3 progressively quieter
    weights = [1.0, 0.5, 0.25]
    
    for i, (F, B) in enumerate(zip(formants, bandwidths)):
        if F > 0 and B > 0:
            b, a = get_resonator_coeffs(F, B, sample_rate)
            filtered = lfilter(b, a, signal)
            
            # Apply weight
            w = weights[i] if i < len(weights) else 0.15
            result += filtered * w
    
    return result
