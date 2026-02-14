
# prosody.py

import numpy as np

class ProsodyEngine:
    """Generate natural pitch contours."""
    
    def __init__(self, base_pitch=120, sample_rate=22050):
        self.base_pitch = base_pitch
        self.sample_rate = sample_rate
    
    def generate_pitch_contour(self, phonemes, total_samples, sentence_type="statement"):
        """
        Generate F0 (pitch) curve for utterance.
        
        sentence_type: "statement", "question", "exclamation"
        """
        pitch = np.ones(total_samples) * self.base_pitch
        
        # Base contour depends on sentence type
        t = np.linspace(0, 1, total_samples)
        
        if sentence_type == "statement":
            # Gentle fall: start slightly high, end lower
            contour = 1.1 - 0.2 * t
        elif sentence_type == "question":
            # Rise at the end
            contour = 1.0 - 0.1 * t + 0.3 * (t ** 3)
        elif sentence_type == "exclamation":
            # Higher energy, slight fall
            contour = 1.2 - 0.15 * t
        else:
            contour = np.ones(total_samples)
        
        pitch = pitch * contour
        
        # Add micro-variations (jitter for naturalness)
        # Slow drift (0.5 Hz)
        drift = np.sin(2 * np.pi * 0.5 * np.arange(total_samples) / self.sample_rate)
        pitch = pitch * (1 + drift * 0.02)
        
        # Fast micro-jitter
        jitter = np.random.uniform(-0.01, 0.01, total_samples)
        # Smooth it
        from scipy.ndimage import uniform_filter1d
        jitter = uniform_filter1d(jitter, size=200)
        pitch = pitch * (1 + jitter)
        
        return pitch
    
    def add_stress(self, pitch, phonemes, stress_pattern=None):
        """
        Add stress (emphasis) to certain syllables.
        
        Stressed syllables: higher pitch, longer duration
        """
        # Simple heuristic: stress first syllable of content words
        # For now, just add slight pitch bumps periodically
        
        bump_interval = len(pitch) // (len(phonemes) // 3 + 1)
        
        for i in range(0, len(pitch), bump_interval):
            # Create a pitch bump
            bump_width = min(2000, len(pitch) - i)
            bump = np.hanning(bump_width) * 0.1 * self.base_pitch
            pitch[i:i+bump_width] += bump[:len(pitch)-i] if i + bump_width > len(pitch) else bump
        
        return pitch
