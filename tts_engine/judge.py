
# judge.py
import speech_recognition as sr
import sys
import os

def judge_audio(path):
    r = sr.Recognizer()
    
    # Load audio
    with sr.AudioFile(path) as source:
        audio = r.record(source)
    
    # Judge
    try:
        # Pocketsphinx is offline but requires separate install.
        # Google is online, free, high quality.
        print(f"Human listening to {path}...")
        text = r.recognize_google(audio)
        print(f"JUDGE HEARD: '{text}'")
        return text
    except sr.UnknownValueError:
        print("JUDGE HEARD: [Unintelligible]")
        return None
    except sr.RequestError as e:
        print(f"JUDGE ERROR: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python judge.py file.wav")
        sys.exit(1)
        
    judge_audio(sys.argv[1])
