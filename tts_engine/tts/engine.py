
import numpy as np
import sounddevice as sd
from scipy.io import wavfile
from .synthesizer import Synthesizer
from .g2p import text_to_phonemes
from .phoneme_bank import PHONEMES

class TTSEngine:
    
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        self.synth = Synthesizer(sample_rate)
        self.speed = 0.6  # Default to 60% speed for clarity
        
    def set_pitch(self, hz):
        """Set base pitch (default 120 Hz for male, 200 Hz for female)."""
        self.synth.base_pitch = hz
    
    def set_voice(self, preset):
        """Quick voice presets."""
        if preset == "male":
            self.synth.base_pitch = 110
            self.synth.humanizer.breathiness = 0.01
        elif preset == "female":
            self.synth.base_pitch = 200
            self.synth.humanizer.breathiness = 0.02
        elif preset == "warm":
            self.synth.base_pitch = 130
            self.synth.humanizer.breathiness = 0.02
            self.synth.humanizer.shimmer = 0.02
            
    def set_speed(self, factor):
        """Set speed multiplier (e.g. 0.5 = half speed, 1.0 = normal)."""
        self.speed = factor
    
    def speak(self, text):
        """Convert text to speech and play."""
        audio = self.synthesize(text)
        try:
            sd.play(audio, self.sample_rate)
            sd.wait()
        except Exception as e:
            print(f"Audio playback failed (server mode?): {e}")
    
    def synthesize(self, text):
        """Convert text to audio using continuous synthesis."""
        phonemes = text_to_phonemes(text)
        
        # Detect sentence type
        if text.strip().endswith("?"):
            sentence_type = "question"
        elif text.strip().endswith("!"):
            sentence_type = "exclamation"
        else:
            sentence_type = "statement"
        
        # Generate Pitch Contour
        from .prosody import ProsodyEngine
        from .transitions import build_formant_trajectory
        
        # We need total samples first to generate pitch
        # Temporarily build traj to get length
        # (This is inefficient doing it twice, but cleaner code for now)
        # Actually synthesize_continuous builds it.
        # Let's move build_formant_trajectory call here?
        # Or better: make synthesize_continuous handle it.
        # But ProsodyEngine needs total_samples.
        
        # Helper to get length only?
        # Let's just estimate or do it inside synth.
        # We'll instantiate ProsodyEngine here or inside Synthesizer?
        # Engine owns high level logic.
        
        # Let's allow synthesize_continuous to take just text/phonemes?
        # But we need pitch.
        
        # Let's update synthesize_continuous in Synthesizer to call Prosody if we don't pass pitch?
        # No, Engine controls it.
        
        # Hack: Call build_formant_trajectory here.
        from .phoneme_bank import PHONEMES
        traj = build_formant_trajectory(phonemes, PHONEMES, self.sample_rate, speed=self.speed)
        total_samples = traj["total_samples"]
        
        prosody = ProsodyEngine(base_pitch=self.synth.base_pitch, sample_rate=self.sample_rate)
        pitch_contour = prosody.generate_pitch_contour(phonemes, total_samples, sentence_type)
        
        # Use continuous synthesis with coarticulation and pitch
        audio = self.synth.synthesize_continuous(phonemes, pitch_contour=pitch_contour, speed=self.speed)
        
        return audio.astype(np.float32)
    
    def save(self, text, filename):
        """Save speech to WAV file."""
        audio = self.synthesize(text)
        # Convert to 16-bit PCM for compatibility
        audio_int16 = (audio * 32767).astype(np.int16)
        wavfile.write(filename, self.sample_rate, audio_int16)
        print(f"Saved: {filename}")
