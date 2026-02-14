
# probe.py
import librosa
import numpy as np
import soundfile as sf

def probe(path, name):
    print(f"🔬 Probing {path} (First 150ms)...")
    y, sr = librosa.load(path, sr=44100)
    # Extract only the first 150ms
    n_samples = int(0.15 * sr)
    segment = y[:n_samples]
    
    # Analyze the 'Real' peak energy and brightness of THIS segment
    rms = np.max(librosa.feature.rms(y=segment)[0])
    cent = np.mean(librosa.feature.spectral_centroid(y=segment, sr=sr)[0])
    
    print(f"   Peak Energy: {rms:4.4f}")
    print(f"   Avg Brightness: {cent:4.0f}Hz")
    
    # Save for you to listen to
    out_name = f"PROBE_{name}.wav"
    sf.write(out_name, segment, sr)
    print(f"   [!] Saved {out_name} for listening.")

if __name__ == "__main__":
    probe("Teacher_CAT.wav", "TEACHER")
    probe("PURE_CAT.wav", "STUDENT")
