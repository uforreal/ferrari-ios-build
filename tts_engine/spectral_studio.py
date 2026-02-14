
# spectral_studio.py
import librosa
import numpy as np
import soundfile as sf
import argparse

class SpectralStudio:
    def __init__(self, sr=44100, n_fft=2048, hop_length=512):
        self.sr = sr
        self.n_fft = n_fft
        self.hop_length = hop_length
    
    def load(self, path):
        """Load audio and convert to Complex Spectrogram"""
        print(f"Loading {path} @ {self.sr}Hz...")
        y, _ = librosa.load(path, sr=self.sr)
        D = librosa.stft(y, n_fft=self.n_fft, hop_length=self.hop_length)
        return D, y 
    
    def save(self, D, path):
        """Convert Spectrogram back to Audio"""
        # 1. Capture Magnitude
        magnitude = np.abs(D)
        
        # 2. Spectral Gating (The Vacuum)
        # Clearer threshold for high-fidelity transients
        threshold = np.max(magnitude) * 0.008
        magnitude[magnitude < threshold] = 0
        
        # 3. Phase Reconstruction (Griffin-Lim)
        print(f"   Reconstructing sharp transients...")
        # 48 iterations for maximum phase-alignment (kills the metallic zing)
        y = librosa.griffinlim(magnitude, hop_length=self.hop_length, n_fft=self.n_fft, n_iter=48)

        # Normalize to 0dB (Max Volume)
        peak = np.max(np.abs(y))
        if peak > 0:
            y = y / peak
        
        sf.write(path, y, self.sr)
        
    def find_islands(self, y):
        """Detect silence-separated islands of sound"""
        # top_db=30 means anything 30dB quieter than peak is silence
        intervals = librosa.effects.split(y, top_db=30, frame_length=2048, hop_length=512)
        print(f"Found {len(intervals)} islands.")
        return intervals

    def extract_island(self, D, y, interval, fade_sec=0.03):
        """Extract a specific time interval island"""
        start_sample, end_sample = interval
        start_sec = start_sample / self.sr
        duration_sec = (end_sample - start_sample) / self.sr
        
        print(f"   Cutting {start_sec:.2f}s -> {start_sec+duration_sec:.2f}s ({duration_sec:.2f}s)")
        
        return self.extract(D, start_sec, duration_sec, fade_sec)

    def extract(self, D, start_sec, duration_sec, fade_sec=0.03):
        start_frame = librosa.time_to_frames(start_sec, sr=self.sr, hop_length=self.hop_length)
        n_frames = librosa.time_to_frames(duration_sec, sr=self.sr, hop_length=self.hop_length)
        
        if start_frame >= D.shape[1]: return np.zeros_like(D[:, 0:1])
        end_frame = min(start_frame + n_frames, D.shape[1])
        slice_spec = D[:, start_frame:end_frame]
        
        # Fade Logic
        actual_frames = slice_spec.shape[1]
        fade_frames = librosa.time_to_frames(fade_sec, sr=self.sr, hop_length=self.hop_length)
        if fade_frames * 2 > actual_frames: fade_frames = actual_frames // 2
        
        if fade_frames > 0:
            fade_in = np.linspace(0, 1, fade_frames)
            sustain_len = actual_frames - 2 * fade_frames
            sustain = np.ones(sustain_len)
            fade_out = np.linspace(1, 0, fade_frames)
            window = np.concatenate([fade_in, sustain, fade_out])
            slice_spec = slice_spec * window[np.newaxis, :]
            
        return slice_spec
        
    def create_canvas(self, duration_sec):
        n_frames = librosa.time_to_frames(duration_sec, sr=self.sr, hop_length=self.hop_length)
        return np.zeros((1 + self.n_fft // 2, n_frames), dtype=complex)
        
    def paste(self, canvas, brush, start_sec, fade_in_sec=0.0):
        start_frame = librosa.time_to_frames(start_sec, sr=self.sr, hop_length=self.hop_length)
        n_frames = brush.shape[1]
        
        if start_frame + n_frames > canvas.shape[1]:
            n_frames = canvas.shape[1] - start_frame
            brush = brush[:, :n_frames]
        
        if n_frames > 0:
            if fade_in_sec > 0:
                # Apply a linear fade-in ramp to the brush before adding
                fade_frames = librosa.time_to_frames(fade_in_sec, sr=self.sr, hop_length=self.hop_length)
                fade_frames = min(fade_frames, n_frames)
                ramp = np.ones(n_frames)
                ramp[:fade_frames] = np.linspace(0, 1, fade_frames)
                brush = brush * ramp
                
            canvas[:, start_frame:start_frame+n_frames] += brush
        return canvas

    def high_pass(self, brush, cutoff_hz):
        """Surgically remove low frequencies from a brush"""
        # Frequency bins
        freqs = librosa.fft_frequencies(sr=self.sr, n_fft=self.n_fft)
        # Find the bin index for the cutoff
        idx = np.searchsorted(freqs, cutoff_hz)
        # Kill everything below
        filtered = brush.copy()
        filtered[:idx, :] = 0
        return filtered

    def stencil(self, carrier_D, stencil_D):
        """Molds the carrier (Rachel) into the structural shape of the stencil (Google)"""
        # 1. Match durations
        min_frames = min(carrier_D.shape[1], stencil_D.shape[1])
        carrier = carrier_D[:, :min_frames]
        stencil = stencil_D[:, :min_frames]
        
        # 2. Extract Spectrogram Magnitude (The Shape)
        mag_carrier = np.abs(carrier)
        mag_stencil = np.abs(stencil)
        
        # 3. Apply the Stencil (Matrix Multiplication)
        # This forces the Carrier to adopt the energy peaks of the Stencil
        # We normalize the stencil to prevent volume explosion
        mag_stencil = mag_stencil / (np.max(mag_stencil) + 1e-6)
        
        # Create the new word
        new_mag = mag_carrier * mag_stencil
        
        # Combine with Carrier's original phase to keep identity
        new_spec = new_mag * np.exp(1j * np.angle(carrier))
        return new_spec

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='Source Audio')
    parser.add_argument('--index', type=int, default=6, help='Which island to extract (1-based)')
    args = parser.parse_args()
    
    studio = SpectralStudio(sr=44100)
    source_spec, y = studio.load(args.file)
    
    # 1. Detect Islands
    islands = studio.find_islands(y)
    
    if len(islands) == 0:
        print("No sound found.")
        exit()
        
    target_idx = args.index - 1
    if target_idx >= len(islands): target_idx = len(islands) - 1
    
    # 2. Extract The Chosen One
    print(f"Targeting Island #{target_idx + 1}")
    brush = studio.extract_island(source_spec, y, islands[target_idx], fade_sec=0.05)
    
    # 3. Create Loop
    final_spec = studio.create_canvas(duration_sec=4.0)
    final_spec = studio.paste(final_spec, brush, start_sec=0.5)
    final_spec = studio.paste(final_spec, brush, start_sec=1.5)
    final_spec = studio.paste(final_spec, brush, start_sec=2.5)
    
    studio.save(final_spec, "Spectral_Result_Clean.wav")
    print("Done.")
