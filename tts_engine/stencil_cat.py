
# stencil_cat.py
from spectral_studio import SpectralStudio
import librosa
import numpy as np

studio = SpectralStudio(sr=44100)

print("🎭 STENCIL ENGINE: RACHEL (Voice) x GOOGLE (Physics)")

# 1. Load the Stencil (The perfect 'Cat' structure)
y_teacher, _ = librosa.load("Teacher_CAT.wav", sr=44100)
teacher_spec = librosa.stft(y_teacher, n_fft=2048, hop_length=512)

# 2. Load the Carrier (Rachel's continuous vocal energy)
# We use 'Ah' as the source for the whole word
y_rachel, _ = librosa.load("brushes/Ah.npy") # Actually this is .npy
rachel_ah = np.load("brushes/Ah.npy")

# 3. Prepare the Carrier
# We need enough Rachel audio to cover the Teacher word
# We pad Rachel's 'Ah' so it is long enough
target_frames = teacher_spec.shape[1]
if rachel_ah.shape[1] < target_frames:
    # Loop the vowel if needed
    repeats = (target_frames // rachel_ah.shape[1]) + 1
    rachel_long = np.tile(rachel_ah, (1, repeats))
else:
    rachel_long = rachel_ah

# 4. Perform the Stencil
# This forces Rachel's frequencies to only exit the throat 
# where Google's mouth is 'open' for CAT.
stenciled_spec = studio.stencil(rachel_long, teacher_spec)

# 5. Save (Normalistion is in .save)
studio.save(stenciled_spec, "STENCIL_CAT.wav")
print("✅ Stencil Complete: STENCIL_CAT.wav")
