
# oracle_tuner.py
from spectral_studio import SpectralStudio
import oracle_judge
import numpy as np
import os

studio = SpectralStudio(sr=44100)

def load_brush(name): return np.load(f"brushes/{name}.npy")

def run_trial(id, params):
    # params: k_len, a_len, t_len, ka_overlap, at_overlap, a_boost
    k_len, a_len, t_len, ka_overlap, at_overlap, a_boost = params
    
    k_raw = load_brush("K")
    ah_raw = load_brush("Ah")
    t_raw = load_brush("T")
    
    # 1. Surgical Extraction
    k_brush = studio.extract(k_raw, 0.012, k_len) * 15.0
    ah_brush = studio.extract(ah_raw, 0.05, a_len) * a_boost
    t_brush = studio.extract(t_raw, 0.0, t_len) * 8.0
    
    # 2. Additive Layout (The Math of the Word Body)
    canvas = studio.create_canvas(1.0)
    
    cursor = 0.1
    studio.paste(canvas, k_brush, cursor)
    
    # A overlaps the K tail
    cursor += (k_len - ka_overlap)
    studio.paste(canvas, ah_brush, cursor, fade_in_sec=min(0.04, ka_overlap))
    
    # T overlaps the A tail
    cursor += (a_len - at_overlap)
    studio.paste(canvas, t_brush, cursor)
    
    path = f"trials/trial_{id}.wav"
    studio.save(canvas, path)
    return path

# --- Optimization Loop ---
if not os.path.exists("trials"): os.makedirs("trials")

best_score = -999
best_params = None

print("🕵️‍♂️ SEARCHING FOR THE INTELLIGIBILITY PEAK...")

# Initial Guess (Phonetic Archetype)
# k_len, a_len, t_len, ka_overlap, at_overlap, a_boost
p = [0.08, 0.22, 0.06, 0.03, 0.02, 1.0]

for i in range(50):
    # Randomly mutate parameters based on 'physics noise'
    test_p = [
        max(0.04, p[0] + np.random.uniform(-0.02, 0.02)), # k_len
        max(0.10, p[1] + np.random.uniform(-0.05, 0.05)), # a_len
        max(0.03, p[2] + np.random.uniform(-0.02, 0.02)), # t_len
        max(0.01, p[3] + np.random.uniform(-0.01, 0.01)), # overlap
        max(0.01, p[4] + np.random.uniform(-0.01, 0.01)), # overlap
        max(0.5, p[5] + np.random.uniform(-0.2, 0.2))     # a_boost
    ]
    
    wav_path = run_trial(i, test_p)
    res = oracle_judge.get_confidence(wav_path, "CAT")
    
    print(f" Trial {i:2d} | Heard: '{res['heard']:<10}' | Conf: {res['score']:5.2f} | Br: {res['brightness']:4.0f}Hz")
    
    if res['match'] and res['score'] > best_score:
        best_score = res['score']
        best_params = test_p
        print(f"   📊 [NEW BEST] Found at iteration {i}")

print("\n🏆 OPTIMIZATION COMPLETE")
# Save final version
final_wav = run_trial("WINNER", best_params)
print(f"Final Word formed: {final_wav}")
