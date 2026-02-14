
import librosa
import numpy as np

def analyze_cat_dna(path):
    print(f"🧬 Extracting Genetic Blueprint: {path}")
    y, sr = librosa.load(path, sr=None)
    y, _ = librosa.effects.trim(y)
    
    # Analyze frame-by-frame (23ms windows)
    hop_length = 512
    n_fft = 2048
    
    # Get Energy Envelope
    rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
    
    # Get Spectral Centroid (Brightness)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length)[0]
    
    # Get Spectral Bandwidth
    bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length)[0]

    frames = range(len(rms))
    times = librosa.frames_to_time(frames, sr=sr, hop_length=hop_length)
    
    print("\nTIMELINE ANALYSIS:")
    print("-" * 60)
    print(f"{'Time':<10} | {'Volume':<10} | {'Brightness':<10} | {'Formants/Physics'}")
    print("-" * 60)
    
    data = []
    
    for i in frames:
        t = times[i]
        vol = rms[i]
        bright = centroid[i]
        
        # Only analyze frames with sound
        if vol > 0.005: 
            # Segment audio for this frame
            start_sample = i * hop_length
            end_sample = min(len(y), (i + 1) * hop_length)
            frame_audio = y[start_sample:end_sample]
            
            # Get Physics
            phys_type = "Burst" if bright > 4000 else "Vowel" if bright < 2500 else "Transition"
            
            # Log
            print(f"{t:4.2f}s      | {vol:4.3f}      | {bright:5.0f}Hz     | {phys_type}")
            
            data.append({
                "time": t,
                "vol": vol,
                "bright": bright,
                "type": phys_type
            })

    print("-" * 60)
    return data

if __name__ == "__main__":
    analyze_cat_dna("Teacher_CAT.wav")
