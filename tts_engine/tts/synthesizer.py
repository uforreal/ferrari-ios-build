
import numpy as np
import sys
import os
from .phoneme_bank import PHONEMES
from .humanizer import Humanizer
from .transitions import build_formant_trajectory
from scipy.signal import resample

# Add tdklatt to path
TDKLATT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tdklatt")
if TDKLATT_PATH not in sys.path:
    sys.path.append(TDKLATT_PATH)

try:
    import tdklatt
except ImportError:
    print("CRITICAL: tdklatt not found. Please ensure tdklatt directory exists.")

class Synthesizer:
    """
    Klatt-Based Synthesizer Wrapper.
    Uses tdklatt for high-quality parametric synthesis.
    """
    
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        self.internal_fs = 10000 # tdklatt default
        self.base_pitch = 110
        self.humanizer = Humanizer()
        
    def synthesize_continuous(self, phonemes, pitch_contour=None, speed=1.0):
        """
        Synthesize speech using tdklatt's Klatt 1980 model.
        """
        # 1. Build trajectories at internal_fs
        traj = build_formant_trajectory(phonemes, PHONEMES, self.internal_fs, speed=speed)
        n_samples = traj["total_samples"]
        
        if n_samples == 0:
            return np.zeros(1, dtype=np.float32)
            
        # 2. Setup tdklatt parameters
        p = tdklatt.KlattParam1980(FS=self.internal_fs, DUR=n_samples/self.internal_fs)
        
        # Fundamental Frequency
        if pitch_contour is not None:
            # Resample pitch contour from engine rate to internal_fs
            if len(pitch_contour) != n_samples:
                # We need to scale pitch_contour to n_samples
                indices = np.linspace(0, len(pitch_contour)-1, n_samples)
                p.F0 = np.interp(indices, np.arange(len(pitch_contour)), pitch_contour)
            else:
                p.F0 = pitch_contour
        else:
            p.F0 = np.ones(n_samples) * self.base_pitch
            
        # Formants
        p.FF = [traj["f1"], traj["f2"], traj["f3"], traj["f4"], traj["f5"]]
        p.BW = [traj["b1"], traj["b2"], traj["b3"], traj["b4"], traj["b5"]]
        
        
        # Voicing Source (AV)
        # Directly use the trajectory calculated by transitions.py
        from scipy.ndimage import gaussian_filter1d
        
        # A small amount of smoothing helps blend the linear/cosine segments
        # sigma=20 samples (~2ms at 10k) is minimal but removing zipper noise
        p.AV = gaussian_filter1d(traj["av"], sigma=20)
        
        # Noise Sources (AH - Aspiration / AF - Frication)
        p.AH = gaussian_filter1d(traj["ah"], sigma=20)
        p.AF = gaussian_filter1d(traj["af"], sigma=20)
        
        # Parallel Amplitudes (A1-A6)
        # In cascade mode (default), these aren't used as much, 
        # but let's set A1 = AV for parallel branches if active
        p.A1 = p.AV 

        
        # 3. Create and run Synth
        s = tdklatt.klatt_make(p)
        s.run()
        
        # 4. Post-processing
        output = s.output
        
        # Normalize
        peak = np.max(np.abs(output))
        if peak > 0:
            output = output / peak * 0.8
            
        # Resample to engine's sample rate
        if self.sample_rate != self.internal_fs:
            num_samples = int(len(output) * self.sample_rate / self.internal_fs)
            output = resample(output, num_samples)
            
        return output.astype(np.float32)

    def synthesize_phoneme(self, phoneme, pitch=None, duration_override=None):
        return self.synthesize_continuous([phoneme])
    
    def synthesize_sequence(self, phonemes, pitches=None):
        return self.synthesize_continuous(phonemes)
