
# Store all phoneme data as dictionaries.
# "Ocean of Characteristics" Model
# Standardized Schema:
#   f: [F1, F2, F3, F4, F5] - Formant frequencies (Hz)
#   b: [B1, B2, B3, B4, B5] - Bandwidths (Hz)
#   av: Amp of Voicing (dB) - The buzz
#   ah: Amp of Aspiration (dB) - The breathiness
#   af: Amp of Frication (dB) - The hiss
#   dur: Duration (ms)
#   type: Category (for transition logic)

PHONEMES = {
    # === VOWELS ===
    # Vowels are driven by AV (Voicing). AH/AF are usually 0.
    "i":  {
        "f": [270, 2290, 3010, 3500, 4500], 
        "b": [60, 90, 150, 200, 250],   
        "av": 60, "ah": 0, "af": 0,
        "dur": 100, "type": "vowel"
    },
    "ɪ":  {
        "f": [390, 1990, 2550, 3500, 4500], 
        "b": [70, 100, 140, 200, 250],  
        "av": 60, "ah": 0, "af": 0,
        "dur": 90,  "type": "vowel"
    },
    "e":  {
        "f": [530, 1840, 2480, 3500, 4500], 
        "b": [70, 100, 140, 200, 250],  
        "av": 60, "ah": 0, "af": 0,
        "dur": 110, "type": "vowel"
    },
    "ɛ":  {
        "f": [660, 1720, 2410, 3500, 4500], 
        "b": [80, 100, 150, 200, 250],  
        "av": 60, "ah": 0, "af": 0,
        "dur": 100, "type": "vowel"
    },
    "æ":  {
        "f": [730, 1090, 2440, 3500, 4500], 
        "b": [90, 110, 170, 200, 250],  
        "av": 60, "ah": 0, "af": 0,
        "dur": 130, "type": "vowel"
    },
    "ɑ":  {
        "f": [730, 1090, 2440, 3500, 4500], 
        "b": [90, 110, 170, 200, 250],  
        "av": 60, "ah": 0, "af": 0,
        "dur": 140, "type": "vowel"
    },
    "ɔ":  {
        "f": [570, 840, 2410, 3500, 4500],  
        "b": [80, 100, 150, 200, 250],  
        "av": 60, "ah": 0, "af": 0,
        "dur": 120, "type": "vowel"
    },
    "o":  {
        "f": [490, 1350, 2380, 3500, 4500], 
        "b": [70, 90, 140, 200, 250],   
        "av": 60, "ah": 0, "af": 0,
        "dur": 110, "type": "vowel"
    },
    "ʊ":  {
        "f": [440, 1020, 2240, 3500, 4500], 
        "b": [70, 100, 140, 200, 250],  
        "av": 60, "ah": 0, "af": 0,
        "dur": 90,  "type": "vowel"
    },
    "u":  {
        "f": [300, 870, 2240, 3500, 4500],  
        "b": [60, 90, 140, 200, 250],   
        "av": 60, "ah": 0, "af": 0,
        "dur": 100, "type": "vowel"
    },
    "ʌ":  {
        "f": [640, 1190, 2390, 3500, 4500], 
        "b": [80, 100, 150, 200, 250],  
        "av": 60, "ah": 0, "af": 0,
        "dur": 90,  "type": "vowel"
    },
    "ə":  {
        "f": [500, 1500, 2490, 3500, 4500], 
        "b": [70, 100, 150, 200, 250],  
        "av": 60, "ah": 0, "af": 0,
        "dur": 60,  "type": "vowel"
    },
    "ɝ":  {
        "f": [500, 1400, 1600, 3500, 4500], 
        "b": [60, 100, 150, 200, 250],  
        "av": 60, "ah": 0, "af": 0,
        "dur": 100, "type": "vowel"
    },
    
    # === FRICATIVES ===
    # Driven by AF (Frication). AV is 0 for unvoiced.
    # We use F formants to color the noise.
    # For /s/, we tune formants to create the high freq peak.
    "s":  {
        # F1 usually cancelled/low, F2/F3/F4 used for spectral shape
        "f": [0, 4000, 5000, 6000, 7000],  
        "b": [500, 500, 500, 1000, 1000], 
        "av": 0, "ah": 0, "af": 55, # Strong hiss
        "dur": 130, "type": "fricative"
    },
    "z":  {
        "f": [0, 4000, 5000, 6000, 7000],  
        "b": [500, 500, 500, 1000, 1000], 
        "av": 30, "ah": 0, "af": 40, # Buzz + Hiss
        "dur": 120, "type": "fricative"
    },
    "f":  {
        "f": [500, 1500, 2500, 3500, 4500], # Neutral shape, mostly noise
        "b": [100, 100, 200, 300, 400],
        "av": 0, "ah": 0, "af": 50,
        "dur": 110, "type": "fricative"
    },
    "v":  {
        "f": [500, 1500, 2500, 3500, 4500], 
        "b": [100, 100, 200, 300, 400],
        "av": 40, "ah": 0, "af": 30,
        "dur": 100, "type": "fricative"
    },
    "ʃ":  { # "Sh"
        "f": [0, 2500, 3500, 4500, 5500], # Lower peak than 's'
        "b": [500, 300, 400, 500, 600],
        "av": 0, "ah": 0, "af": 55,
        "dur": 130, "type": "fricative"
    },
    "ʒ":  { # "Zh"
        "f": [0, 2500, 3500, 4500, 5500],
        "b": [500, 300, 400, 500, 600],
        "av": 40, "ah": 0, "af": 40,
        "dur": 120, "type": "fricative"
    },
    "h":  {
        "f": [500, 1500, 2500, 3500, 4500], 
        "b": [100, 100, 150, 200, 250],
        "av": 0, "ah": 50, "af": 0, # AH is aspiration (breath)
        "dur": 80,  "type": "fricative"
    },
    
    # === NASALS ===
    "m":  {
        "f": [300, 1000, 2500, 3500, 4500], 
        "b": [50, 100, 150, 200, 250],  
        "av": 60, "ah": 0, "af": 0,
        "dur": 100, "type": "nasal"
    },
    "n":  {
        "f": [300, 1400, 2500, 3500, 4500], 
        "b": [50, 100, 150, 200, 250],  
        "av": 60, "ah": 0, "af": 0,
        "dur": 90,  "type": "nasal"
    },
    "ŋ":  {
        "f": [300, 1300, 2500, 3500, 4500], 
        "b": [50, 100, 150, 200, 250],  
        "av": 60, "ah": 0, "af": 0,
        "dur": 90,  "type": "nasal"
    },
    
    # === LIQUIDS & GLIDES ===
    "l":  {
        "f": [350, 1100, 2800, 3500, 4500], 
        "b": [60, 100, 150, 200, 250],  
        "av": 60, "ah": 0, "af": 0,
        "dur": 90,  "type": "liquid"
    },
    "r":  {
        "f": [350, 1300, 1600, 3500, 4500], 
        "b": [60, 100, 150, 200, 250],  
        "av": 60, "ah": 0, "af": 0,
        "dur": 90,  "type": "liquid"
    },
    "w":  {
        "f": [300, 610, 2200, 3500, 4500],  
        "b": [50, 80, 120, 200, 250],   
        "av": 60, "ah": 0, "af": 0,
        "dur": 70,  "type": "glide"
    },
    "j":  {
        "f": [270, 2200, 3000, 3500, 4500], 
        "b": [50, 80, 120, 200, 250],   
        "av": 60, "ah": 0, "af": 0,
        "dur": 70,  "type": "glide"
    },
    
    # === STOPS ===
    # Stops are complex: require Silence -> Burst -> Transition
    # This naive bank just defines the "Stop" state (silence/voicing bar)
    # The burst is often handled by the engine's transitions, but we can define the 'target'
    # as the closure.
    "p":  { "f": [500, 1500, 2500, 3500, 4500], "b": [100, 100, 150, 200, 250], "av": 0, "ah": 0, "af": 0, "dur": 80, "type": "stop" },
    "b":  { "f": [500, 1500, 2500, 3500, 4500], "b": [100, 100, 150, 200, 250], "av": 60, "ah": 0, "af": 0, "dur": 80, "type": "stop" }, # Voice bar
    "t":  { "f": [500, 1500, 2500, 3500, 4500], "b": [100, 100, 150, 200, 250], "av": 0, "ah": 0, "af": 0, "dur": 80, "type": "stop" },
    "d":  { "f": [500, 1500, 2500, 3500, 4500], "b": [100, 100, 150, 200, 250], "av": 60, "ah": 0, "af": 0, "dur": 80, "type": "stop" },
    "k":  { "f": [500, 1500, 2500, 3500, 4500], "b": [100, 100, 150, 200, 250], "av": 0, "ah": 0, "af": 0, "dur": 80, "type": "stop" },
    "g":  { "f": [500, 1500, 2500, 3500, 4500], "b": [100, 100, 150, 200, 250], "av": 60, "ah": 0, "af": 0, "dur": 80, "type": "stop" },
}
