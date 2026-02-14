
# oracle_judge.py
import whisper
import numpy as np
import soundfile as sf
import librosa
import sys

# Cache the model to speed up loops
_MODEL = None

def get_confidence(path, target_word):
    global _MODEL
    if _MODEL is None:
        print("🧠 Waking up the Oracle (Whisper)...")
        _MODEL = whisper.load_model("tiny")
    
    try:
        # 1. Load & Pre-process
        y, sr = sf.read(path)
        if sr != 16000:
            y = librosa.resample(y, orig_sr=sr, target_sr=16000)
        y = y.astype(np.float32)
        
        # 2. Transcribe with details
        # We look for the 'avg_logprob' - higher (closer to 0) is better
        result = _MODEL.transcribe(y, fp16=False) 
        
        text = result['text'].strip().upper().replace(".", "").replace(",", "")
        
        # 3. Score calculation
        # If it heard the right word, we look at the probability
        logprob = -999
        match = (target_word.upper() in text)
        
        if len(result['segments']) > 0:
            logprob = result['segments'][0]['avg_logprob']
        
        # Physics Feedback: Spectral Centroid check
        # Is the high-freq energy balanced?
        cent = librosa.feature.spectral_centroid(y=y, sr=16000)[0]
        avg_cent = np.mean(cent)
        
        return {
            "match": match,
            "heard": text,
            "score": logprob,
            "brightness": avg_cent
        }
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    res = get_confidence(sys.argv[1], sys.argv[2])
    print(res)
