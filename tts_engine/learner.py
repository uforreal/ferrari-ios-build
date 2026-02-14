
# learner.py
from spectral_studio import SpectralStudio
import numpy as np
import librosa
import judge_whisper

# Initialize
studio = SpectralStudio(sr=44100)

def load_audio(path):
    print(f"📚 Loading Teacher: {path}")
    y, sr = librosa.load(path, sr=44100)
    # Trim silence
    y, _ = librosa.effects.trim(y, top_db=20)
    return y

def analyze_teacher(y):
    # Detect Onsets (Events)
    onset_frames = librosa.onset.onset_detect(y=y, sr=44100, units='frames')
    onset_times = librosa.frames_to_time(onset_frames, sr=44100)
    
    print(f"   Teacher Events detected at: {onset_times}")
    
    # We expect roughly:
    # 0.0s -> K
    # X.Xs -> A
    # Y.Ys -> T
    
    if len(onset_times) < 2:
        print("   ⚠️ Not enough events detected in Teacher. Using fallback timing.")
        return [0.0, 0.15, 0.35] # Fallback
        
    return onset_times

def create_student(timings):
    print("🎓 Creating Student based on Teacher timings...")
    
    # Calculate durations based on gaps
    # K duration = Time(A) - Time(K)
    # A duration = Time(T) - Time(A)
    
    # Note: onset_detect might miss the first one if it's at 0.0
    # Let's force a 0.0 start
    provisional_times = [0.0]
    for t in timings:
        if t > 0.05: # Filter out immediate start duplicates
            provisional_times.append(t)
            
    # We need 3 events: K start, A start, T start
    if len(provisional_times) < 3:
        # Pad if missing
        while len(provisional_times) < 3:
            provisional_times.append(provisional_times[-1] + 0.2)
    
    k_start = provisional_times[0]
    a_start = provisional_times[1]
    t_start = provisional_times[2]
    
    print(f"   Aligning: K@{k_start:.2f}s, A@{a_start:.2f}s, T@{t_start:.2f}s")
    
    # === Load Rachel's Brushes ===
    # K (Smart Burst)
    k_full = np.load("brushes/K.npy")
    # Quick dirty smart extract again (first 5 frames)
    k_brush = k_full[:, 0:5] * 8.0
    
    # Ah (Vowel)
    ah_full = np.load("brushes/Ah.npy")
    # Take a nice chunk
    ah_brush = studio.extract(ah_full, 0.02, 0.25, fade_sec=0.02)
    
    # T (Pop)
    t_full = np.load("brushes/T.npy")
    t_brush = studio.extract(t_full, 0.0, 0.05, fade_sec=0.005) * 3.0
    
    # === Stitch ===
    # Canvas duration = T_start + 0.2s
    canvas = studio.create_canvas(t_start + 0.3)
    
    # Paste K
    canvas = studio.paste(canvas, k_brush, k_start)
    
    # Paste A
    canvas = studio.paste(canvas, ah_brush, a_start)
    
    # Paste T
    canvas = studio.paste(canvas, t_brush, t_start)
    
    out_path = "Student_CAT.wav"
    studio.save(canvas, out_path)
    return out_path

if __name__ == "__main__":
    # 1. Load Teacher
    teacher_y = load_audio("Teacher_CAT.wav")
    
    # 2. Analyze
    timings = analyze_teacher(teacher_y)
    
    # 3. Synthesize
    student_file = create_student(timings)
    
    # 4. Judge
    print("\n⚖️ JUDGEMENT PENDING...")
    judge_whisper.judge(student_file)
