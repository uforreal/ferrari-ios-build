
# lpc_bridge.py
import librosa
import numpy as np
import scipy.signal as signal
import soundfile as sf

def extract_lpc_filter(y, order=16):
    """Extracts the 'Mouth Shape' (LPC coefficients) from a signal"""
    # lpc returns the filter coefficients
    a = librosa.lpc(y, order=order)
    return a

def extract_source(y, a):
    """Extracts the 'Vocals' (Residual) by passing audio through an inverse filter"""
    # This removes the 'mouth' and leaves only the 'identity/breath'
    residual = signal.lfilter(a, 1, y)
    return residual

def synthesize(source, filter_coeffs):
    """Resynthesizes by passing a new source through the mouth filter"""
    return signal.lfilter([1], filter_coeffs, source)

def run_bridge(target_word="CAT"):
    print(f"🌉 THE LPC BRIDGE: Preserving Rachel's Soul, Using the Word's Physics")
    
    # 1. LOAD THE ARTICULATION (The Teacher - The 'What')
    y_t, sr = librosa.load(f"Teacher_{target_word}.wav", sr=22050)
    y_t, _ = librosa.effects.trim(y_t)
    
    # 2. LOAD THE IDENTITY (Rachel - The 'Who')
    # We take Rachel's 'Ah' to get her raw vocal cord signature
    # (Since our .npy are spectrograms, I will generate a raw wave from her brush first)
    ah_spec = np.load("brushes/Ah.npy")
    y_r = librosa.istft(ah_spec, hop_length=512, n_fft=2048)
    if len(y_r) < len(y_t):
        y_r = np.tile(y_r, int(np.ceil(len(y_t)/len(y_r))))
    y_r = y_r[:len(y_t)]
    
    # 3. THE FORENSIC CLEANING
    # We analyze the audio in 30ms windows (The speed of a mouth moving)
    win_len = int(0.03 * sr)
    hop_len = int(0.01 * sr)
    
    output = np.zeros(len(y_t))
    
    print("   [!] De-composing and Re-weaving the vocal tract...")
    
    for i in range(0, len(y_t) - win_len, hop_len):
        # Slice the windows
        chunk_t = y_t[i:i+win_len]
        chunk_r = y_r[i:i+win_len]
        
        # Extract the 'Mouth' from the Teacher (Order 16 = standard human tract)
        a_teacher = extract_lpc_filter(chunk_t, order=22)
        
        # Extract the 'Identity' from Rachel 
        a_rachel = extract_lpc_filter(chunk_r, order=22)
        source_rachel = extract_source(chunk_r, a_rachel)
        
        # RE-SYNTHESIS: Rachel's Identity + Teacher's Mouth
        # We use Rachel's raw vocal buzz but shape it with Google's mouth filter
        resynthesized_chunk = synthesize(source_rachel, a_teacher)
        
        # Windowed Add-Overlap to prevent clicks
        window = np.hanning(win_len)
        output[i:i+win_len] += resynthesized_chunk * window

    # Final Polish
    output = output / (np.max(np.abs(output)) + 1e-6)
    sf.write("LPC_CAT.wav", output, sr)
    print("✨ SUCCESS: Rachel has physically spoken through the Teacher's blueprint.")

if __name__ == "__main__":
    run_bridge("CAT")
