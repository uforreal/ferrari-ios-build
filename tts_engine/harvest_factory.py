
# harvest_factory.py
import librosa
import numpy as np
import os
import argparse
from spectral_studio import SpectralStudio

def run_harvest(audio_path, char_string, threshold_db=25):
    chars = list(char_string)
    print(f"Factory Online. Processing: {audio_path} (Threshold: {threshold_db}dB)")
    
    studio = SpectralStudio(sr=44100)
    
    print("   Loading audio...")
    full_spec, full_y = studio.load(audio_path)
    
    # 2. Detect Islands
    # Using stricter threshold to ignore breaths
    islands = studio.find_islands(full_y) # spectral_studio uses 30 by default, let's override
    # Actually spectral_studio.find_islands hardcodes 30. We should override it here manually.
    intervals = librosa.effects.split(full_y, top_db=threshold_db, frame_length=2048, hop_length=512)
    print(f"   Found {len(intervals)} islands.")
    
    count = len(intervals)
    expected = len(chars) * 3
    
    if count == expected:
        print("Perfect Match: 3 takes per letter.")
        mode = "triple"
    elif count == len(chars):
        print("Warning: Only 1 take per letter.")
        mode = "single"
    else:
        print(f"Mismatch! Expected {expected} or {len(chars)}, found {count}.")
        mode = "dump"
        
    os.makedirs("brushes", exist_ok=True)
    
    if mode == "dump":
        os.makedirs("brushes/dump", exist_ok=True)
        for i, island in enumerate(intervals):
            brush = studio.extract_island(full_spec, full_y, island, fade_sec=0.03)
            np.save(f"brushes/dump/{os.path.basename(audio_path)}_{i+1:02d}.npy", brush)
    else:
        for i, letter in enumerate(chars):
            if mode == "triple":
                idx = i * 3 + 1
            else:
                idx = i
            
            brush = studio.extract_island(full_spec, full_y, intervals[idx], fade_sec=0.03)
            np.save(f"brushes/{letter}.npy", brush)

    print("Harvest Complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    parser.add_argument('--chars', type=str, required=True)
    parser.add_argument('--db', type=float, default=25, help="Silence threshold (lower = stricter)")
    args = parser.parse_args()
    
    run_harvest(args.file, args.chars, args.db)
