
# sequencer.py
import numpy as np
import argparse
import os
from spectral_studio import SpectralStudio
import librosa

class Sequencer:
    def __init__(self):
        self.studio = SpectralStudio(sr=44100)
        self.brushes = {}
        self.load_bank()
        
    def load_bank(self):
        print("Loading Brush Bank...")
        brush_dir = "brushes"
        if not os.path.exists(brush_dir):
            print("Create 'brushes' directory first!")
            return
            
        for f in os.listdir(brush_dir):
            if f.endswith(".npy"):
                char = f.split(".")[0].upper()
                try:
                    self.brushes[char] = np.load(os.path.join(brush_dir, f))
                    print(f"   Loaded {char}")
                except:
                    print(f"   Failed to load {f}")

    def sequence(self, text):
        print(f"Sequencing: '{text}'")
        # Estimate duration: 0.4s per char + 0.5s padding
        duration = len(text) * 0.4 + 1.0
        canvas = self.studio.create_canvas(duration)
        
        cursor_sec = 0.1
        
        for char in text.upper():
            if char in self.brushes:
                brush = self.brushes[char]
                
                # === AUTO-CROP ===
                # Most brushes are 1.0s+ (merged). We only want the onset (0.3s).
                # Convert 0.3s to frames
                max_frames = librosa.time_to_frames(0.35, sr=44100, hop_length=512)
                if brush.shape[1] > max_frames:
                    brush = brush[:, :max_frames]
                
                # Apply localized fade out to avoid clicks on the chop
                # (Simple manual fade on the last 5 frames)
                if brush.shape[1] > 5:
                    for f in range(5):
                        vol = 1.0 - (f / 5.0)
                        brush[:, -(f+1)] *= vol

                # Paste
                # Overlap logic: A standard letter is ~0.15s speech + 0.1s silence?
                # Let's paste every 0.25s for a fast tempo.
                
                self.studio.paste(canvas, brush, cursor_sec)
                cursor_sec += 0.25 
            elif char == " ":
                cursor_sec += 0.2
            else:
                print(f"   Missing Brush: {char}")
        
        return canvas

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('text', type=str)
    args = parser.parse_args()
    
    seq = Sequencer()
    canvas = seq.sequence(args.text)
    
    out_name = "Sequence_Output.wav"
    seq.studio.save(canvas, out_name)
    print(f"Done: {out_name}")
