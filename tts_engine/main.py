
from tts.engine import TTSEngine
import numpy as np
import time
import sounddevice as sd
from scipy.io import wavfile

# Create engine
tts = TTSEngine()
tts.set_voice("warm")
tts.set_speed(0.6) 

print("--- FINAL ENGINE TEST ---")
print("Synthesizing full conversation...")

# Define sentences
sentences = [
    "hello",
    "i am a robot",
    "how can i help you",
    "systems operational",
    "frequency stable"
]

all_audio = []
silence = np.zeros(int(0.5 * tts.sample_rate))

for text in sentences:
    print(f"Speaking: {text}")
    
    # Generate
    audio = tts.synthesize(text)
    all_audio.append(audio)
    all_audio.append(silence)
    
    # Play
    sd.play(audio, tts.sample_rate)
    sd.wait()
    time.sleep(0.2)

# Save EVERYTHING to file
final_output = np.concatenate(all_audio)
# Convert to 16-bit PCM for compatibility
final_output_int16 = (final_output * 32767).astype(np.int16)
wavfile.write("full_demo.wav", tts.sample_rate, final_output_int16)
print(f"\nSaved full session to: full_demo.wav")
