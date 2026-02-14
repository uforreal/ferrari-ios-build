
# talk.py
import librosa
import numpy as np
import os
import sys
from gtts import gTTS
from spectral_studio import SpectralStudio

studio = SpectralStudio(sr=44100)

PHONEME_MAP = {
    'C': 'K', 'K': 'K', 'A': 'Ah', 'T': 'T', 'B': 'B'
}

def analyze_physics(text):
    print(f"🔬 PHYSIC-SCAN: Decoding '{text}'")
    tts = gTTS(text=text, lang="en")
    tts.save("temp_teacher.mp3")
    y, _ = librosa.load("temp_teacher.mp3", sr=44100)
    y, _ = librosa.effects.trim(y, top_db=30)
    sr = 44100
    
    rms = librosa.feature.rms(y=y, hop_length=512)[0]
    times = librosa.frames_to_time(range(len(rms)), sr=sr, hop_length=512)
    
    # Identify Active Boundaries
    vowel_frame = np.argmax(rms)
    active_indices = np.where(rms > np.max(rms) * 0.1)[0]
    
    word_start = times[active_indices[0]]
    word_end = times[active_indices[-1]]
    
    word_str = text.upper().replace(" ", "")
    mapping = []
    
    # 3-Phoneme word logic (CAT, BAT)
    if len(word_str) == 3:
        # K starts at the very beginning of energy
        k_time = word_start
        # A starts shortly after
        a_time = times[vowel_frame] - 0.05
        # T is the final spike at the end
        t_time = word_end - 0.05
        
        mapping = [
            (PHONEME_MAP.get(word_str[0], word_str[0]), k_time, a_time - k_time),
            (PHONEME_MAP.get(word_str[1], word_str[1]), a_time, t_time - a_time),
            (PHONEME_MAP.get(word_str[2], word_str[2]), t_time, 0.05)
        ]
        
    return mapping, (len(y)/sr)

def speak(text):
    mapping, total_dur = analyze_physics(text)
    canvas = studio.create_canvas(total_dur + 0.2)
    
    print(f"💉 SURGICAL Stitching...")
    
    for i, (p_name, start, duration) in enumerate(mapping):
        try:
            brush_raw = np.load(f"brushes/{p_name}.npy")
            
            # PHONEME PHYSICS
            if p_name in ["K", "T", "B", "P"]:
                # SURGERY: Take only the first 30ms of the consonant
                # This kills the 'Tee' and 'Kay' vowel tails
                brush = studio.extract(brush_raw, 0.012, 0.035, fade_sec=0.005) * 15.0
            else:
                # Vowels take the full required duration
                brush = studio.extract(brush_raw, 0.05, duration, fade_sec=0.01)

            # TIGHT OVERLAP (15ms)
            overlap = 0.015 if i > 0 else 0.0
            studio.paste(canvas, brush, start - overlap, fade_in_sec=0.01)
            print(f"   [+] {p_name} stitched at {start:.3f}s")
            
        except Exception:
            pass

    out_file = f"SURGICAL_{text.upper()}.wav"
    studio.save(canvas, out_file)
    print(f"✨ SURGERY COMPLETE: {out_file}")

if __name__ == "__main__":
    speak(sys.argv[1] if len(sys.argv) > 1 else "CAT")
