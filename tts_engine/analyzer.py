
# analyzer.py
import librosa
import numpy as np

def analyze_fingerprint(path):
    print(f"🔬 Analyzing Anatomy of: {path}")
    y, sr = librosa.load(path, sr=44100)
    
    # 1. Onset Envelope (Rhythm)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    times = librosa.times_like(onset_env, sr=sr)
    
    # 2. Spectral Centroid (Brightness/Timbre)
    # High centroid = "S", "T", "K"
    # Low centroid = "O", "U", "M"
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    
    # 3. RMS Energy (Volume)
    S, phase = librosa.magphase(librosa.stft(y))
    rms = librosa.feature.rms(S=S)[0]
    
    # Scan for "Events" (Peaks in processing)
    # We define an event as a region of significant energy
    onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, units='time')
    
    print(f"   Detected {len(onsets)} Structural Events at: {onsets}")
    
    for i, t in enumerate(onsets):
        # Frame index
        frame = librosa.time_to_frames(t, sr=sr)
        
        # Get metrics at this moment
        brightness = cent[frame]
        loudness = rms[frame]
        
        # Classify Sound Type based on Physics
        sound_type = "Unknown"
        if brightness > 3000:
            sound_type = "Fricative / Plosive Burst (S, T, K)"
        elif brightness < 1500 and loudness > 0.01:
            sound_type = "Vowel / Voiced (A, O, M)"
        else:
             sound_type = "Transition / Breath"
             
        print(f"   Event #{i+1} @ {t:.2f}s: Type=[{sound_type}] | FreqCenter={brightness:.0f}Hz | Energy={loudness:.3f}")

if __name__ == "__main__":
    analyze_fingerprint("Teacher_CAT.wav")
