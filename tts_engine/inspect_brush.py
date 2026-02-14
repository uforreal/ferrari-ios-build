
# inspect_brush.py
import librosa
import numpy as np

def inspect(name):
    print(f"🔍 Inspecting Brush Physics: {name}.npy")
    brush = np.load(f"brushes/{name}.npy")
    
    # Convert to audio to analyze
    y = librosa.istft(brush, hop_length=512, n_fft=2048)
    
    # Find the Peak Brightness (The Burst)
    # K is high frequency (4000Hz+). Let's find where the energy moves there.
    cent = librosa.feature.spectral_centroid(y=y, sr=44100)[0]
    rms = librosa.feature.rms(y=y)[0]
    
    # Find the first frame where energy > 10% of max AND brightness > 3000Hz
    burst_frame = 0
    max_rms = np.max(rms)
    for i in range(len(rms)):
        if rms[i] > max_rms * 0.1 and cent[i] > 3000:
            burst_frame = i
            break
            
    burst_time = librosa.frames_to_time(burst_frame, sr=44100, hop_length=512)
    print(f"   [!] Physical Burst detected at {burst_time:.3f}s (Frame {burst_frame})")
    print(f"   Brightness at Burst: {cent[burst_frame]:.0f}Hz")
    print(f"   Energy at Burst: {rms[burst_frame]:.3f}")

if __name__ == "__main__":
    inspect("K")
