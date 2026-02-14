
# judge_whisper.py
import whisper
import numpy as np
import soundfile as sf
import librosa
import sys

def judge(path):
    print(f"👂 Listening to {path}...")
    try:
        # Load Model (Lazy load or global?)
        # For simplicity, load every time (slow but safe)
        model = whisper.load_model("tiny")
        
        # Load Audio via SoundFile (Bypass FFmpeg)
        y, sr = sf.read(path)
        
        # Resample to 16k
        if sr != 16000:
            y = librosa.resample(y, orig_sr=sr, target_sr=16000)
            
        # Cast to float32
        y = y.astype(np.float32)
        
        # Transcribe
        result = model.transcribe(y, fp16=False) # fp16=False for CPU
        text = result['text'].strip()
        print(f"🧠 HEARD: '{text}'")
        return text
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python judge_whisper.py file.wav")
    else:
        judge(sys.argv[1])
