
# test_whisper.py
import whisper
import numpy as np

def test():
    print("Loading Whisper Model (Tiny)...")
    try:
        model = whisper.load_model("tiny")
        print("Model Loaded.")
        
        # Test recognition
        # If ffmpeg is missing, this usually fails on load_audio
        print("Transcribing Surgery_CAT_v8_BLEND.wav...")
        result = model.transcribe("Surgery_CAT_v8_BLEND.wav")
        print(f"WHISPER HEARD: '{result['text']}'")
        
    except Exception as e:
        print(f"WHISPER ERROR: {e}")
        print("Attempting Bypass (Numpy Load)...")
        # Bypass ffmpeg by using soundfile/librosa to load
        try:
            import soundfile as sf
            y, sr = sf.read("Surgery_CAT_v8_BLEND.wav")
            # Whisper expects 16kHz
            import librosa
            y_16k = librosa.resample(y, orig_sr=sr, target_sr=16000)
            
            result = model.transcribe(y_16k)
            print(f"WHISPER BYPASS HEARD: '{result['text']}'")
        except Exception as e2:
            print(f"BYPASS ERROR: {e2}")

if __name__ == "__main__":
    test()
