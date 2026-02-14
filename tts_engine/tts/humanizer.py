
import numpy as np
from scipy.ndimage import uniform_filter1d
from scipy.signal import butter, filtfilt

class Humanizer:
    """Add human-like imperfections during synthesis."""
    
    def __init__(self):
        # CLEAN ROBOT SETTINGS (High Intelligibility)
        self.jitter = 0.005        # Pitch wobble (0.5%)
        self.shimmer = 0.02        # Amplitude wobble (2%)  
        self.breathiness = 0.01    # Noise mixed in (1%)
        self.drift_speed = 0.1     # Hz
        self.drift_amount = 0.002  # Slow pitch drift
        
        self._drift_phase = 0
    
    def apply_shimmer(self, signal):
        """Add amplitude variation."""
        if self.shimmer <= 0: return signal
        
        wobble = 1 + np.random.uniform(-self.shimmer, self.shimmer, len(signal))
        # Smooth the wobble
        wobble = uniform_filter1d(wobble, size=100)
        return signal * wobble
    
    def add_breathiness(self, signal, sample_rate):
        """Mix in soft noise."""
        if self.breathiness <= 0: return signal
        
        breath = np.random.uniform(-1, 1, len(signal))
        # Low-pass filter the breath
        b, a = butter(2, 3000 / (sample_rate/2), btype='low')
        breath = filtfilt(b, a, breath)
        breath = breath / (np.max(np.abs(breath)) + 0.001)
        
        # Only add breath where there's signal
        envelope = np.abs(signal)
        envelope = uniform_filter1d(envelope, size=500)
        envelope = envelope / (np.max(envelope) + 0.001)
        
        return signal + breath * self.breathiness * envelope
    
    def get_pitch_drift(self, duration_sec, sample_rate):
        """Get slow pitch drift multiplier."""
        samples = int(duration_sec * sample_rate)
        t = np.arange(samples) / sample_rate
        drift = 1 + np.sin(2 * np.pi * self.drift_speed * t + self._drift_phase) * self.drift_amount
        self._drift_phase += duration_sec * self.drift_speed * 2 * np.pi
        return drift
