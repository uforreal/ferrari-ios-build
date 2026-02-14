
import numpy as np

def glottal_pulse(duration_sec, f0, sample_rate, jitter=0.0):
    """
    Generate band-limited sawtooth waverform (rich harmonics).
    """
    t = np.arange(int(duration_sec * sample_rate)) / sample_rate
    
    # generate phase with jitter
    phases = 2 * np.pi * f0 * t
    
    # Add jitter to phase integral if needed, but for now let's keep it simple for clarity
    # Simple sawtooth: 2 * (t * f0 - floor(t * 0.5 + f0)) ...
    # Let's use scipy.signal.sawtooth if we could, but we can generate it raw
    
    # Basic Sawtooth (Harmonics decay at -6dB/oct)
    # signal = 2 * (t * f0 - np.floor(t * f0 + 0.5)) 
    
    # Band-limited approximation (sum of sines) is too slow.
    # Let's use a naive sawtooth but smooth the discontinuity slightly to avoid severe aliasing
    
    # Actually, a simple impulse train is best for formant synthesis, 
    # but sawtooth is "buzzier" and louder.
    
    # Let's use a periodic sinc (BLIT) or just a really sharp pulse? 
    # Let's stick to the classic "Rosenberg C" but make it sharper.
    
    # NEW IMPLEMENTATION: Sharper Pulse (Rosenberg-ish)
    period_samples = int(sample_rate / f0)
    output = np.zeros(len(t))
    
    pulse_len = int(period_samples * 0.6) # 60% duty cycle
    if pulse_len < 1: pulse_len = 1
    
    for i in range(0, len(t), period_samples):
        # Add random jitter to period length for next cycle
        current_p = int(period_samples * (1 + np.random.uniform(-jitter, jitter)))
        if current_p < 5: current_p = 5
        
        # Draw ONE pulse
        # Simple triangular/parabolic pulse for rich spectrum
        # 0 -> 1 -> 0
        
        # A simple impulse is 1, 0, 0...
        # A simple sawtooth is 1, 0.9, 0.8...
        
        # Let's do a Sawtooth-like shape for maximum harmonics
        # 1.0 down to -1.0
        
        # Check bounds
        end = min(i + current_p, len(t))
        length = end - i
        
        # Ramp from 1 to -1
        ramp = np.linspace(1, -1, length)
        
        # Attenuate edges to reduce clicking
        window = np.hanning(length)
        # Actually sawtooth doesn't window, it resets.
        # But naive sawtooth aliases.
        
        # Let's use a generated buzzing sound: simple sine^0.3? No.
        
        # Let's try: Naive Sawtooth for raw buzzy power.
        output[i:end] += ramp * 0.5
        
        # Note: changing loop step 'period_samples' is tricky if we vary 'current_p'.
        # We need a while loop.
        pass
    
    # Re-do with while loop for correct jitter
    output = np.zeros(len(t))
    i = 0
    phase = 0
    while i < len(t):
        current_f0 = f0 * (1 + np.random.uniform(-jitter, jitter))
        p_len = int(sample_rate / current_f0)
        if p_len < 2: p_len = 2
        
        end = min(i + p_len, len(t))
        length = end - i
        
        # SAWTOOTH: linearly decreasing from 0.8 to -0.8
        seg = np.linspace(0.8, -0.8, length)
        output[i:end] = seg
        
        i += p_len

    return output


def noise(duration_sec, sample_rate):
    """Generate white noise."""
    samples = int(duration_sec * sample_rate)
    return np.random.uniform(-1, 1, samples)


def bandpass_noise(duration_sec, sample_rate, low_hz, high_hz):
    """Generate bandpass filtered noise for fricatives."""
    from scipy.signal import butter, filtfilt
    
    samples = int(duration_sec * sample_rate)
    white = np.random.uniform(-1, 1, samples)
    
    # Bandpass filter
    nyquist = sample_rate / 2
    low = low_hz / nyquist
    high = min(high_hz / nyquist, 0.99)
    
    b, a = butter(4, [low, high], btype='band')
    filtered = filtfilt(b, a, white)
    
    return filtered / (np.max(np.abs(filtered)) + 0.001)
