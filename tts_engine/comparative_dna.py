
# comparative_dna.py
import librosa
import numpy as np

def get_metrics(path):
    y, sr = librosa.load(path, sr=44100)
    # NO TRIMMING! We need those first milliseconds.
    
    # RMS Energy
    rms = librosa.feature.rms(y=y)[0]
    # Brightness
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    
    # Locate the K burst: Find the first frame where RMS rises significantly
    k_frame = 0
    for i in range(len(rms)):
        if rms[i] > 0.005: 
            k_frame = i
            break
            
    return {
        "k_time": librosa.frames_to_time(k_frame, sr=sr),
        "k_bright": cent[k_frame],
        "k_energy": rms[k_frame],
        "max_energy": np.max(rms)
    }

def compare():
    print("📋 REVISED COMPARATIVE PHYSICS REPORT")
    print("-" * 50)
    
    teacher = get_metrics("Teacher_CAT.wav")
    student = get_metrics("PURE_CAT.wav")
    
    print(f"{'Metric':<15} | {'Teacher':<10} | {'Student':<10} | {'Delta'}")
    print("-" * 50)
    
    # Compare Energy Ratio (Crucial!)
    ratio_t = teacher['k_energy'] / (teacher['max_energy'] + 1e-6)
    ratio_s = student['k_energy'] / (student['max_energy'] + 1e-6)
    
    print(f"K-to-A Ratio    | {ratio_t:8.2f}   | {ratio_s:8.2f}   | {ratio_s-ratio_t:8.2f}")
    print(f"K Brightness    | {teacher['k_bright']:8.0f}Hz | {student['k_bright']:8.0f}Hz | {student['k_bright']-teacher['k_bright']:8.0f}")
    print("-" * 50)

if __name__ == "__main__":
    compare()
