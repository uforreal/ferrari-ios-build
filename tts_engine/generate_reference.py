
# generate_reference.py
from gtts import gTTS
import os

print("Generating Teacher Reference...")
tts = gTTS(text="Cat", lang="en", tld="com") # US English
tts.save("Teacher_CAT.mp3")
print("Saved Teacher_CAT.mp3")

# Optional: Convert to WAV for easier processing if ffmpeg exists
try:
    import soundfile as sf
    import librosa
    y, sr = librosa.load("Teacher_CAT.mp3", sr=44100)
    sf.write("Teacher_CAT.wav", y, sr)
    print("Converted to Teacher_CAT.wav")
except Exception as e:
    print(f"Conversion warning: {e}")
