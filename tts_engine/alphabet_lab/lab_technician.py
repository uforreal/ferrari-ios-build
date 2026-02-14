
# alphabet_lab/lab_technician.py
import sys
import os
import argparse
from scipy.io import wavfile
import numpy as np

# Ensure tts package is in path (assuming we run from tts_engine root)
sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())

from tts.synthesizer import Synthesizer

# === THE RECIPE BOOK (Editable during lab sessions) ===
# We will tweak these values constantly.
ALPHABET_RECIPES = {
    "A": [("e", 200), ("i", 150)],            
    "B": [("b", 60), ("i", 250)],          
    "C": [("s", 120), ("i", 250)],            
    "D": [("d", 60), ("i", 250)],          
    "E": [("i", 350)],                         
    "F": [("ɛ", 150), ("f", 180)],             
    "G": [("d", 40), ("ʒ", 60), ("i", 250)], 
    "H": [("e", 150), ("t", 40), ("ʃ", 150)],   
    "I": [("ɑ", 200), ("i", 150)],            
    "J": [("d", 40), ("ʒ", 60), ("e", 150), ("i", 100)], 
    "K": [("k", 80), ("e", 150), ("i", 100)], 
    "L": [("ɛ", 150), ("l", 200)],             
    "M": [("ɛ", 150), ("m", 200)],             
    "N": [("ɛ", 150), ("n", 200)],             
    "O": [("o", 250), ("u", 150)],            
    "P": [("p", 60), ("i", 250)],          
    "Q": [("k", 60), ("j", 40), ("u", 250)], 
    "R": [("ɑ", 250), ("r", 150)],            
    "S": [("ɛ", 150), ("s", 200)],             
    "T": [("t", 60), ("i", 250)],          
    "U": [("j", 60), ("u", 300)],          
    "V": [("v", 80), ("i", 250)],          
    "W": [("d", 40), ("ʌ", 80), ("b", 40), ("ə", 40), ("l", 80), ("j", 40), ("u", 200)], 
    "X": [("ɛ", 150), ("k", 40), ("s", 200)], 
    "Y": [("w", 60), ("ɑ", 180), ("i", 150)], 
    "Z": [("z", 80), ("i", 250)],          
}

def generate_letter(letter):
    letter = letter.upper()
    if letter not in ALPHABET_RECIPES:
        print(f"Error: Letter '{letter}' not found in recipes.")
        return

    print(f"[LAB] Lab Technician: Synthesizing '{letter}'...")
    sequence = ALPHABET_RECIPES[letter]
    # Small pause at start to avoid transient clicking
    full_sequence = ["_pause"] + sequence + ["_pause"]
    
    print(f"   Recipe: {sequence}")
    
    synth = Synthesizer()
    audio = synth.synthesize_sequence(full_sequence)
    
    # Int16 conversion
    audio_int16 = (audio * 32767).astype(np.int16)
    
    filename = f"{letter}_test.wav"
    wavfile.write(filename, synth.sample_rate, audio_int16)
    print(f"[OK] Generated: alphabet_lab/{filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Synthesize a single alphabet letter.')
    parser.add_argument('letter', type=str, help='The letter to synthesize (A-Z)')
    args = parser.parse_args()
    
    generate_letter(args.letter)
